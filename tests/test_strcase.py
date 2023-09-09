import pytest

from restrun.strcase import class_name, module_name


class TestModuleName:
    @pytest.mark.parametrize(
        "path_name, expected",
        [
            ("foo/bar", "foo_bar"),
            ("/foo/bar/baz", "foo_bar_baz"),
            ("/pets/{pet_id}", "pets_pet_id"),
            ("/pets/{pet_id}/import", "pets_pet_id_import"),
        ],
    )
    def test_module_name(self, path_name: str, expected: str) -> None:
        assert module_name(path_name) == expected


class TestClassName:
    @pytest.mark.parametrize(
        "path_name, expected",
        [
            ("foo/bar", "FooBar"),
            ("/foo/bar/baz", "FooBarBaz"),
            ("/pets/{pet_id}", "PetsPetId"),
            ("/pets/{pet_id}/import", "PetsPetIdImport"),
        ],
    )
    def test_class_name(self, path_name: str, expected: str) -> None:
        assert class_name(path_name) == expected
