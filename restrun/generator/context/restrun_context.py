from dataclasses import dataclass, field
from glob import glob
from pathlib import Path
from typing import cast

import restrun
from restrun.config import Config
from restrun.core import http
from restrun.core.operation import Operation
from restrun.generator import ClassInfo, find_classes_from_code
from restrun.generator.context.resource_context import (
    ResourceContext,
    make_resource_contexts,
)


@dataclass(frozen=True)
class RestrunContext:
    resources: list[ResourceContext]

    client_prefix: str

    server_urls: list[http.URL]

    version: str = restrun.__version__

    client_mixins: list[ClassInfo] = field(default_factory=list)

    real_client_mixins: list[ClassInfo] = field(default_factory=list)

    mock_client_mixins: list[ClassInfo] = field(default_factory=list)

    @property
    def client_mixin_path_names(self) -> list[str]:
        return [
            f"{mixin.module_name}.{mixin.class_name}" for mixin in self.client_mixins
        ]

    @property
    def real_client_mixin_path_names(self) -> list[str]:
        return [
            f"{mixin.module_name}.{mixin.class_name}"
            for mixin in self.real_client_mixins
        ]

    @property
    def mock_client_mixin_path_names(self) -> list[str]:
        return [
            f"{mixin.module_name}.{mixin.class_name}"
            for mixin in self.mock_client_mixins
        ]

    @property
    def has_operation(self) -> bool:
        return (
            sum(
                len(operation_infos)
                for operation_infos in self.operation_infos_map.values()
            )
            != 0
        )

    @property
    def operation_infos_map(self) -> dict[http.Method, tuple[ClassInfo[Operation]]]:
        results: dict[http.Method, list[ClassInfo[Operation]]] = {
            "GET": [],
            "POST": [],
            "PUT": [],
            "PATCH": [],
            "DELETE": [],
        }

        for resource in self.resources:
            for method, operation_info in resource.operation_map.items():
                results[cast(http.Method, method)].append(
                    cast(ClassInfo[Operation], operation_info)
                )

        return {
            method: tuple(operation_infos)
            for method, operation_infos in results.items()
        }

    def get_operation_urls(
        self, resource_info: "ClassInfo[Operation]"
    ) -> list[http.URL]:
        return [
            f'{url.rstrip("/")}/{resource_info.class_type.path.lstrip("/")}'
            for url in self.server_urls
        ]

    def get_resource_urls(self, resource: "ResourceContext") -> list[http.URL]:
        urls: set[http.URL] = set()
        for operation in resource.operations:
            urls.update(self.get_operation_urls(operation))

        return list(sorted(urls))


def make_rustrun_context(base_dir: Path, config: Config) -> RestrunContext:
    client_mixins_dir = base_dir / "client" / "mixins"

    client_mixins: list[ClassInfo] = []
    real_client_mixins: list[ClassInfo] = []
    mock_client_mixins: list[ClassInfo] = []

    if client_mixins_dir.exists():
        from restrun.core.client import (
            RestrunClientMixin,
            RestrunMockClientMixin,
            RestrunRealClientMixin,
        )

        for pyfile in glob(str(client_mixins_dir / "*.py")):
            pypath = Path(pyfile)

            mixins_map = find_classes_from_code(
                pypath,
                RestrunClientMixin,
                RestrunRealClientMixin,
                RestrunMockClientMixin,
            )
            client_mixins.extend(mixins_map[RestrunClientMixin])
            real_client_mixins.extend(mixins_map[RestrunRealClientMixin])
            mock_client_mixins.extend(mixins_map[RestrunMockClientMixin])

    return RestrunContext(
        client_prefix=config.name,
        server_urls=config.server_urls,
        client_mixins=client_mixins,
        real_client_mixins=real_client_mixins,
        mock_client_mixins=mock_client_mixins,
        resources=make_resource_contexts(base_dir),
    )
