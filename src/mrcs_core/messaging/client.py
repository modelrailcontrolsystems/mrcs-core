"""
Created on 1 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

* Client - an abstract RabbitMQ peer
* Publisher - a RabbitMQ peer that publishes with a routing on a given exchange
* Subscriber - a RabbitMQ peer that subscribes to routings on a given exchange

https://www.rabbitmq.com/tutorials/tutorial-four-python
https://github.com/aiidateam/aiida-core/issues/1142
"""

import json
from abc import ABC

import pika

from mrcs_core.data.json import JSONify
from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import RoutingKey
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class Client(ABC):
    """
    classdocs
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
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def exchange_delete(self, exchange, callback):
        if self.channel is None:
            raise RuntimeError('exchange_delete: no channel')

        self.channel.exchange_delete(self, exchange=exchange, if_unused=True, callback=callback)


    def queue_delete(self, queue, callback):
        if self.channel is None:
            raise RuntimeError('queue_delete: no channel')

        self.channel.queue_delete(self, queue, if_unused=True, if_empty=False, callback=callback)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Manager:{{channel:{self.channel}}}'


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(Client):
    """
    classdocs
    """

    __EXCHANGE_TYPE = 'topic'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, exchange):
        """
        Constructor
        """
        super().__init__()
        self.__exchange = exchange


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        super().connect()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.__EXCHANGE_TYPE, durable=True)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def exchange(self):
        return self.__exchange


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Endpoint:{{exchange:{self.exchange}, channel:{self.channel}}}'


# --------------------------------------------------------------------------------------------------------------------

class Publisher(Endpoint):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, exchange):
        """
        Constructor
        """
        super().__init__(exchange)


    # ----------------------------------------------------------------------------------------------------------------

    def publish(self, message: Message):
        if self.channel is None:
            raise RuntimeError('publish: no channel')

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=str(message.routing_key),
            body=JSONify.dumps(message.body),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
        )


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Publisher:{{exchange:{self.exchange}, channel:{self.channel}}}'


# --------------------------------------------------------------------------------------------------------------------

class Subscriber(Endpoint):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, exchange, queue, callback):
        """
        Constructor
        """
        super().__init__(exchange)
        self.__queue = queue
        self.__callback = callback


    # ----------------------------------------------------------------------------------------------------------------

    def subscribe(self, *routing_keys: RoutingKey):
        if self.channel is None:
            raise RuntimeError('subscribe: no channel')

        if not routing_keys:
            raise RuntimeError('subscribe: no routing keys')

        self.channel.queue_declare(queue=self.queue, durable=True, exclusive=True)

        for routing_key in routing_keys:
            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue,
                routing_key=str(routing_key),
            )

        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.on_message_callback,
        )

        self.channel.start_consuming()


    def on_message_callback(self, ch, method, _properties, body):
        self._logger.warning(f'on_message_callback - routing:{method.routing_key}, delivery_tag:{method.delivery_tag}')

        self.callback(Message.construct(method.routing_key, json.loads(body.decode())))
        ch.basic_ack(delivery_tag=method.delivery_tag)      # ACK will not take place if callback raises an exception


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def queue(self):
        return self.__queue


    @property
    def callback(self):
        return self.__callback


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'Subscriber:{{exchange:{self.exchange}, queue:{self.queue}, callback:{self.callback}, '
                f'channel:{self.channel}}}')
