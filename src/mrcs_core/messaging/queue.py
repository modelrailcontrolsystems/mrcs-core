"""
Created on 22 Dec 2020

Created on 1 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A queue hosted by RabbitMQ

{
  "arguments": {
    "x-queue-type": "classic"
  },
  "auto_delete": false,
  "consumer_capacity": 1,
  "consumer_utilisation": 1,
  "consumers": 1,
  "durable": false,
  "effective_policy_definition": {},
  "exclusive": true,
  "internal": false,
  "internal_owner": false,
  "memory": 14240,
  "message_bytes": 0,
  "message_bytes_paged_out": 0,
  "message_bytes_persistent": 0,
  "message_bytes_ram": 0,
  "message_bytes_ready": 0,
  "message_bytes_unacknowledged": 0,
  "message_stats": {
    "ack": 0,
    "ack_details": {
      "rate": 0
    },
    "deliver": 0,
    "deliver_details": {
      "rate": 0
    },
    "deliver_get": 2,
    "deliver_get_details": {
      "rate": 0
    },
    "deliver_no_ack": 2,
    "deliver_no_ack_details": {
      "rate": 0
    },
    "get": 0,
    "get_details": {
      "rate": 0
    },
    "get_empty": 0,
    "get_empty_details": {
      "rate": 0
    },
    "get_no_ack": 0,
    "get_no_ack_details": {
      "rate": 0
    },
    "publish": 2,
    "publish_details": {
      "rate": 0
    },
    "redeliver": 0,
    "redeliver_details": {
      "rate": 0
    }
  },
  "messages": 0,
  "messages_details": {
    "rate": 0
  },
  "messages_paged_out": 0,
  "messages_persistent": 0,
  "messages_ram": 0,
  "messages_ready": 0,
  "messages_ready_details": {
    "rate": 0
  },
  "messages_ready_ram": 0,
  "messages_unacknowledged": 0,
  "messages_unacknowledged_details": {
    "rate": 0
  },
  "messages_unacknowledged_ram": 0,
  "name": "log_receiver_695",
  "node": "rabbit@localhost",
  "reductions": 12310,
  "reductions_details": {
    "rate": 0
  },
  "state": "running",
  "storage_version": 2,
  "type": "classic",
  "vhost": "/"
}

https://www.rabbitmq.com/docs/http-api-reference
"""

from collections import OrderedDict

from mrcs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Queue(JSONable):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        name = jdict.get('name')
        queue_type = jdict.get('type')
        durable = jdict.get('durable')
        exclusive = jdict.get('exclusive')

        state = jdict.get('state')
        consumers = jdict.get('consumers')

        messages = jdict.get('messages')
        messages_ready = jdict.get('messages_ready')
        messages_unacknowledged = jdict.get('messages_unacknowledged')

        return cls(name, queue_type, durable, exclusive, state, consumers,
                   messages, messages_ready, messages_unacknowledged)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, queue_type, durable, exclusive, state, consumers,
                 messages, messages_ready, messages_unacknowledged):
        """
        Constructor
        """
        super().__init__()

        self.__name = name                                                  # string
        self.__queue_type = queue_type                                      # string
        self.__durable = durable                                            # bool
        self.__exclusive = exclusive                                        # bool

        self.__state = state                                                # string
        self.__consumers = consumers                                        # int

        self.__messages = messages                                          # int
        self.__messages_ready = messages_ready                              # int
        self.__messages_unacknowledged = messages_unacknowledged            # int


    def __lt__(self, other):
        return self.name < other.name


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['name'] = self.name
        jdict['type'] = self.queue_type
        jdict['durable'] = self.durable
        jdict['exclusive'] = self.exclusive

        jdict['state'] = self.state
        jdict['consumers'] = self.consumers

        jdict['messages'] = self.messages
        jdict['messages_ready'] = self.messages_ready
        jdict['messages_unacknowledged'] = self.messages_unacknowledged

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def queue_type(self):
        return self.__queue_type


    @property
    def durable(self):
        return self.__durable


    @property
    def exclusive(self):
        return self.__exclusive


    @property
    def state(self):
        return self.__state


    @property
    def consumers(self):
        return self.__consumers


    @property
    def messages(self):
        return self.__messages


    @property
    def messages_ready(self):
        return self.__messages_ready


    @property
    def messages_unacknowledged(self):
        return self.__messages_unacknowledged


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'Queue:{{name:{self.name}, queue_type:{self.queue_type}, durable:{self.durable}, '
                f'exclusive:{self.exclusive}, state:{self.state}, consumers:{self.consumers}, '
                f'messages:{self.messages}, messages_ready:{self.messages_ready}, '
                f'messages_unacknowledged:{self.messages_unacknowledged}}}')
