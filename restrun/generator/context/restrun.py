from dataclasses import dataclass, field
from glob import glob
from pathlib import Path
from typing import cast

import restrun
from restrun.config import Config
from restrun.core import http
from restrun.core.request import Request
from restrun.generator import ClassInfo, find_classes_from_code
from restrun.generator.context.resource import ResourceContext, make_resource_contexts


@dataclass
class RestrunContext:
    config: Config
    resources: list[ResourceContext]

    client_prefix: str

    version: str = field(default=restrun.__version__)

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
    def request_infos_map(self) -> dict[http.Method, list[ClassInfo[Request]]]:
        results: dict[http.Method, list[ClassInfo[Request]]] = {
            "GET": [],
            "POST": [],
            "PUT": [],
            "PATCH": [],
            "DELETE": [],
        }

        for resource in self.resources:
            for method, request_info in resource.method_map.items():
                results[cast(http.Method, method)].append(
                    cast(ClassInfo[Request], request_info)
                )

        return results


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
        config=config,
        client_prefix=config.name,
        client_mixins=client_mixins,
        real_client_mixins=real_client_mixins,
        mock_client_mixins=mock_client_mixins,
        resources=make_resource_contexts(base_dir),
    )
