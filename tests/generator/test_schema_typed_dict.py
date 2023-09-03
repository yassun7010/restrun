import pytest

from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.context.restrun_context import RestrunContext
from restrun.generator.context.schema_context import SchemaContext
from restrun.generator.schema_typed_dict import SchemaTypedDictGenerator
from restrun.openapi.schema import PythonDictField, PythonLiteralType


@pytest.fixture
def schema_context() -> SchemaContext:
    return SchemaContext(
        class_name="User",
        fields={
            "id": PythonDictField(PythonLiteralType.INT, required=True),
            "name": PythonDictField(PythonLiteralType.STR, required=True),
            "age": PythonDictField(PythonLiteralType.INT, required=True),
        },
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

        assert locales["User"] is not None
