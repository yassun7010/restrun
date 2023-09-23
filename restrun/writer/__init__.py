from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator import write_python_code
from restrun.generator.operation import OperationGenerator
from restrun.strcase import module_name

if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator.context.operation_context import OperationContext
    from restrun.generator.context.resources_context import ResourcesContext
    from restrun.generator.context.restrun_context import RestrunContext
    from restrun.generator.context.schema_context import SchemaContext


logger = getLogger(__name__)


def write_module(base_dir: Path, config: "Config", context: "RestrunContext") -> None:
    from restrun.generator.module import ModuleGenerator

    write_python_code(
        base_dir / "__init__.py",
        lambda: ModuleGenerator().generate(config, context),
    )


def write_clients(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    resources_context: "ResourcesContext",
) -> None:
    from restrun.generator.client import ClientGenerator
    from restrun.generator.client_mixins_module import ClientMixinsModuleGenerator
    from restrun.generator.client_module import ClientModuleGenerator
    from restrun.generator.mock_client import MockClientGenerator
    from restrun.generator.real_client import RealClientGenerator

    for filename, generator in [
        ("client.py", ClientGenerator()),
        ("real_client.py", RealClientGenerator()),
        ("mock_client.py", MockClientGenerator()),
        ("__init__.py", ClientModuleGenerator()),
        (Path("mixins") / "__init__.py", ClientMixinsModuleGenerator()),
    ]:
        write_python_code(
            base_dir / "client" / filename,
            lambda: generator.generate(
                config,
                restrun_context,
                resources_context,
            ),
        )


def write_schemas(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    schema_contexts: "list[SchemaContext]",
):
    from restrun.generator.schema import SchemaGenerator
    from restrun.generator.schemas_module import SchemasModuleGenerator

    write_python_code(
        base_dir / "schemas" / "__init__.py",
        lambda: SchemasModuleGenerator().generate(config, restrun_context),
    )

    for schema_context in schema_contexts:
        write_python_code(
            base_dir / "schemas" / f"{schema_context.file_name}.py",
            lambda: SchemaGenerator().generate(config, restrun_context, schema_context),
        )


def write_operations(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    operation_contexts: "list[OperationContext]",
) -> None:
    for operation_context in operation_contexts:
        write_python_code(
            base_dir
            / "resources"
            / module_name(operation_context.path_name)
            / f"{module_name(operation_context.class_name)}.py",
            lambda: OperationGenerator().generate(
                config,
                restrun_context,
                operation_context,
            ),
        )


def write_resources(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    resources_context: "ResourcesContext",
) -> None:
    from restrun.generator.resource_module import ResourceModuleGenerator
    from restrun.generator.resources_module import ResourcesModuleGenerator

    for resource_context in resources_context:
        write_python_code(
            base_dir / "resources" / resource_context.module_name / "__init__.py",
            lambda: ResourceModuleGenerator().generate(
                config, restrun_context, resource_context
            ),
        )

    write_python_code(
        base_dir / "resources" / "__init__.py",
        lambda: ResourcesModuleGenerator().generate(
            config,
            restrun_context,
            resources_context,
        ),
    )
