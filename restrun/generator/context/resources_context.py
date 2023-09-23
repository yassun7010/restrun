from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Iterator, cast
from restrun.core import http
from restrun.core.operation import Operation
from restrun.generator import ClassInfo

from restrun.generator.context.resource_context import (
    ResourceContext,
    make_resource_context,
)


@dataclass(frozen=True)
class ResourcesContext:
    resources: list[ResourceContext]

    def __iter__(self) -> Iterator[ResourceContext]:
        return iter(self.resources)

    def __len__(self) -> int:
        return len(self.resources)

    @cached_property
    def is_empty(self) -> bool:
        return (
            sum(
                len(operation_infos)
                for operation_infos in self.operation_infos_map.values()
            )
            != 0
        )

    @property
    def operation_infos_map(self) -> dict[http.Method, list[ClassInfo[Operation]]]:
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

        return results


def make_resources_context(base_dir: Path) -> ResourcesContext:
    resource_contexts = []

    resources_path = base_dir / "resources"
    if not resources_path.exists():
        resources_path.mkdir(parents=True)

    for resource_dir in resources_path.iterdir():
        if not resource_dir.is_dir():
            continue

        if resource_context := make_resource_context(resource_dir):
            resource_contexts.append(resource_context)

    return ResourcesContext(
        resources=resource_contexts,
    )
