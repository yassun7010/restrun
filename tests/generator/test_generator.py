from pathlib import Path
from textwrap import dedent

from restrun.core.operation import GetOperation, PatchOperation, PostOperation
from restrun.generator import find_classes_from_code
from tests.conftest import tempfilepath


def test_find_classes_from_code_when_single_class_search() -> None:
    with tempfilepath(Path(__file__).parent) as source:
        with open(source, "w") as file:
            file.write(
                dedent(
                    """
                    from restrun.core.request import GetOperation

                    class A(GetOperation):
                        pass
                    """
                )
            )

        reuqst_class_map = find_classes_from_code(source, GetOperation)
        assert len(reuqst_class_map[GetOperation]) == 1


def test_find_classes_from_code_when_multi_classes_search() -> None:
    with tempfilepath(Path(__file__).parent) as source:
        with open(source, "w") as file:
            file.write(
                dedent(
                    """
                    from restrun.core.request import GetOperation, PostOperation

                    class A(GetOperation):
                        pass

                    class B(PostOperation):
                        pass
                    """
                )
            )

        reuqst_class_map = find_classes_from_code(
            source, GetOperation, PostOperation, PatchOperation
        )
        assert len(reuqst_class_map[GetOperation]) == 1
        assert len(reuqst_class_map[PostOperation]) == 1
        assert len(reuqst_class_map[PatchOperation]) == 0
