import pytest

from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.context.restrun_context import RestrunContext
from restrun.generator.context.schema_context import SchemaContext
from restrun.generator.schema_typed_dict import SchemaTypedDictGenerator
from restrun.openapi.schema import PythonLiteralType, PythonObject, PythonObjectProperty


@pytest.fixture
def schema_context() -> SchemaContext:
    return SchemaContext(
        type_name="User",
        file_name="user",
        data_type=PythonObject(
            class_name="User",
            properties={
                "id": PythonObjectProperty(PythonLiteralType.INT, required=True),
                "name": PythonObjectProperty(PythonLiteralType.STR, required=True),
                "age": PythonObjectProperty(PythonLiteralType.INT, required=True),
            },
        ),
    )


class TestSchemaTypedDictGenerator:
    def test_check_auto_generated(
        self,
        config: Config,
        restrun_context: RestrunContext,
        schema_context: SchemaContext,
    ) -> None:
        assert is_auto_generated_or_empty(
            SchemaTypedDictGenerator().generate(config, restrun_context, schema_context)
        )

    def test_validate_generated_code(
        self,
        config: Config,
        restrun_context: RestrunContext,
        schema_context: SchemaContext,
    ):
        locales = {}
        code = SchemaTypedDictGenerator().generate(
            config, restrun_context, schema_context
        )

        exec(code, None, locales)

        print(code)

        assert locales["UserDict"] is not None
