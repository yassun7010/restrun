from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from restrun.generator import GeneratedPythonCode
    from restrun.generator.context import Context


class ClientGenerator:
    def generate(self, context: "Context") -> "GeneratedPythonCode":
        ...
