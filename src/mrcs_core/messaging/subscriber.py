"""
Created on 1 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A RabbitMQ peer that subscribes to given routing keys on a given exchange

https://www.rabbitmq.com/tutorials/tutorial-four-python
"""

import pika

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

    @classmethod
    def ack(cls, ch, method):
        ch.basic_ack(delivery_tag=method.delivery_tag)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, exchange, queue, callback, channel=None):
        """
        Constructor
        """
        self.__exchange = exchange
        self.__queue = queue
        self.__callback = callback

        self.__channel = channel
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.__DEFAULT_HOST),
        )

        self.__channel = connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic")


    def subscribe(self, *binding_keys: RoutingKey):
        if self.channel is None:
            raise RuntimeError('subscribe: no channel')

        if not binding_keys:
            raise RuntimeError('subscribe: no binding keys')

        self.channel.queue_declare(queue=self.queue, exclusive=True)

        for binding_key in binding_keys:
            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue,
                routing_key=str(binding_key),
            )

        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.callback,
        )

        self.channel.start_consuming()


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
