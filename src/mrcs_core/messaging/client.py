"""
Created on 1 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

* Client - an abstract RabbitMQ client
* Manager - a Client that can perform broker management tasks
* Endpoint - a RabbitMQ peer that can act as a publisher only or as a publisher / subscriber

https://www.rabbitmq.com/tutorials/tutorial-four-python
https://github.com/aiidateam/aiida-core/issues/1142
"""

from abc import ABC

import pika

from mrcs_core.data.equipment_identity import EquipmentIdentifier
from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import RoutingKey, PublicationRoutingKey
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class Client(ABC):
    """
    An abstract RabbitMQ client
    """

    __DEFAULT_HOST = '127.0.0.1'        # do not use localhost - IPv6 issues

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__channel = None
        self._logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.__DEFAULT_HOST),
        )

        self.__channel = connection.channel()


    def close(self):
        if self.channel is None:
            return False

        self.channel.close()
        self.__channel = None
        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def channel(self):
        return self.__channel


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Client:{{channel:{self.channel}}}'


# --------------------------------------------------------------------------------------------------------------------

class Manager(Client):
    """
    A Client that can perform broker management tasks
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def exchange_delete(self, exchange):
        if self.channel is None:
            raise RuntimeError('exchange_delete: no channel')

        self.channel.exchange_delete(exchange=exchange, if_unused=True)


    def queue_delete(self, queue):
        if self.channel is None:
            raise RuntimeError('queue_delete: no channel')

        self.channel.queue_delete(queue, if_unused=True, if_empty=False)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Manager:{{channel:{self.channel}}}'


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(Client):
    """
    A RabbitMQ peer that can act as a publisher only or as a publisher / subscriber
    """

    __EXCHANGE_TYPE = 'topic'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, exchange: str, identity: EquipmentIdentifier | None, queue, callback):
        """
        Constructor
        """
        super().__init__()

        self.__exchange = exchange                      # string

        self.__identity = identity                      # EquipmentIdentifier | None
        self.__queue = queue                            # string
        self.__callback = callback                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        super().connect()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.__EXCHANGE_TYPE, durable=True)


    def publish(self, message: Message):
        if self.channel is None:
            raise RuntimeError('publish: no channel')

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=message.routing_key.as_json(),
            body=JSONify.dumps(message.body),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
        )


    def subscribe(self, *routing_keys: RoutingKey):
        if self.channel is None:
            raise RuntimeError('subscribe: no channel')

        if self.identity is None:
            raise RuntimeError('subscribe: no identity')

        if self.queue is None:
            raise RuntimeError('subscribe: no queue')

        if self.callback is None:
            raise RuntimeError('subscribe: no callback')

        if not routing_keys:
            raise RuntimeError('subscribe: no routing keys')

        self.channel.queue_declare(self.queue, durable=True, exclusive=False)   # durables may not be exclusive

        for routing_key in routing_keys:
            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue,
                routing_key=routing_key.as_json(),
            )

        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.on_message_callback,
        )

        self.channel.start_consuming()


    def on_message_callback(self, ch, method, _properties, body):
        self._logger.warning(f'on_message_callback - routing:{method.routing_key}, delivery_tag:{method.delivery_tag}')

        routing_key = PublicationRoutingKey.construct_from_jdict(method.routing_key)
        if routing_key.source == self.identity:
            return                                          # do not send message to self

        self.callback(Message.construct_from_callback(routing_key, body))

        ch.basic_ack(delivery_tag=method.delivery_tag)      # ACK will not take place if callback raises an exception


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def exchange(self):
        return self.__exchange


    @property
    def identity(self):
        return self.__identity


    @property
    def queue(self):
        return self.__queue


    @property
    def callback(self):
        return self.__callback


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'Endpoint:{{exchange:{self.exchange}, identity:{self.identity}, queue:{self.queue}, '
                f'callback:{self.callback}, channel:{self.channel}}}')
