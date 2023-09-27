from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator import write_python_code
from restrun.utils.strcase import module_name


if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator.context.operation_context import OperationContext
    from restrun.generator.context.resource_context import ResourceContext
    from restrun.generator.context.resources_context import ResourcesContext
    from restrun.generator.context.restrun_context import RestrunContext
    from restrun.generator.context.schema_context import SchemaContext


logger = getLogger(__name__)


def write_root_module(
    base_dir: Path,
    config: "Config",
    context: "RestrunContext",
) -> None:
    from restrun.generator.root_module import RootModuleGenerator

    write_python_code(
        base_dir / "__init__.py",
        lambda: RootModuleGenerator.generate(config, context),
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


def write_schema(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    schema_context: "SchemaContext",
):
    from restrun.generator.schema import SchemaGenerator

    write_python_code(
        base_dir / "schemas" / f"{schema_context.file_name}.py",
        lambda: SchemaGenerator.generate(config, restrun_context, schema_context),
    )


def write_schemas(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    schema_contexts: "list[SchemaContext]",
):
    from restrun.generator.schemas_module import SchemasModuleGenerator

    write_python_code(
        base_dir / "schemas" / "__init__.py",
        lambda: SchemasModuleGenerator.generate(config, restrun_context),
    )

    for schema_context in schema_contexts:
        write_schema(
            base_dir,
            config,
            restrun_context,
            schema_context,
        )


def write_operation(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    operation_context: "OperationContext",
) -> None:
    from restrun.generator.operation import OperationGenerator

    write_python_code(
        base_dir
        / "resources"
        / module_name(operation_context.path_name)
        / f"{module_name(operation_context.class_name)}.py",
        lambda: OperationGenerator.generate(
            config,
            restrun_context,
            operation_context,
        ),
    )


def write_operations(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    operation_contexts: "list[OperationContext]",
) -> None:
    for operation_context in operation_contexts:
        write_operation(
            base_dir,
            config,
            restrun_context,
            operation_context,
        )


def write_resource(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    resource_context: "ResourceContext",
) -> None:
    from restrun.generator.resource_module import ResourceModuleGenerator

    write_python_code(
        base_dir / "resources" / resource_context.module_name / "__init__.py",
        lambda: ResourceModuleGenerator.generate(
            config, restrun_context, resource_context
        ),
    )


def write_resources(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    resources_context: "ResourcesContext",
) -> None:
    from restrun.generator.resources_module import ResourcesModuleGenerator

    write_python_code(
        base_dir / "resources" / "__init__.py",
        lambda: ResourcesModuleGenerator.generate(
            config,
            restrun_context,
            resources_context,
        ),
    )

    for resource_context in resources_context:
        write_resource(
            base_dir,
            config,
            restrun_context,
            resource_context,
        )


def write_python_codes(base_dir: Path, config: "Config", config_path: Path) -> None:
    import importlib.util
    import sys

    from pathlib import Path

    from restrun.generator.context.operation_context import make_operation_contexts
    from restrun.generator.context.resources_context import make_resources_context
    from restrun.generator.context.restrun_context import make_rustrun_context
    from restrun.generator.context.schema_context import make_schema_contexts

    restrun_context = make_rustrun_context(base_dir, config)

    write_root_module(base_dir, config, restrun_context)

    # import root module for operation module load.
    if spec := importlib.util.spec_from_file_location(
        str(base_dir), base_dir / "__init__.py"
    ):
        if module := importlib.util.module_from_spec(spec):
            sys.modules[spec.name] = module

    for source in config.root.sources:
        if source.type == "openapi":
            if (
                isinstance(source.location, Path)
                and not source.location.exists()
                and (config_path.parent / source.location).exists()
            ):
                source.location = config_path.parent / source.location

            write_schemas(
                base_dir, config, restrun_context, make_schema_contexts(source)
            )

            write_operations(
                base_dir,
                config,
                restrun_context,
                make_operation_contexts(source.server_urls, source),
            )

    resources_context = make_resources_context(base_dir)

    write_resources(base_dir, config, restrun_context, resources_context)
    write_clients(base_dir, config, restrun_context, resources_context)
