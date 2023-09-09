from restrun.core import http
from restrun.core.model import ExtraForbidModel
from restrun.core.operation import GetOperation


class GetV1PetsResponseBody(ExtraForbidModel):
    name: str


class GetV1Pets(GetOperation):
    @classmethod
    def url(cls) -> "http.URL":
        return "https://petstore3.swagger.io/api/v1/pets"

    def get(self) -> "GetV1PetsResponseBody":
        return self._client.get(self.url(), response_body_type=GetV1PetsResponseBody)
