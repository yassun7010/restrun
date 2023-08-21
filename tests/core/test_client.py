import pytest

from restrun.core.client import RestrunClient


def test_cannot_create_client_by_constructor() -> None:
    with pytest.raises(TypeError):
        RestrunClient()  # type: ignore
