from restrun.generator import is_auto_generated
from restrun.generator.client_module import ClientModuleGenerator
from restrun.generator.context.restrun import RestrunContext


class TestClientModuleGenerator:
    def test_check_auto_generated(self, restrun_context: RestrunContext) -> None:
        assert is_auto_generated(ClientModuleGenerator().generate(restrun_context))
