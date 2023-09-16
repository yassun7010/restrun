import pytest

from restrun.config import Config
from restrun.generator import AUTO_GENERATED_DOC_COMMENT, is_auto_generated_or_empty
from restrun.generator.context.restrun_context import RestrunContext
from restrun.generator.context.schema_context import SchemaContext
from restrun.generator.schema_typed_dict import SchemaTypedDictGenerator
from restrun.openapi.schema import PythonLiteralType, PythonObject, PythonObjectProperty
from tests.conftest import format_by_black


class TestSchemaTypedDictGenerator:
    def test_check_auto_generated(
        self,
        config: Config,
        restrun_context: RestrunContext,
    ) -> None:
        assert is_auto_generated_or_empty(
            SchemaTypedDictGenerator().generate(
                config,
                restrun_context,
                SchemaContext(
                    type_name="User",
                    file_name="user",
                    data_type=PythonObject(
                        class_name="User",
                        properties={
                            "id": PythonObjectProperty(
                                PythonLiteralType.INT, required=True
                            ),
                            "name": PythonObjectProperty(
                                PythonLiteralType.STR, required=True
                            ),
                            "age": PythonObjectProperty(
                                PythonLiteralType.INT, required=True
                            ),
                        },
                    ),
                ),
            )
        )

    def test_validate_generated_code(
        self,
        config: Config,
        restrun_context: RestrunContext,
    ):
        locales = {}
        code = SchemaTypedDictGenerator().generate(
            config,
            restrun_context,
            SchemaContext(
                type_name="User",
                file_name="user",
                data_type=PythonObject(
                    class_name="User",
                    properties={
                        "id": PythonObjectProperty(
                            PythonLiteralType.INT, required=True
                        ),
                        "name": PythonObjectProperty(
                            PythonLiteralType.STR, required=True
                        ),
                        "age": PythonObjectProperty(
                            PythonLiteralType.INT, required=True
                        ),
                    },
                ),
            ),
        )

        exec(code, None, locales)

        print(code)

        assert locales["User"] is not None

    @pytest.mark.parametrize(
        "literal",
        list(PythonLiteralType),
    )
    def test_literal_type_schema(
        self,
        config: Config,
        restrun_context: RestrunContext,
        literal: PythonLiteralType,
    ):
        schema_context = SchemaContext(
            type_name="Literal",
            file_name="literal",
            data_type=literal,
        )
        code = SchemaTypedDictGenerator().generate(
            config,
            restrun_context,
            schema_context,
        )
        code = format_by_black(code)
        if len(schema_context.import_field_types) != 0:
            imports = "\n".join(schema_context.import_field_types) + "\n"
        else:
            imports = ""

        assert (
            code
            == f"{AUTO_GENERATED_DOC_COMMENT}\n{imports}\n\nLiteral = {literal.value}\n"
        )
