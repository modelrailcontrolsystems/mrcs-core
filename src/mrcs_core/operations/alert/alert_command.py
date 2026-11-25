"""
Created on 19 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

The commands accepted by an AlertNode

{
    "type": "AlertCommand",
    "action": "RESOLVE",
    "response_required": false,
    "kwargs": {
        "id": 1
    }
}
"""

from mrcs_core.operations.alert.alert_action import AlertAction
from mrcs_core.operations.node_command import NodeCommand


# --------------------------------------------------------------------------------------------------------------------

class AlertCommand(NodeCommand[AlertAction]):
    """
    the commands accepted by an AlertNode
    """


    @classmethod
    def action_class(cls) -> type[AlertAction]:
        return AlertAction


    @classmethod
    def construct_RESOLVE(cls, id: int, response_required: bool = True):
        return cls(AlertAction.RESOLVE, response_required=response_required, id=id)


    @classmethod
    def construct_RESOLVE_ALL(cls, response_required: bool = True):
        return cls(AlertAction.RESOLVE_ALL, response_required=response_required)


    @classmethod
    def construct_LIST_UNRESOLVED(cls, response_required: bool = True):
        return cls(AlertAction.LIST_UNRESOLVED, response_required=response_required)


    @classmethod
    def construct_LIST_LATEST(cls, limit: int, response_required: bool = True):
        return cls(AlertAction.LIST_LATEST, response_required=response_required, limit=limit)


    @classmethod
    def construct_DELETE_RESOLVED(cls, response_required: bool = True):
        return cls(AlertAction.DELETE_RESOLVED, response_required=response_required)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, action: AlertAction, response_required: bool = True, **kwargs):
        super().__init__(action, response_required=response_required, **kwargs)
