from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.context.restrun_context import RestrunContext
from restrun.generator.mock_client import MockClientGenerator
from restrun.generator.context.resources_context import ResourcesContext


class TestMockClientGenerator:
    def test_check_auto_generated(
        self,
        config: Config,
        restrun_context: RestrunContext,
        resources_context: ResourcesContext,
    ) -> None:
        assert is_auto_generated_or_empty(
            MockClientGenerator().generate(
                config,
                restrun_context,
                resources_context,
            )
        )
