from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.context.operation_context import (
    OperationContext,
    PythonResponseJsonBody,
)
from restrun.generator.context.restrun_context import RestrunContext
from restrun.generator.get_operation import GetOperationGenerator
from restrun.openapi.schema import PythonObject


class TestOperationGenerator:
    def test_check_auto_generated(
        self, config: Config, restrun_context: RestrunContext
    ) -> None:
        assert is_auto_generated_or_empty(
            GetOperationGenerator().generate(
                config,
                restrun_context,
                OperationContext(
                    class_name="GetPets",
                    method="GET",
                    url="h/pets",
                    response_json_body=PythonResponseJsonBody(
                        class_name="GetPetsResponse",
                        data_type=PythonObject(
                            class_name="GetPetsJsonResponse", properties={}
                        ),
                    ),
                ),
            )
        )
