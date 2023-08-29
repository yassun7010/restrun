from restrun.generator import is_auto_generated_or_empty
from restrun.generator.client_mixins_module import ClientMixinsModuleGenerator
from restrun.generator.context.restrun import RestrunContext


class TestClientMixinsModuleGenerator:
    def test_check_auto_generated(self, restrun_context: RestrunContext) -> None:
        assert is_auto_generated_or_empty(
            ClientMixinsModuleGenerator().generate(restrun_context)
        )
