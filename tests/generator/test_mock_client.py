import os
from pathlib import Path

from restrun.config import Config
from restrun.config.v1 import V1Config
from restrun.generator import is_auto_generated
from restrun.generator.client import ClientGenerator
from restrun.generator.context.restrun import RestrunContext
from restrun.generator.mock_client import MockClientGenerator


class TestMockClientGenerator:
    def test_generate(self):
        locals = {}

        context = RestrunContext.from_config(
            Config(
                root=V1Config(
                    name="my",
                    version="1",
                )
            )
        )
        files = [Path(__file__).parent / "client.py"]
        for file in files:
            with open(Path(__file__).parent / "client.py", "w") as file:
                file.write(ClientGenerator().generate(context))

        code = MockClientGenerator().generate(context)

        exec(code, None, locals)

        for file in files:
            os.remove(file)

        assert is_auto_generated(code)
        assert locals["MyMockClient"] is not None
