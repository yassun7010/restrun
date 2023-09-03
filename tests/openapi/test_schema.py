from restrun.openapi.schema import (
    PythonArray,
    PythonDict,
    PythonLiteralType,
    PythonLiteralUnion,
    PythonReference,
    get_data_type,
)
from tests.data import load_openapi


class TestSchema:
    def test_petstore_order_schema(self):
        openapi = load_openapi("petstore.openapi_v3_0_2.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "Order",
            openapi.root.components.schemas["Order"],
            openapi.root.components.schemas,
        ) == PythonDict(
            class_name="Order",
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

    def test_petstore_customer_schema(self):
        openapi = load_openapi("petstore.openapi_v3_0_2.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "Customer",
            openapi.root.components.schemas["Customer"],
            openapi.root.components.schemas,
        ) == PythonDict(
            class_name="Customer",
            properties={
                "id": PythonLiteralType.INT,
                "username": PythonLiteralType.STR,
                "address": PythonArray(
                    name="address",
                    items=PythonReference(
                        ref="#/components/schemas/Address",
                        target=PythonDict(
                            class_name="Address",
                            properties={
                                "street": PythonLiteralType.STR,
                                "city": PythonLiteralType.STR,
                                "state": PythonLiteralType.STR,
                                "zip": PythonLiteralType.STR,
                            },
                        ),
                    ),
                ),
            },
        )

    def test_petstore_address_schema(self):
        openapi = load_openapi("petstore.openapi_v3_0_2.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "Address",
            openapi.root.components.schemas["Address"],
            openapi.root.components.schemas,
        ) == PythonDict(
            class_name="Address",
            properties={
                "street": PythonLiteralType.STR,
                "city": PythonLiteralType.STR,
                "state": PythonLiteralType.STR,
                "zip": PythonLiteralType.STR,
            },
        )

    def test_petstore_category_schema(self):
        openapi = load_openapi("petstore.openapi_v3_0_2.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "Category",
            openapi.root.components.schemas["Category"],
            openapi.root.components.schemas,
        ) == PythonDict(
            class_name="Category",
            properties={
                "id": PythonLiteralType.INT,
                "name": PythonLiteralType.STR,
            },
        )

    def test_potstore_user_schema(self):
        openapi = load_openapi("petstore.openapi_v3_0_2.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "User",
            openapi.root.components.schemas["User"],
            openapi.root.components.schemas,
        ) == PythonDict(
            class_name="User",
            properties={
                "id": PythonLiteralType.INT,
                "username": PythonLiteralType.STR,
                "firstName": PythonLiteralType.STR,
                "lastName": PythonLiteralType.STR,
                "email": PythonLiteralType.STR,
                "password": PythonLiteralType.STR,
                "phone": PythonLiteralType.STR,
                "userStatus": PythonLiteralType.INT,
            },
        )
