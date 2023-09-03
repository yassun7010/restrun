from tests.data import load_openapi


class TestSchema:
    def test_petstore(self):
        load_openapi("petstore.openapi.json")
