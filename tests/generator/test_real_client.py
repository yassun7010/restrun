from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.context.restrun import RestrunContext
from restrun.generator.real_client import RealClientGenerator


class TestRealClientGenerator:
    def test_check_auto_generated(
        self, config: Config, restrun_context: RestrunContext
    ) -> None:
        assert is_auto_generated_or_empty(
            RealClientGenerator().generate(config, restrun_context)
        )
