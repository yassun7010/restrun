from dataclasses import dataclass

from restrun.openapi.schema import PythonDictField


@dataclass(frozen=True)
class SchemaContext:
    class_name: str
    fields: dict[str, PythonDictField]
    additional_properties: bool = True

    @property
    def import_field_types(self) -> list[str]:
        return []
