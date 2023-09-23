import json

from pathlib import Path

from restrun.openapi.openapi import OpenAPI


def load_openapi(filename: str) -> OpenAPI:
    with open(Path(__file__).parent / filename) as file:
        return OpenAPI.model_validate(json.load(file))
