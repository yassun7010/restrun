from collections import OrderedDict

from restrun.openapi.schema import PythonDict, get_data_type
from tests.data import load_openapi


class TestSchema:
    def test_petstore(self):
        openapi = load_openapi("petstore.openapi.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "Order", openapi.root.components.schemas["Order"]
        ) == PythonDict(
            name="Order",
            properties=OrderedDict(),
        )
