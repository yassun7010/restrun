import pytest

from restrun.config import Config
from restrun.generator import AUTO_GENERATED_DOC_COMMENT, is_auto_generated_or_empty
from restrun.generator.context.restrun_context import RestrunContext
from restrun.generator.context.schema_context import SchemaContext
from restrun.generator.schema import SchemaGenerator
from restrun.openapi.schema import (
    PythonArray,
    PythonCustomStr,
    PythonLiteralType,
    PythonLiteralUnion,
    PythonObject,
    PythonObjectProperty,
)
from tests.conftest import format_by_black


class TestSchemaGenerator:
    def test_check_auto_generated(
        self,
        config: Config,
        restrun_context: RestrunContext,
    ) -> None:
        assert is_auto_generated_or_empty(
            SchemaGenerator().generate(
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
        code = SchemaGenerator().generate(
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
        code = SchemaGenerator().generate(
            config,
            restrun_context,
            schema_context,
        )

        assert format_by_black(code) == expected_type(
            schema_context,
            f"Literal = {literal.value}",
        )

    def test_custom_str_type_schema(
        self,
        config: Config,
        restrun_context: RestrunContext,
    ):
        schema_context = SchemaContext(
            type_name="CustomStr",
            file_name="custom_str",
            data_type=PythonCustomStr("custom"),
        )
        code = SchemaGenerator().generate(
            config,
            restrun_context,
            schema_context,
        )
        code = format_by_black(code)

        assert format_by_black(code) == expected_type(
            schema_context,
            "CustomStr = str",
        )

    def test_literal_union_type_schema(
        self,
        config: Config,
        restrun_context: RestrunContext,
    ):
        schema_context = SchemaContext(
            type_name="LiteralUnion",
            file_name="literal_union",
            data_type=PythonLiteralUnion(PythonLiteralType.INT, items=[1, 2, 3]),
        )
        code = SchemaGenerator().generate(
            config,
            restrun_context,
            schema_context,
        )

        assert format_by_black(code) == expected_type(
            schema_context,
            "LiteralUnion = typing.Literal[1, 2, 3]",
        )

    def test_array_type_schema(
        self,
        config: Config,
        restrun_context: RestrunContext,
    ):
        schema_context = SchemaContext(
            type_name="ArrayInt",
            file_name="array_int",
            data_type=PythonArray("ArrayInt", PythonLiteralType.INT),
        )
        code = SchemaGenerator().generate(
            config,
            restrun_context,
            schema_context,
        )

        assert format_by_black(code) == expected_type(
            schema_context,
            "ArrayInt = list[int]",
        )


def expected_type(schema_context: SchemaContext, type_def: str) -> str:
    if len(schema_context.import_field_types) != 0:
        imports = "\n".join(schema_context.import_field_types) + "\n"
    else:
        imports = ""

    return f"{AUTO_GENERATED_DOC_COMMENT}\n{imports}\n\n{type_def}\n"
