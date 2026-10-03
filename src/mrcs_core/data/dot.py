"""
Created on 2 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Utilities supporting dot-path strings
"""


# --------------------------------------------------------------------------------------------------------------------

class Dot(object):
    """
    Utilities supporting dot-path strings
    """


    @staticmethod
    def path(*nodes) -> str:
        return '.'.join([str(node) for node in nodes])


    @staticmethod
    def node(path: str | None, index: int) -> str | None:
        if path is None or path == '*':
            return None

        nodes = path.split('.')
        if index < len(nodes):
            return nodes[index]

        return None


    @staticmethod
    def nodes(path: str | None) -> list[str]:
        if path is None or path == '*':
            return []

        return path.split('.')
