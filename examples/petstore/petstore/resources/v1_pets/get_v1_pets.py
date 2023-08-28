from restrun.core import http
from restrun.core.model import ExtraForbidModel
from restrun.core.request import GetRequest


class GetV1PetsRequestResponseBody(ExtraForbidModel):
    name: str


class GetV1PetsRequest(GetRequest):
    @property
    @classmethod
    def url(cls) -> "http.URL":
        return "https://petstore3.swagger.io/api/v1/pets"

    def get(self) -> "GetV1PetsRequestResponseBody":
        return self._client.get(
            self.url, response_body_type=GetV1PetsRequestResponseBody
        )
