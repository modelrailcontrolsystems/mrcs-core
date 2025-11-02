"""
Created on 1 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A RabbitMQ peer that subscribes to routings on a given exchange

https://www.rabbitmq.com/tutorials/tutorial-four-python
"""
import pika

from mrcs_core.messaging.message import Message
from mrcs_core.messaging.routing_key import RoutingKey
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class Subscriber(object):
    """
    classdocs
    """

    __DEFAULT_HOST = 'localhost'
    __EXCHANGE_TYPE = 'topic'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, exchange, queue, callback):
        """
        Constructor
        """
        self.__exchange = exchange
        self.__queue = queue
        self.__callback = callback

        self.__channel = None
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.__DEFAULT_HOST),
        )

        self.__channel = connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.__EXCHANGE_TYPE)


    def subscribe(self, *routing_keys: RoutingKey):
        if self.channel is None:
            raise RuntimeError('subscribe: no channel')

        if not routing_keys:
            raise RuntimeError('subscribe: no routing keys')

        self.channel.queue_declare(queue=self.queue, exclusive=True)

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
        self.__logger.warning(f'received message - routing:{method.routing_key}, delivery_tag:{method.delivery_tag}')

        self.callback(Message.construct(method.routing_key, body.decode()))
        ch.basic_ack(delivery_tag=method.delivery_tag)      # will not take place if callback raises an exception


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def exchange(self):
        return self.__exchange


    @property
    def queue(self):
        return self.__queue


    @property
    def callback(self):
        return self.__callback


    @property
    def channel(self):
        return self.__channel


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'Subscriber:{{exchange:{self.exchange}, queue:{self.queue}, callback:{self.callback}, '
                f'channel:{self.channel}}}')
