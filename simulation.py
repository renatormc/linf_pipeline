from datetime import datetime, timedelta
from typing import Iterable, Iterator


def interval_iterator(data_inicial: datetime, data_final: datetime) -> Iterator[datetime]:
    data = data_inicial
    while data < data_final:
        yield data
        data += timedelta(minutes=1)