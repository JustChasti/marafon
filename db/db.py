from time import sleep

from pymongo import MongoClient
from loguru import logger

from db.config import base_domen, base_port, client_name


while True:
    try:
        client = MongoClient(
            host=base_domen,
            port=base_port,
        )
        db = client[client_name]
        regular_tasks = db["regular_tasks"]
        user_collection = db["user"]
        break
    except Exception as e:
        logger.exception(e)
        sleep(5)
