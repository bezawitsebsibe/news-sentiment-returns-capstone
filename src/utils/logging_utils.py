from loguru import logger

def get_logger():
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level="INFO")
    return logger
