"""
Created on 2 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

An exchange hosted by RabbitMQ

{
    "name": "topic_logs",
    "type": "topic",
    "durable": false,
    "internal": false,
    "auto_delete": false,
    "message_stats": {
        "publish_in": 7,
        "publish_out": 10
    }
}

https://www.rabbitmq.com/docs/http-api-reference
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Exchange(JSONable):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        name = jdict.get('name')
        exchange_type = jdict.get('type')
        durable = jdict.get('durable')
        internal = jdict.get('internal')
        auto_delete = jdict.get('auto_delete')

        message_stats = MessageStats.construct_from_jdict(jdict.get('message_stats'))

        return cls(name, exchange_type, durable, internal, auto_delete, message_stats)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, exchange_type, durable, internal, auto_delete, message_stats):
        """
        Constructor
        """
        super().__init__()

        self.__name = name                                          # string
        self.__exchange_type = exchange_type                        # string
        self.__durable = durable                                    # bool
        self.__internal = internal                                  # bool
        self.__auto_delete = auto_delete                            # bool

        self.__message_stats = message_stats                        # MessageStats


    def __eq__(self, other):
        return (self.name == other.name and self.exchange_type == other.exchange_type and
                self.durable == other.durable and self.internal == other.internal and
                self.auto_delete == other.auto_delete and self.message_stats == other.message_stats)


    def __lt__(self, other):
        return self.name < other.name           # names are unique within an exchange


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['name'] = self.name
        jdict['type'] = self.exchange_type
        jdict['durable'] = self.durable
        jdict['internal'] = self.internal
        jdict['auto_delete'] = self.auto_delete

        jdict['message_stats'] = self.message_stats

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def exchange_type(self):
        return self.__exchange_type


    @property
    def durable(self):
        return self.__durable


    @property
    def internal(self):
        return self.__internal


    @property
    def auto_delete(self):
        return self.__auto_delete


    @property
    def message_stats(self):
        return self.__message_stats


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'Exchange:{{name:{self.name}, exchange_type:{self.exchange_type}, durable:{self.durable}, '
                f'internal:{self.internal}, auto_delete:{self.auto_delete}, message_stats:{self.message_stats}}}')


# --------------------------------------------------------------------------------------------------------------------

class MessageStats(JSONable):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        publish_in = jdict.get('publish_in')
        publish_out = jdict.get('publish_out')

        return cls(publish_in, publish_out)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, publish_in, publish_out):
        """
        Constructor
        """
        super().__init__()

        self.__publish_in = publish_in                      # int
        self.__publish_out = publish_out                    # int


    def __eq__(self, other):
        return self.publish_in == other.publish_in and self.publish_out == other.publish_out


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['publish_in'] = self.publish_in
        jdict['publish_out'] = self.publish_out

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def publish_in(self):
        return self.__publish_in


    @property
    def publish_out(self):
        return self.__publish_out


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'MessageStats:{{publish_in:{self.publish_in}, publish_out:{self.publish_out}}}'
