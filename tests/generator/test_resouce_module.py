from restrun.generator import is_auto_generated
from restrun.generator.context.resource import ResourceContext
from restrun.generator.context.restrun import RestrunContext
from restrun.generator.resource_module import ResourceModuleGenerator


class TestResourceModuleGenerator:
    def test_check_auto_generated(
        self, restrun_context: RestrunContext, resource_context: ResourceContext
    ) -> None:
        assert is_auto_generated(
            ResourceModuleGenerator().generate(
                restrun_context,
                resource_context,
            )
        )
