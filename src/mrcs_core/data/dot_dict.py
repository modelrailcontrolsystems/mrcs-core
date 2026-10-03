"""
Created on 2 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

An OrderedDict whose contents can be accessed using dot path notation
"""

from collections import OrderedDict


# --------------------------------------------------------------------------------------------------------------------

class DotDict(OrderedDict):
    """
    an OrderedDict whose contents can be accessed using dot path notation
    """


    @classmethod
    def path(cls, *nodes) -> str:
        return '.'.join(nodes)


    @classmethod
    def node(cls, path: str | None, index: int) -> str | None:
        if path is None or path == '*':
            return None

        nodes = path.split('.')
        if index < len(nodes):
            return nodes[index]

        return None


    @classmethod
    def nodes(cls, path: str | None) -> list[str] | None:
        if path is None or path == '*':
            return None

        return path.split('.')


    # ----------------------------------------------------------------------------------------------------------------

    def item(self, path: str | None):
        nodes = self.nodes(path)

        if nodes is None:
            return self

        traversed = []
        item = self

        for node in nodes:
            try:
                traversed.append(node)
                item = item[node]
            except (KeyError, TypeError):
                raise KeyError(self.path(*traversed))

        return item
