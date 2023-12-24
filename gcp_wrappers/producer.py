import json
import logging
import os
from typing import Dict, Any
from google.cloud import pubsub_v1
from settings import sa_credentials_for_clients, TOPIC_NAME

logger = logging.getLogger()
credentials = sa_credentials_for_clients


def publish_message(message: Dict[str, Any]) -> None:
    logger.info(f"publish_message enter")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(os.environ.get("GCP_PROJECT"), TOPIC_NAME)
    print(f"publishing {message['message_id']} to topic {topic_path}")
    publisher.publish(topic_path, data=json.dumps(message).encode("utf-8")).result()
