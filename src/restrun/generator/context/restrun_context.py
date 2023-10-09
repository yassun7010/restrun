from dataclasses import dataclass, field
from glob import glob
from pathlib import Path

import restrun

from restrun.config import Config
from restrun.core import http
from restrun.core.operation import Operation
from restrun.generator import ClassInfo, find_classes_from_code
from restrun.generator.context.resource_context import ResourceContext


@dataclass(frozen=True)
class RestrunContext:
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

    def get_operation_urls(
        self, resource_info: "ClassInfo[Operation]"
    ) -> list[http.URL]:
        urls = [
            f'{url.rstrip("/")}/{resource_info.class_type.path.lstrip("/")}'
            for url in self.server_urls
        ]

        return (
            urls
            if len(urls) != 0
            else [
                http.URL(
                    f"https://example.com/{resource_info.class_type.path.strip('/')}"
                )
            ]
        )

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
    )
