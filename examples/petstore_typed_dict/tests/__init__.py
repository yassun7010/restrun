from petstore.client.mock_client import PetstoreMockClient
from petstore.resources.pet_pet_id.get_pet_pet_id import GetPetPetIdResponseBody


def test_client():
    (
        PetstoreMockClient.from_bearer_token(token="")
        .inject_get_response(
            "https://petstore3.com/pet/{petId}",
            response=GetPetPetIdResponseBody(
                id=12,
                name="aaa",
                status="available",
                photoUrls=[],
            ),
        )
        .request("https://petstore3.com/pet/findByTags")
        .get()
    )
