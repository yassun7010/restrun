from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.context.resource_context import ResourceContext
from restrun.generator.context.restrun_context import RestrunContext
from restrun.generator.resource_module import generate_resource_module


class TestGenerateResourceModule:
    def test_check_auto_generated(
        self,
        config: Config,
        restrun_context: RestrunContext,
        resource_context: ResourceContext,
    ) -> None:
        assert is_auto_generated_or_empty(
            generate_resource_module(
                config,
                restrun_context,
                resource_context,
            )
        )
