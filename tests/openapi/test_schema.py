from restrun.openapi.schema import (
    PythonArray,
    PythonDict,
    PythonDictField,
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
                "id": PythonDictField(PythonLiteralType.INT),
                "petId": PythonDictField(PythonLiteralType.INT),
                "quantity": PythonDictField(PythonLiteralType.INT),
                "shipDate": PythonDictField(PythonLiteralType.DATETIME),
                "status": PythonDictField(
                    PythonLiteralUnion(
                        PythonLiteralType.STR,
                        ["placed", "approved", "delivered"],
                    )
                ),
                "complete": PythonDictField(PythonLiteralType.BOOL),
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
                "id": PythonDictField(PythonLiteralType.INT),
                "username": PythonDictField(PythonLiteralType.STR),
                "address": PythonDictField(
                    PythonArray(
                        name="address",
                        items=PythonReference(
                            ref="#/components/schemas/Address",
                            target=PythonDict(
                                class_name="Address",
                                properties={
                                    "street": PythonDictField(PythonLiteralType.STR),
                                    "city": PythonDictField(PythonLiteralType.STR),
                                    "state": PythonDictField(PythonLiteralType.STR),
                                    "zip": PythonDictField(PythonLiteralType.STR),
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
        ) == PythonDict(
            class_name="Address",
            properties={
                "street": PythonDictField(PythonLiteralType.STR),
                "city": PythonDictField(PythonLiteralType.STR),
                "state": PythonDictField(PythonLiteralType.STR),
                "zip": PythonDictField(PythonLiteralType.STR),
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
                "id": PythonDictField(PythonLiteralType.INT),
                "name": PythonDictField(PythonLiteralType.STR),
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
                "id": PythonDictField(PythonLiteralType.INT),
                "username": PythonDictField(PythonLiteralType.STR),
                "firstName": PythonDictField(PythonLiteralType.STR),
                "lastName": PythonDictField(PythonLiteralType.STR),
                "email": PythonDictField(PythonLiteralType.STR),
                "password": PythonDictField(PythonLiteralType.STR),
                "phone": PythonDictField(PythonLiteralType.STR),
                "userStatus": PythonDictField(PythonLiteralType.INT),
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
        ) == PythonDict(
            class_name="Tag",
            properties={
                "id": PythonDictField(PythonLiteralType.INT),
                "name": PythonDictField(PythonLiteralType.STR),
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
        ) == PythonDict(
            class_name="Pet",
            properties={
                "id": PythonDictField(PythonLiteralType.INT),
                "name": PythonDictField(
                    PythonLiteralType.STR,
                    required=True,
                ),
                "category": PythonDictField(
                    PythonReference(
                        ref="#/components/schemas/Category",
                        target=PythonDict(
                            class_name="Category",
                            properties={
                                "id": PythonDictField(PythonLiteralType.INT),
                                "name": PythonDictField(PythonLiteralType.STR),
                            },
                        ),
                    )
                ),
                "photoUrls": PythonDictField(
                    PythonArray(
                        name="photoUrls",
                        items=PythonLiteralType.STR,
                    ),
                    required=True,
                ),
                "tags": PythonDictField(
                    PythonArray(
                        name="tags",
                        items=PythonReference(
                            ref="#/components/schemas/Tag",
                            target=PythonDict(
                                class_name="Tag",
                                properties={
                                    "id": PythonDictField(PythonLiteralType.INT),
                                    "name": PythonDictField(PythonLiteralType.STR),
                                },
                            ),
                        ),
                    )
                ),
                "status": PythonDictField(
                    PythonLiteralUnion(
                        PythonLiteralType.STR,
                        ["available", "pending", "sold"],
                    )
                ),
            },
        )
