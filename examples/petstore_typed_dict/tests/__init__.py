from petstore.client.mock_client import PetstoreMockClient
from petstore.resources.pet_pet_id_upload_image.post_pet_pet_id_upload_image import (
    PostPetPetIdUploadImageResponseBody,
)


def test_client():
    PetstoreMockClient.from_bearer_token(token="").inject_post_response(
        "https://petstore3.com/pet/{petId}/uploadImage",
        response=PostPetPetIdUploadImageResponseBody(code=123),
    ).request("https://petstore3.com/pet/findByTags").get({"tags": []})
