"""
Created on 6 Dec 2025

@author: Bruno Beloff (bbeloff@me.com)

The MRCS local web server base URL configuration

{
    "host": "127.0.0.1",
    "port": 8000,
    "is_secure": false
}

https://en.wikipedia.org/wiki/URL
"""

from collections import OrderedDict

from mrcs_core.data.json import MultiPersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Server(MultiPersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "server_conf.json"


    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))
        return cls.conf_dir(), filename


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, name=None):
        if not jdict:
            return None

        host = jdict.get('host')
        port = jdict.get('port')
        is_secure = jdict.get('is_secure')

        return cls(host, port, is_secure, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host: str, port: int, is_secure: bool, name=None):
        super().__init__(name)

        self.__host = host
        self.__port = port
        self.__is_secure = is_secure


    # ----------------------------------------------------------------------------------------------------------------

    def url(self, path='/'):
        if not path.startswith('/'):
            raise ValueError(path)

        return self.base_url + path


    @property
    def base_url(self):
        scheme = 'https' if self.is_secure else 'http'
        return f'{scheme}://{self.authority}'


    @property
    def authority(self):
        port = '' if self.port == 80 else ':' + str(self.__port)
        return f'{self.host}{port}'


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['host'] = self.host
        jdict['port'] = self.port
        jdict['is_secure'] = self.is_secure

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def host(self):
        return self.__host


    @property
    def port(self):
        return self.__port


    @property
    def is_secure(self):
        return self.__is_secure


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Server:{{name:{self.name}, host:{self.host}, port:{self.port}, is_secure:{self.is_secure}}}'
