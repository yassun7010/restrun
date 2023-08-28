from restrun.generator import is_auto_generated
from restrun.generator.context.restrun import RestrunContext
from restrun.generator.real_client import RealClientGenerator


class TestRealClientGenerator:
    def test_check_auto_generated(self, restrun_context: RestrunContext) -> None:
        assert is_auto_generated(RealClientGenerator().generate(restrun_context))
