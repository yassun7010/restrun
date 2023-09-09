from restrun.core import http
from restrun.core.model import ExtraForbidModel
from restrun.core.operation import GetOperation


class GetV1PetsResponseBody(ExtraForbidModel):
    name: str


class GetV1Pets(GetOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/v1/pets"

    def get(self) -> "GetV1PetsResponseBody":
        return self._client.get(self.path, response_body_type=GetV1PetsResponseBody)
