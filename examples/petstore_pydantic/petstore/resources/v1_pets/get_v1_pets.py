from restrun.core import http
from restrun.core.model import ExtraForbidModel
from restrun.core.operation import GetOperation


class GetV1PetsRequestResponseBody(ExtraForbidModel):
    name: str


class GetV1PetsRequest(GetOperation):
    @classmethod
    @property
    def path(cls) -> "http.URL":
        return "/v1/pets"

    def get(self) -> "GetV1PetsRequestResponseBody":
        return self._client.get(self.path, response_type=GetV1PetsRequestResponseBody)
