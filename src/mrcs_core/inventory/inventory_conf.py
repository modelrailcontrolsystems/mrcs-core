"""
Created on 10 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Persists the selected inventory conf.

If there is only one inventory, then the inventory conf need not be set - a sole inventory is by default the selected
inventory.
"""

from collections import OrderedDict

from mypy.types import Any

from mrcs_core.data.json import PersistentJSONable
from mrcs_core.inventory.inventory import Inventory


# --------------------------------------------------------------------------------------------------------------------

class InventoryConf(PersistentJSONable):
    """
    persists the selected inventory conf
    """

    __FILENAME = "inventory_conf.json"


    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load_selected_inventory(cls, manager) -> Inventory | None:
        inventories = Inventory.list(manager)

        conf = cls.load(manager)
        if conf is not None:
            if conf.selected_inventory not in inventories:
                raise KeyError(f'Selected inventory is set to {conf.selected_inventory} '
                               f'but this inventory is not present.')

            return Inventory.load(manager, name=conf.selected_inventory)

        if len(inventories) == 1:
            return Inventory.load(manager, name=inventories[0])

        return None


    @classmethod
    def construct_from_jdict(cls, jdict) -> InventoryConf | None:
        if jdict is None:
            return None

        selected_inventory = jdict.get('selected')

        return cls(selected_inventory)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, selected_inventory: str):
        super().__init__()

        self.__selected_inventory = selected_inventory


    def __eq__(self, other: Any):
        try:
            return self.selected_inventory == other.selected_inventory
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['selected'] = self.selected_inventory

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def selected_inventory(self):
        return self.__selected_inventory


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'InventoryConf:{{selected_inventory:{self.selected_inventory}}}'
