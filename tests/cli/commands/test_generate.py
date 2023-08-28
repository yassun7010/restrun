from restrun.cli.commands.generate import GenerateTarget, get_targets

ALL_TARGETS = set(
    [
        GenerateTarget.CLIENT,
        GenerateTarget.RESOURCE,
    ]
)


class TestGetTargets:
    def test_get_targets_default(self) -> None:
        assert get_targets([GenerateTarget.ALL]) == ALL_TARGETS

    def test_get_targets_with_all(self) -> None:
        assert get_targets([GenerateTarget.ALL, GenerateTarget.CLIENT]) == ALL_TARGETS

    def test_get_targets_without_all(self) -> None:
        targets = [GenerateTarget.CLIENT, GenerateTarget.RESOURCE]
        assert get_targets(targets) == set(targets)
