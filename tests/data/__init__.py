import json
from pathlib import Path

from restrun.openapi.openapi import OpenAPI

DATA_DIR = Path(__file__).parent


def load_openapi(filename: str) -> OpenAPI:
    with open(DATA_DIR / "openapi" / filename) as file:
        return OpenAPI.model_validate(json.load(file))
