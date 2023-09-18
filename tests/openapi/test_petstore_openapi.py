from restrun.openapi.schema import (
    PythonArray,
    PythonLiteralType,
    PythonLiteralUnion,
    PythonObject,
    PythonObjectProperty,
    PythonReference,
    get_data_type,
)

from . import load_openapi


class TestSchema:
    def test_petstore_order_schema(self):
        openapi = load_openapi("petstore.openapi_v3_0_2.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "Order",
            openapi.root.components.schemas["Order"],
            openapi.root.components.schemas,
        ) == PythonObject(
            type_name="Order",
            properties={
                "id": PythonObjectProperty(PythonLiteralType.INT),
                "petId": PythonObjectProperty(PythonLiteralType.INT),
                "quantity": PythonObjectProperty(PythonLiteralType.INT),
                "shipDate": PythonObjectProperty(PythonLiteralType.DATETIME),
                "status": PythonObjectProperty(
                    PythonLiteralUnion(
                        PythonLiteralType.STR,
                        ["placed", "approved", "delivered"],
                    ),
                    description="Order Status",
                ),
                "complete": PythonObjectProperty(PythonLiteralType.BOOL),
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
        ) == PythonObject(
            type_name="Customer",
            properties={
                "id": PythonObjectProperty(PythonLiteralType.INT),
                "username": PythonObjectProperty(PythonLiteralType.STR),
                "address": PythonObjectProperty(
                    PythonArray(
                        item_data_type=PythonReference(
                            ref="#/components/schemas/Address",
                            target=PythonObject(
                                type_name="Address",
                                properties={
                                    "street": PythonObjectProperty(
                                        PythonLiteralType.STR
                                    ),
                                    "city": PythonObjectProperty(PythonLiteralType.STR),
                                    "state": PythonObjectProperty(
                                        PythonLiteralType.STR
                                    ),
                                    "zip": PythonObjectProperty(PythonLiteralType.STR),
                                },
                            ),
                        ),
                    )
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
        ) == PythonObject(
            type_name="Address",
            properties={
                "street": PythonObjectProperty(PythonLiteralType.STR),
                "city": PythonObjectProperty(PythonLiteralType.STR),
                "state": PythonObjectProperty(PythonLiteralType.STR),
                "zip": PythonObjectProperty(PythonLiteralType.STR),
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
        ) == PythonObject(
            type_name="Category",
            properties={
                "id": PythonObjectProperty(PythonLiteralType.INT),
                "name": PythonObjectProperty(PythonLiteralType.STR),
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
        ) == PythonObject(
            type_name="User",
            properties={
                "id": PythonObjectProperty(PythonLiteralType.INT),
                "username": PythonObjectProperty(PythonLiteralType.STR),
                "firstName": PythonObjectProperty(PythonLiteralType.STR),
                "lastName": PythonObjectProperty(PythonLiteralType.STR),
                "email": PythonObjectProperty(PythonLiteralType.STR),
                "password": PythonObjectProperty(PythonLiteralType.STR),
                "phone": PythonObjectProperty(PythonLiteralType.STR),
                "userStatus": PythonObjectProperty(
                    PythonLiteralType.INT, description="User Status"
                ),
            },
        )

    def test_petstore_tag_schema(self):
        openapi = load_openapi("petstore.openapi_v3_0_2.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "Tag",
            openapi.root.components.schemas["Tag"],
            openapi.root.components.schemas,
        ) == PythonObject(
            type_name="Tag",
            properties={
                "id": PythonObjectProperty(PythonLiteralType.INT),
                "name": PythonObjectProperty(PythonLiteralType.STR),
            },
        )

    def test_petstore_pet_schema(self):
        openapi = load_openapi("petstore.openapi_v3_0_2.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "Pet",
            openapi.root.components.schemas["Pet"],
            openapi.root.components.schemas,
        ) == PythonObject(
            type_name="Pet",
            properties={
                "id": PythonObjectProperty(PythonLiteralType.INT),
                "name": PythonObjectProperty(
                    PythonLiteralType.STR,
                    required=True,
                ),
                "category": PythonObjectProperty(
                    PythonReference(
                        ref="#/components/schemas/Category",
                        target=PythonObject(
                            type_name="Category",
                            properties={
                                "id": PythonObjectProperty(PythonLiteralType.INT),
                                "name": PythonObjectProperty(PythonLiteralType.STR),
                            },
                        ),
                    )
                ),
                "photoUrls": PythonObjectProperty(
                    PythonArray(
                        item_data_type=PythonLiteralType.STR,
                    ),
                    required=True,
                ),
                "tags": PythonObjectProperty(
                    PythonArray(
                        item_data_type=PythonReference(
                            ref="#/components/schemas/Tag",
                            target=PythonObject(
                                type_name="Tag",
                                properties={
                                    "id": PythonObjectProperty(PythonLiteralType.INT),
                                    "name": PythonObjectProperty(PythonLiteralType.STR),
                                },
                            ),
                        ),
                    )
                ),
                "status": PythonObjectProperty(
                    PythonLiteralUnion(
                        PythonLiteralType.STR,
                        ["available", "pending", "sold"],
                    ),
                    description="pet status in the store",
                ),
            },
        )

    def test_petstore_api_response_schema(self):
        openapi = load_openapi("petstore.openapi_v3_0_2.json")

        assert openapi.root.components is not None
        assert openapi.root.components.schemas is not None

        assert get_data_type(
            "ApiResponse",
            openapi.root.components.schemas["ApiResponse"],
            openapi.root.components.schemas,
        ) == PythonObject(
            type_name="ApiResponse",
            properties={
                "code": PythonObjectProperty(PythonLiteralType.INT),
                "type": PythonObjectProperty(PythonLiteralType.STR),
                "message": PythonObjectProperty(PythonLiteralType.STR),
            },
        )
