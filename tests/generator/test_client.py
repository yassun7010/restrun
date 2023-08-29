from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.client import ClientGenerator
from restrun.generator.context.restrun import RestrunContext


class TestClientGenerator:
    def test_check_auto_generated(
        self, config: Config, restrun_context: RestrunContext
    ) -> None:
        assert is_auto_generated_or_empty(
            ClientGenerator().generate(config, restrun_context)
        )

    def test_generate(self, config: Config, restrun_context: RestrunContext) -> None:
        locals = {}

        code = ClientGenerator().generate(config, restrun_context)

        exec(code, None, locals)

        assert is_auto_generated_or_empty(code)
        assert locals["MyClient"] is not None
