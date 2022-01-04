from time import sleep

from pymongo import MongoClient
from loguru import logger

from config import base_domen, base_port, client_name


while True:
    try:
        client = MongoClient(
            host=base_domen,
            port=base_port,
        )
        db = client[client_name]
        shichko_collection = db["shichko"]
        thanks_collection = db["thanks"]
        plans_collection = db["plans"]
        books_collection = db["books"]
        lessons_collection = db["lessons"]
        clean_collection = db["clean"]
        sport_collection = db["sport"]
        run_walk_collection = db["run_walk"]

        user_collection = db["user"]
        main_collection = db["main"]

        break
    except Exception as e:
        logger.exception(e)
        sleep(5)
