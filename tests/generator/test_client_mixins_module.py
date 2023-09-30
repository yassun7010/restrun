from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.client_mixins_module import generate_client_mixin_module
from restrun.generator.context.resources_context import ResourcesContext
from restrun.generator.context.restrun_context import RestrunContext


class TestGenerateClientMixinModule:
    def test_check_auto_generated(
        self,
        config: Config,
        restrun_context: RestrunContext,
        resources_context: ResourcesContext,
    ) -> None:
        assert is_auto_generated_or_empty(
            generate_client_mixin_module(
                config,
                restrun_context,
                resources_context,
            )
        )
