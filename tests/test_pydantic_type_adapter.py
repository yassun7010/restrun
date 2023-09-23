import pytest

from pydantic import ConfigDict, TypeAdapter, ValidationError
from typing_extensions import TypedDict


class TestPydanticTypeAdapter:
    @pytest.mark.parametrize(
        "type, expected",
        [
            (int, 1),
            (float, 1.0),
            (str, "foo"),
            (bool, True),
            (list, []),
            (dict, {}),
        ],
    )
    def test_literal_type_adapter(self, type, expected):
        TypeAdapter(type).validate_python(expected)

    def test_typed_dict_type_adapter(self):
        class A(TypedDict):
            a: int
            b: str

        TypeAdapter(A).validate_python({"a": 1, "b": "foo"})
        TypeAdapter(A).validate_python({"a": 1, "b": "foo", "c": {}})

        with pytest.raises(ValidationError):
            TypeAdapter(A).validate_python({"a": 1})

    def test_forbit_typed_dict_type_adapter(self):
        class A(TypedDict):
            __pydantic_config__ = ConfigDict(extra="forbid")  # type: ignore

            a: int
            b: str

        TypeAdapter(A).validate_python({"a": 1, "b": "foo"})

        with pytest.raises(ValidationError):
            TypeAdapter(A).validate_python({"a": 1, "b": "foo", "c": {}})

        with pytest.raises(ValidationError):
            TypeAdapter(A).validate_python({"a": 1})

    def test_nested_typed_dict_type_adapter(self):
        class A(TypedDict):
            a: int
            b: "B"

        class B(TypedDict):
            c: int
            d: str

        TypeAdapter(A).validate_python({"a": 1, "b": {"c": 1, "d": "foo"}})
        TypeAdapter(A).validate_python({"a": 1, "b": {"c": 1, "d": "foo"}, "c": {}})

        with pytest.raises(ValidationError):
            TypeAdapter(A).validate_python({"a": 1})

    def test_forbit_nested_typed_dict_type_adapter(self):
        class A(TypedDict):
            __pydantic_config__ = ConfigDict(extra="forbid")  # type: ignore

            a: int
            b: "B"

        class B(TypedDict):
            __pydantic_config__ = ConfigDict(extra="forbid")  # type: ignore

            c: int
            d: str

        TypeAdapter(A).validate_python({"a": 1, "b": {"c": 1, "d": "foo"}})

        with pytest.raises(ValidationError):
            TypeAdapter(A).validate_python({"a": 1})

        with pytest.raises(ValidationError):
            TypeAdapter(A).validate_python({"a": 1, "b": {"c": 1, "d": "foo"}, "c": {}})

        with pytest.raises(ValidationError):
            TypeAdapter(A).validate_python(
                {"a": 1, "b": {"c": 1, "d": "foo", "e": "bar"}}
            )
