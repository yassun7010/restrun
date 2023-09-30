from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.client import generate_client
from restrun.generator.context.resources_context import ResourcesContext
from restrun.generator.context.restrun_context import RestrunContext


class TestGenerateClient:
    def test_check_auto_generated(
        self,
        config: Config,
        restrun_context: RestrunContext,
        resources_context: ResourcesContext,
    ) -> None:
        assert is_auto_generated_or_empty(
            generate_client(
                config,
                restrun_context,
                resources_context,
            )
        )

    def test_generate(
        self,
        config: Config,
        restrun_context: RestrunContext,
        resources_context: ResourcesContext,
    ) -> None:
        locals = {}

        code = generate_client(
            config,
            restrun_context,
            resources_context,
        )

        exec(code, None, locals)

        assert locals["TestProjectClient"] is not None
