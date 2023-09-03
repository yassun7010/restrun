from restrun.openapi.schema import (
    PythonDict,
    PythonLiteralType,
    PythonLiteralUnion,
    get_data_type,
)
from tests.data import load_openapi


class TestSchema:
    def test_petstore_order_schema(self):
        openapi = load_openapi("petstore.openapi_v3_0_2.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "Order", openapi.root.components.schemas["Order"]
        ) == PythonDict(
            name="Order",
            properties={
                "id": PythonLiteralType.INT,
                "petId": PythonLiteralType.INT,
                "quantity": PythonLiteralType.INT,
                "shipDate": PythonLiteralType.DATETIME,
                "status": PythonLiteralUnion(
                    PythonLiteralType.STR,
                    ["placed", "approved", "delivered"],
                ),
                "complete": PythonLiteralType.BOOL,
            },
        )
