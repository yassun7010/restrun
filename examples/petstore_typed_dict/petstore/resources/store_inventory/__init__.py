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

from . import get_store_inventory


class StoreInventoryResource(get_store_inventory.GetStoreInventory, Resource):
    pass
