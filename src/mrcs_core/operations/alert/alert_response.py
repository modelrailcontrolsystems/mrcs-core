"""
Created on 21 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

An ACK / NACK + data in response to an ActionCommand

{
    "type": "AlertResponse",
    "action": "RESOLVE",
    "error": "this is an error"
}

{
    "type": "AlertResponse",
    "action": "RESOLVE",
    "payload": {
        "type": "AlertCommand",
        "action": "CLEAR_RESOLVED",
        "response_required": true,
        "kwargs": {}
    }
}
"""

from typing import Any

from mrcs_core.operations.alert.alert_action import AlertAction
from mrcs_core.operations.node_response import NodeResponse


# --------------------------------------------------------------------------------------------------------------------

class AlertResponse(NodeResponse[AlertAction]):
    """
    an ACK / NACK + data in response to an ActionCommand
    """


    @classmethod
    def action_class(cls) -> type[AlertAction]:
        return AlertAction


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, action: AlertAction, error: str | None = None, payload: Any = None):
        super().__init__(action, error=error, payload=payload)
