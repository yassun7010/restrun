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
from typing import Literal, Self, overload

from typing_extensions import override

from restrun.core.client import RestrunMockClient
from restrun.exceptions import RestrunError

from ..resources.pet import post_pet, put_pet
from ..resources.pet_find_by_status import get_pet_find_by_status
from ..resources.pet_find_by_tags import get_pet_find_by_tags
from ..resources.pet_pet_id import get_pet_pet_id, post_pet_pet_id
from ..resources.pet_pet_id_upload_image import post_pet_pet_id_upload_image
from ..resources.store_inventory import get_store_inventory
from ..resources.store_order import post_store_order
from ..resources.store_order_order_id import get_store_order_order_id
from ..resources.user import post_user
from ..resources.user_create_with_list import post_user_create_with_list
from ..resources.user_login import get_user_login
from ..resources.user_logout import get_user_logout
from ..resources.user_username import get_user_username, put_user_username
from ..resources.v1_pets import get_v1_pets
from .client import PetstoreClient
from .mixins import bearer_token_login_mixin


class PetstoreMockClient(
    bearer_token_login_mixin.MockBearTokenLoginMixin, RestrunMockClient, PetstoreClient
):
    @overload
    def inject_get_response_body(
        self,
        url: Literal["https://petstore3.com/store/inventory"],
        response_body: get_store_inventory.GetStoreInventoryResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_get_response_body(
        self,
        url: Literal["https://petstore3.com/pet/findByTags"],
        response_body: get_pet_find_by_tags.GetPetFindByTagsResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_get_response_body(
        self,
        url: Literal["https://petstore3.com/user/{username}"],
        response_body: get_user_username.GetUserUsernameResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_get_response_body(
        self,
        url: Literal["https://petstore3.com/store/order/{orderId}"],
        response_body: get_store_order_order_id.GetStoreOrderOrderIdResponseBody
        | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_get_response_body(
        self,
        url: Literal["https://petstore3.com/pet/{petId}"],
        response_body: get_pet_pet_id.GetPetPetIdResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_get_response_body(
        self,
        url: Literal["https://petstore3.com/user/login"],
        response_body: get_user_login.GetUserLoginResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_get_response_body(
        self,
        url: Literal["https://petstore3.com/v1/pets"],
        response_body: get_v1_pets.GetV1PetsRequestResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_get_response_body(
        self,
        url: Literal["https://petstore3.com/pet/findByStatus"],
        response_body: get_pet_find_by_status.GetPetFindByStatusResponseBody
        | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_get_response_body(
        self,
        url: Literal["https://petstore3.com/user/logout"],
        response_body: get_user_logout.GetUserLogoutResponseBody | RestrunError,
    ) -> "Self":
        ...

    @override
    def inject_get_response_body(self, url, response_body) -> "Self":
        self._client.inject_get_response_body(url, response_body)

        return self

    @overload
    def inject_post_response_body(
        self,
        url: Literal["https://petstore3.com/pet/{petId}/uploadImage"],
        response_body: post_pet_pet_id_upload_image.PostPetPetIdUploadImageResponseBody
        | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_post_response_body(
        self,
        url: Literal["https://petstore3.com/user"],
        response_body: post_user.PostUserResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_post_response_body(
        self,
        url: Literal["https://petstore3.com/pet/{petId}"],
        response_body: post_pet_pet_id.PostPetPetIdResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_post_response_body(
        self,
        url: Literal["https://petstore3.com/pet"],
        response_body: post_pet.PostPetResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_post_response_body(
        self,
        url: Literal["https://petstore3.com/store/order"],
        response_body: post_store_order.PostStoreOrderResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_post_response_body(
        self,
        url: Literal["https://petstore3.com/user/createWithList"],
        response_body: post_user_create_with_list.PostUserCreateWithListResponseBody
        | RestrunError,
    ) -> "Self":
        ...

    @override
    def inject_post_response_body(self, url, response_body) -> "Self":
        self._client.inject_post_response_body(url, response_body)

        return self

    @overload
    def inject_put_response_body(
        self,
        url: Literal["https://petstore3.com/user/{username}"],
        response_body: put_user_username.PutUserUsernameResponseBody | RestrunError,
    ) -> "Self":
        ...

    @overload
    def inject_put_response_body(
        self,
        url: Literal["https://petstore3.com/pet"],
        response_body: put_pet.PutPetResponseBody | RestrunError,
    ) -> "Self":
        ...

    @override
    def inject_put_response_body(self, url, response_body) -> "Self":
        self._client.inject_put_response_body(url, response_body)

        return self
