from restrun.generator import is_auto_generated_or_empty
from restrun.generator.client_module import ClientModuleGenerator
from restrun.generator.context.restrun import RestrunContext


class TestClientModuleGenerator:
    def test_check_auto_generated(self, restrun_context: RestrunContext) -> None:
        assert is_auto_generated_or_empty(
            ClientModuleGenerator().generate(restrun_context)
        )
