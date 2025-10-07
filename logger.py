import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tg_messenger.log"),
        logging.StreamHandler()
    ]
)

def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)
