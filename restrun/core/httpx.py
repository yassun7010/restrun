from typing import (
    Any,
    Callable,
    Mapping,
    NotRequired,
    Type,
    TypedDict,
)

import httpx
import pydantic
from typing_extensions import override

from restrun.core.http import (
    URL,
    Headers,
    Method,
    QuryParameters,
    RequestJsonBody,
    ResponseModelBody,
)
from restrun.core.request import RequestRealClient
from restrun.exception import (
    ResponseJsonBodyParseError,
    ResponseJsonBodyValidationError,
    ResponseStatusCodeError,
)


class HttpxClientArguments(TypedDict):
    auth: NotRequired[httpx._types.AuthTypes | None]
    params: NotRequired[httpx._types.QueryParamTypes | None]
    headers: NotRequired[httpx._types.HeaderTypes | None]
    cookies: NotRequired[httpx._types.CookieTypes | None]
    verify: NotRequired[httpx._types.VerifyTypes]
    cert: NotRequired[httpx._types.CertTypes | None]
    http1: NotRequired[bool]
    http2: NotRequired[bool]
    proxies: NotRequired[httpx._types.ProxiesTypes | None]
    mounts: NotRequired[Mapping[str, httpx.BaseTransport] | None]
    timeout: NotRequired[httpx._types.TimeoutTypes]
    follow_redirects: NotRequired[bool]
    limits: NotRequired[httpx.Limits]
    max_redirects: NotRequired[int]
    event_hooks: NotRequired[Mapping[str, list[httpx._client.EventHook]]]
    base_url: NotRequired[httpx._types.URLTypes]
    transport: NotRequired[httpx.BaseTransport | None]
    app: NotRequired[Callable[..., Any] | None]
    trust_env: NotRequired[bool]
    default_encoding: NotRequired[str | Callable[[bytes], str]]


class RequestHttpxClient(RequestRealClient):
    def __init__(
        self,
        httpx_client: httpx.Client,
        *,
        auth: httpx._auth.Auth | None,
    ) -> None:
        self._httpx_client = httpx_client
        self._auth = auth

    @override
    def get(
        self,
        *,
        url: URL,
        response_body_type: Type[ResponseModelBody],
        query: QuryParameters | None = None,
    ) -> ResponseModelBody:
        method = "GET"
        response = self._httpx_client.request(
            method=method,
            url=url,
            auth=self._auth,
            params=remove_none_field(query),
        )

        if response.is_error:
            raise ResponseStatusCodeError(
                method=method,
                url=url,
                status_code=response.status_code,
                response_body=response.content,
            )
        return parse_json_response(
            method,
            url,
            response,
            response_body_type,
        )

    @override
    def post(
        self,
        *,
        url: URL,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        method = "POST"
        response = self._httpx_client.request(
            method=method,
            url=url,
            auth=self._auth,
            params=remove_none_field(query),
            json=remove_none_field(body),
            headers=headers,
        )

        if response.is_error:
            raise ResponseStatusCodeError(
                method=method,
                url=url,
                status_code=response.status_code,
                response_body=response.content,
            )
        return parse_json_response(
            method,
            url,
            response,
            response_body_type,
        )

    @override
    def put(
        self,
        *,
        url: URL,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        method = "PUT"
        response = self._httpx_client.request(
            method=method,
            url=url,
            auth=self._auth,
            params=remove_none_field(query),
            json=remove_none_field(body),
            headers=headers,
        )

        if response.is_error:
            raise ResponseStatusCodeError(
                method=method,
                url=url,
                status_code=response.status_code,
                response_body=response.content,
            )
        return parse_json_response(
            method,
            url,
            response,
            response_body_type,
        )

    @override
    def patch(
        self,
        *,
        url: URL,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        method = "PATCH"
        response = self._httpx_client.request(
            method=method,
            url=url,
            auth=self._auth,
            params=remove_none_field(query),
            json=remove_none_field(body),
            headers=headers,
        )

        if response.is_error:
            raise ResponseStatusCodeError(
                method=method,
                url=url,
                status_code=response.status_code,
                response_body=response.content,
            )
        return parse_json_response(
            method,
            url,
            response,
            response_body_type,
        )

    @override
    def delete(
        self,
        *,
        url: URL,
        response_body_type: Type[ResponseModelBody],
        headers: Headers | None = None,
        query: QuryParameters | None = None,
        body: RequestJsonBody | None = None,
    ) -> ResponseModelBody:
        method = "DELETE"
        response = self._httpx_client.request(
            method=method,
            url=url,
            auth=self._auth,
            params=remove_none_field(query),
            headers=headers,
            json=remove_none_field(body),
        )

        if response.is_error:
            raise ResponseStatusCodeError(
                method=method,
                url=url,
                status_code=response.status_code,
                response_body=response.content,
            )
        return parse_json_response(
            method,
            url,
            response,
            response_body_type,
        )


def parse_json_response(
    method: Method,
    url: URL,
    response: httpx.Response,
    response_body_type: Type[ResponseModelBody],
) -> ResponseModelBody:
    if response.content == b"":
        data: dict = {}
    else:
        try:
            data = response.json()

        except ValueError:
            raise ResponseJsonBodyParseError(
                method,
                url,
                response.content,
            )

    try:
        return response_body_type(**data)

    except pydantic.ValidationError as error:
        raise ResponseJsonBodyValidationError(method, url, data, error)


def remove_none_field(data: dict | None) -> dict | None:
    if data is None:
        return None

    return {
        k: remove_none_field(v) if isinstance(v, dict) else v
        for k, v in data.items()
        if v is not None
    }
