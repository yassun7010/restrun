from examples.petstore_pydantic.petstore.client.mock_client import PetstoreMockClient


def test_client():
    PetstoreMockClient.from_bearer_token(token="").request(
        "https://petstore3.com/pet/findByTags"
    ).get({"tags": []})
