from restrun.cli.app import App


class TestGetTargets:
    def test_petstore_pydantic_example(self) -> None:
        App.run(
            [
                "--verbose",
                "--config",
                "examples/petstore_pydantic/restrun.yml",
                "generate",
            ]
        )
