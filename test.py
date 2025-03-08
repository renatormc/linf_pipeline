from datetime import datetime, timedelta
import logging

inicio = datetime(2024, 1, 1, 0, 0, 0)
fim = datetime(2024, 12, 31, 23, 59, 59)
delta = timedelta(minutes=5)

res = (fim - inicio)/delta
logging.info(res)