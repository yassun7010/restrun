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
from restrun.core.resource import Resource

from . import get_pet_pet_id, post_pet_pet_id


class PetPetIdResource(
    get_pet_pet_id.GetPetPetId, post_pet_pet_id.PostPetPetId, Resource
):
    pass
