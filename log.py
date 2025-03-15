import logging
import config

file_handler = logging.FileHandler(config.APPDIR / '.local/app.log', encoding='utf-8', mode="w")

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)





