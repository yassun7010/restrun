from restrun.generator import is_auto_generated
from restrun.generator.context.restrun import RestrunContext
from restrun.generator.mock_client import MockClientGenerator


class TestMockClientGenerator:
    def test_check_auto_generated(self, restrun_context: RestrunContext) -> None:
        assert is_auto_generated(MockClientGenerator().generate(restrun_context))
