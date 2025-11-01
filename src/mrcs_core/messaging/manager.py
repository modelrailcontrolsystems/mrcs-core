"""
Created on 1 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A utility for listing message queues
Note that queues should be deleted using messaging clients.

https://www.rabbitmq.com/docs/http-api-reference
https://stackoverflow.com/questions/4287941/how-can-i-list-or-discover-queues-on-a-rabbitmq-exchange-using-python
"""

import requests

from mrcs_core.messaging.queue import Queue
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class Manager(object):
    """
    classdocs
    """

    __DEFAULT_HOST = 'localhost'
    __DEFAULT_PORT = 15672

    __DEFAULT_USERNAME = 'guest'
    __DEFAULT_PASSWORD = 'guest'

    __DEFAULT_VIRTUAL_HOST = ''

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, host=None, port=None, username=None, password=None):
        mgr_host = cls.__DEFAULT_HOST if host is None else host
        mgr_port = cls.__DEFAULT_PORT if port is None else port

        mgr_username = cls.__DEFAULT_USERNAME if username is None else username
        mgr_password = cls.__DEFAULT_PASSWORD if password is None else password

        return cls(mgr_host, mgr_port, mgr_username, mgr_password)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, port, username, password):
        """
        Constructor
        """
        self.__host = host
        self.__port = port

        self.__username = username
        self.__password = password

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def list_queues(self):
        url = f'{self.__base_url()}/api/queues/{self.__DEFAULT_VIRTUAL_HOST}'
        response = requests.get(url, auth=(self.username, self.password))

        queues = [Queue.construct_from_jdict(q) for q in response.json()]

        return queues


    def __base_url(self):
        return f'http://{self.host}:{self.port}'


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def host(self):
        return self.__host


    @property
    def port(self):
        return self.__port


    @property
    def username(self):
        return self.__username


    @property
    def password(self):
        return self.__password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Manager:{{host:{self.host}, port:{self.port}, username:{self.username}, password:{self.password}}}'
