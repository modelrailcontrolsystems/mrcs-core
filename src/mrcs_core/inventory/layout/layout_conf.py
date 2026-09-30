"""
Created on 29 Sep 2026

@author: Bruno Beloff (bbeloff@me.com)

Persists the selected layout conf.

If there is only one layout, then the layout conf need not be set - a sole layout is by default the selected layout.
"""

from collections import OrderedDict

from mypy.types import Any

from mrcs_core.data.json import PersistentJSONable
from mrcs_core.inventory.layout.layout import Layout


# --------------------------------------------------------------------------------------------------------------------

class LayoutConf(PersistentJSONable):
    """
    persists the selected layout conf
    """

    __FILENAME = "layout_conf.json"


    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load_selected_layout(cls, manager) -> Layout | None:
        layouts = Layout.list(manager)

        conf = cls.load(manager)
        if conf is not None:
            if conf.selected_layout not in layouts:
                raise KeyError(f'Selected layout is set to {conf.selected_layout} but this layout is not known.')

            return Layout.load(manager, name=conf.selected_layout)

        if len(layouts) == 1:
            return Layout.load(manager, name=layouts[0])

        return None


    @classmethod
    def construct_from_jdict(cls, jdict) -> LayoutConf | None:
        if jdict is None:
            return None

        selected_layout = jdict.get('selected')

        return cls(selected_layout)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, selected_layout: str):
        super().__init__()

        self.__selected_layout = selected_layout


    def __eq__(self, other: Any):
        try:
            return self.selected_layout == other.selected_layout
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['selected'] = self.selected_layout

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def selected_layout(self):
        return self.__selected_layout


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'LayoutConf:{{selected_layout:{self.selected_layout}}}'
