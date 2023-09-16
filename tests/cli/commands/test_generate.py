from restrun.cli.app import App


class TestGetTargets:
    def test_petstore_example(self) -> None:
        App.run(
            [
                "--verbose",
                "--config",
                "examples/petstore/restrun.yml",
                "generate",
            ]
        )
