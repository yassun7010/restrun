from typing import Literal

from pydantic import BaseModel


class V1Config(BaseModel):
    version: Literal["1"]
