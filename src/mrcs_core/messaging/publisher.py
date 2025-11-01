"""
Created on 1 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A RabbitMQ peer that publishes on a given exchange

https://www.rabbitmq.com/tutorials/tutorial-four-python
"""

import pika

from mrcs_core.data.json import JSONable, JSONify
from mrcs_core.messaging.routing_key import RoutingKey
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class Publisher(object):
    """
    classdocs
    """

    __DEFAULT_HOST = 'localhost'
    __EXCHANGE_TYPE = 'topic'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, exchange, channel=None):
        """
        Constructor
        """
        self.__exchange = exchange

        self.__channel = channel
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.__DEFAULT_HOST),
        )

        self.__channel = connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.__EXCHANGE_TYPE)   # durable=True


    def publish(self, routing_key: RoutingKey, message):
        if self.channel is None:
            raise RuntimeError('publish: no channel')

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=str(routing_key),
            body=JSONify.dumps(message),
            # properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
        )


    def close(self):
        if self.channel is None:
            return

        self.channel.close()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def exchange(self):
        return self.__exchange


    @property
    def channel(self):
        return self.__channel


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'Publisher:{{exchange:{self.exchange}, channel:{self.channel}}}'
