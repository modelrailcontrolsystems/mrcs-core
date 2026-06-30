"""
Created on 28 Jun 2026

@author: Bruno Beloff (bbeloff@me.com)

Networking configuration of a DCC control router

{
    "ip_address": "192.168.1.111",
    "port": 21105,
    "timeout": 1.2,
    "subscription": {
        "flags": [
            "CAN_DETECTOR",
            "TRACK",
            "X_LOCO_INFO_ALL"
        ]
    }
}
"""

from collections import OrderedDict

from mrcs_core.data.json import PersistentJSONable
from mrcs_core.equipment.control_router.control_router_subscription import ControlRouterSubscription
from mrcs_core.sys.ipv4_address import IPv4Address


# --------------------------------------------------------------------------------------------------------------------

class ControlRouterConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "control_router_conf.json"


    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        ip_address = IPv4Address.construct(jdict.get('ip_address'))
        port = jdict.get('port')
        timeout = jdict.get('timeout')
        subscription = ControlRouterSubscription.construct_from_jdict(jdict.get('subscription'))

        return cls(ip_address, port, timeout, subscription)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ip_address: IPv4Address, port: int, timeout: float, subscription: ControlRouterSubscription):
        super().__init__()

        self.__ip_address = ip_address
        self.__port = port
        self.__timeout = timeout
        self.__subscription = subscription


    def __eq__(self, other):
        try:
            return (self.ip_address == other.ip_address and self.port == other.port and
                    self.timeout == other.timeout and self.subscription == other.subscription)
        except (AttributeError, TypeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['ip_address'] = self.ip_address.dot_decimal
        jdict['port'] = self.port
        jdict['timeout'] = self.timeout
        jdict['subscription'] = self.subscription

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ip_address(self):
        return self.__ip_address


    @ip_address.setter
    def ip_address(self, dot_decimal: str):
        self.__ip_address = IPv4Address.construct(dot_decimal)


    @property
    def port(self):
        return self.__port


    @port.setter
    def port(self, port: int):
        self.__port = port


    @property
    def timeout(self):
        return self.__timeout


    @timeout.setter
    def timeout(self, timeout: float):
        self.__timeout = timeout


    @property
    def subscription(self):
        return self.__subscription


    @subscription.setter
    def subscription(self, subscription: ControlRouterSubscription):
        self.__subscription = subscription


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'ControlRouterConf:{{ip_address:{self.ip_address}, port:{self.port}, timeout:{self.timeout}, '
                f'subscription:{self.subscription}}}')
