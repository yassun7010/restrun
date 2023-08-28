from pathlib import Path
from textwrap import dedent

from restrun.core.request import GetRequest, PatchRequest, PostRequest
from restrun.generator import find_classes_from_code
from tests.conftest import tempfilepath


def test_find_classes_from_code_when_single_class_search() -> None:
    with tempfilepath(Path(__file__).parent) as source:
        with open(source, "w") as file:
            file.write(
                dedent(
                    """
                    from restrun.core.request import GetRequest

                    class A(GetRequest):
                        pass
                    """
                )
            )

        reuqst_class_map = find_classes_from_code(source, GetRequest)
        assert len(reuqst_class_map[GetRequest]) == 1


def test_find_classes_from_code_when_multi_classes_search() -> None:
    with tempfilepath(Path(__file__).parent) as source:
        with open(source, "w") as file:
            file.write(
                dedent(
                    """
                    from restrun.core.request import GetRequest, PostRequest

                    class A(GetRequest):
                        pass

                    class B(PostRequest):
                        pass
                    """
                )
            )

        reuqst_class_map = find_classes_from_code(
            source, GetRequest, PostRequest, PatchRequest
        )
        assert len(reuqst_class_map[GetRequest]) == 1
        assert len(reuqst_class_map[PostRequest]) == 1
        assert len(reuqst_class_map[PatchRequest]) == 0
