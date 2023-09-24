from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.context.restrun_context import RestrunContext
from restrun.generator.root_module import RootModuleGenerator


class TestRootModuleGenerator:
    def test_check_auto_generated(
        self,
        config: Config,
        restrun_context: RestrunContext,
    ) -> None:
        assert is_auto_generated_or_empty(
            RootModuleGenerator().generate(
                config,
                restrun_context,
            )
        )
