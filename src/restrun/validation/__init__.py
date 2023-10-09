from typing import Any


try:
    from pydantic import TypeAdapter  # type: ignore

    _USE_PYDANTIC = True


except ImportError:  # pragma: no cover

    class TypeAdapter[T]:
        def __init__(self, __type: type[T], *args, **kwargs) -> None:
            pass

        def validate_python(self, data: Any) -> T:
            return data

    _USE_PYDANTIC = False


def validate_schema[T](data: Any, adapter: TypeAdapter[T]) -> T:
    if _USE_PYDANTIC:
        return adapter.validate_python(data)

    else:
        return data


__all__ = ["validate_schema"]
