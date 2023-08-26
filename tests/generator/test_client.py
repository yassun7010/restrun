from restrun.config import Config
from restrun.config.v1 import V1Config
from restrun.generator import is_auto_generated
from restrun.generator.client import ClientGenerator
from restrun.generator.context import Context


class TestClientGenerator:
    def test_generate(self):
        locals = {}

        context = Context.from_config(
            Config(
                root=V1Config(
                    name="my",
                    version="1",
                )
            )
        )

        code = ClientGenerator().generate(context)

        exec(code, None, locals)

        assert is_auto_generated(code)
        assert locals["MyClient"] is not None
