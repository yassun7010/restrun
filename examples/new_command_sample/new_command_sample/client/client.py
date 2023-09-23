#
# Code generated by restrun "0.1.0".
#
# Removing this comment from this file will exclude it from automatic generation target
# and it will not be updated, unless the file contents are empty.
# If you wish to make special modifications to the auto-generated code,
# please remove this comment.
#
# For more information about restrun,
# please refer to https://github.com/yassun7010/restrun .
#
from typing import Literal

from typing_extensions import overload

from restrun.core.client import RestrunClient
from restrun.exceptions import URLNotSupportedError

from ..resources import (
    pet,
    pet_find_by_status,
    pet_find_by_tags,
    pet_pet_id,
    pet_pet_id_upload_image,
    store_inventory,
    store_order,
    store_order_order_id,
    user,
    user_create_with_list,
    user_login,
    user_logout,
    user_username,
)


class NewCommandSampleClient(RestrunClient):
    @overload
    def resource(
        self,
        url: Literal["https://example.com/store/inventory"],
    ) -> store_inventory.StoreInventoryResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/pet/{petId}/uploadImage"],
    ) -> pet_pet_id_upload_image.PetPetIdUploadImageResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/pet/findByTags"],
    ) -> pet_find_by_tags.PetFindByTagsResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/user/{username}"],
    ) -> user_username.UserUsernameResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/user"],
    ) -> user.UserResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/store/order/{orderId}"],
    ) -> store_order_order_id.StoreOrderOrderIdResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/pet/{petId}"],
    ) -> pet_pet_id.PetPetIdResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/user/login"],
    ) -> user_login.UserLoginResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/pet"],
    ) -> pet.PetResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/store/order"],
    ) -> store_order.StoreOrderResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/user/createWithList"],
    ) -> user_create_with_list.UserCreateWithListResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/pet/findByStatus"],
    ) -> pet_find_by_status.PetFindByStatusResource:
        ...

    @overload
    def resource(
        self,
        url: Literal["https://example.com/user/logout"],
    ) -> user_logout.UserLogoutResource:
        ...

    def resource(self, url):
        if url in ["https://example.com/store/inventory"]:
            return store_inventory.StoreInventoryResource(self._client)

        if url in ["https://example.com/pet/{petId}/uploadImage"]:
            return pet_pet_id_upload_image.PetPetIdUploadImageResource(self._client)

        if url in ["https://example.com/pet/findByTags"]:
            return pet_find_by_tags.PetFindByTagsResource(self._client)

        if url in ["https://example.com/user/{username}"]:
            return user_username.UserUsernameResource(self._client)

        if url in ["https://example.com/user"]:
            return user.UserResource(self._client)

        if url in ["https://example.com/store/order/{orderId}"]:
            return store_order_order_id.StoreOrderOrderIdResource(self._client)

        if url in ["https://example.com/pet/{petId}"]:
            return pet_pet_id.PetPetIdResource(self._client)

        if url in ["https://example.com/user/login"]:
            return user_login.UserLoginResource(self._client)

        if url in ["https://example.com/pet"]:
            return pet.PetResource(self._client)

        if url in ["https://example.com/store/order"]:
            return store_order.StoreOrderResource(self._client)

        if url in ["https://example.com/user/createWithList"]:
            return user_create_with_list.UserCreateWithListResource(self._client)

        if url in ["https://example.com/pet/findByStatus"]:
            return pet_find_by_status.PetFindByStatusResource(self._client)

        if url in ["https://example.com/user/logout"]:
            return user_logout.UserLogoutResource(self._client)

        raise URLNotSupportedError(url)
