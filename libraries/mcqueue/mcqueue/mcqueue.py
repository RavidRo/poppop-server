from time import sleep
from typing import Callable

import pika
import pika.channel
import pika.frame
import pika.spec
import pika.exceptions

from mclogging import logger

QUEUE_NAME: str = "announces"
RABBIT_MQ_HOST = "queue"
RABBIT_MQ_PORT = 5672

MAX_RETRIES = 5


class Queue:
    def __init__(self) -> None:
        self._connect()
        self._channel = self._connection.channel()
        self._channel.queue_declare(
            queue=QUEUE_NAME,
            durable=True,
            exclusive=False,
            auto_delete=False,
        )

    def _connect(self) -> None:
        parameters = pika.ConnectionParameters(
            host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT
        )
        retries = 0
        while retries < MAX_RETRIES:
            try:
                self._connection = pika.BlockingConnection(parameters)
                logger.info(f"Connected to RabbitMQ on {RABBIT_MQ_HOST}:{RABBIT_MQ_PORT}")
                return
            except pika.exceptions.AMQPConnectionError:
                logger.warning("Failed to connect to RabbitMQ, trying again...")
                sleep(3)
                retries += 1

        logger.error("Failed to connect to RabbitMQ")
        raise Exception("Failed to connect to RabbitMQ")

    def publish(self, message: str) -> None:
        self._channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message.encode(),
        )

    def listen(self, on_message: Callable[[str], None]) -> None:
        def _on_message(
            channel: pika.channel.Channel,
            method: pika.spec.Basic.Deliver,
            _header: pika.spec.BasicProperties,
            body: bytes,
        ) -> None:
            try:
                on_message(body.decode())
                channel.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Failed to process message: {e}")
                channel.basic_nack(delivery_tag=method.delivery_tag)

        self._channel.basic_consume(QUEUE_NAME, _on_message, auto_ack=False)
        try:
            self._channel.start_consuming()
        except KeyboardInterrupt:
            self._channel.stop_consuming()
        self._connection.close()

    def __enter__(self) -> "Queue":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._connection.close()
