from pathlib import Path
from typing import TYPE_CHECKING

from restrun.generator.schema_typed_dict import SchemaTypedDictGenerator

if TYPE_CHECKING:
    from restrun.config import Config
    from restrun.generator.context.restrun_context import RestrunContext
    from restrun.generator.context.schema_context import SchemaContext


def write_clients(base_dir: Path, config: "Config", context: "RestrunContext") -> None:
    from restrun.generator import is_auto_generated_or_empty
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
        filepath = base_dir / "client" / filename

        if filepath.exists() and not is_auto_generated_or_empty(filepath):
            continue

        code = generator.generate(config, context)
        with open(filepath, "w") as file:
            file.write(code)


def write_schemas(
    base_dir: Path,
    config: "Config",
    restrun_context: "RestrunContext",
    schema_contexts: "list[SchemaContext]",
):
    from restrun.generator import is_auto_generated_or_empty
    from restrun.generator.schemas_module import SchemasModuleGenerator

    schema_dir_path = base_dir / "schemas"
    if not schema_dir_path.exists():
        schema_dir_path.mkdir()

    filepath = schema_dir_path / "__init__.py"

    if filepath.exists() and not is_auto_generated_or_empty(filepath):
        return

    code = SchemasModuleGenerator().generate(config, restrun_context)
    with open(filepath, "w") as file:
        file.write(code)

    for schema_context in schema_contexts:
        filepath = schema_dir_path / f"{schema_context.file_name}.py"
        code = SchemaTypedDictGenerator().generate(
            config, restrun_context, schema_context
        )
        with open(filepath, "w") as file:
            file.write(code)


def write_resources(
    base_dir: Path, config: "Config", context: "RestrunContext"
) -> None:
    from restrun.generator import is_auto_generated_or_empty
    from restrun.generator.resource_module import ResourceModuleGenerator
    from restrun.generator.resources_module import ResourcesModuleGenerator

    for resource_context in context.resources:
        filepath = base_dir / "resources" / resource_context.module_name / "__init__.py"
        if filepath.exists() and not is_auto_generated_or_empty(filepath):
            continue

        code = ResourceModuleGenerator().generate(config, context, resource_context)
        with open(
            base_dir / "resources" / resource_context.module_name / "__init__.py", "w"
        ) as file:
            file.write(code)

    filepath = base_dir / "resources" / "__init__.py"
    if filepath.exists() and not is_auto_generated_or_empty(filepath):
        return

    code = ResourcesModuleGenerator().generate(config, context)
    with open(filepath, "w") as file:
        file.write(code)
