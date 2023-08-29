from restrun.generator import is_auto_generated_or_empty
from restrun.generator.context.restrun import RestrunContext
from restrun.generator.resources_module import ResourcesModuleGenerator


class TestResourcesModuleGenerator:
    def test_check_auto_generated(self, restrun_context: RestrunContext) -> None:
        assert is_auto_generated_or_empty(
            ResourcesModuleGenerator().generate(restrun_context)
        )
