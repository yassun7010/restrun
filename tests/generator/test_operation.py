from restrun.config import Config
from restrun.generator import is_auto_generated_or_empty
from restrun.generator.context.operation_context import (
    OperationContext,
    PythonResponseJsonBody,
)
from restrun.generator.context.restrun_context import RestrunContext
from restrun.generator.operation import generate_operation
from restrun.openapi.schema import PythonObject


class TestGenerateOperation:
    def test_check_auto_generated(
        self, config: Config, restrun_context: RestrunContext
    ) -> None:
        assert is_auto_generated_or_empty(
            generate_operation(
                config,
                restrun_context,
                OperationContext(
                    class_name="GetPets",
                    path_name="pets",
                    method="GET",
                    urls=["https://examples.com/pets"],
                    response_json_body=PythonResponseJsonBody(
                        class_name="GetPetsResponse",
                        data_type=PythonObject(
                            type_name="GetPetsJsonResponse", properties={}
                        ),
                    ),
                ),
            )
        )
