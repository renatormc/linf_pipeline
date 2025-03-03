from datetime import datetime, timedelta
from operator import and_
from typing import Iterable, Iterator
from models import Objeto, Pericia, db_session
from models import Perito


def interval_iterator(data_inicial: datetime, data_final: datetime) -> Iterator[datetime]:
    data = data_inicial
    while data < data_final:
        yield data
        data += timedelta(minutes=1)
        
def get_perito_disponivel() -> Perito | None:
    query = db_session.query(Perito).where(
        Perito.pericias.any(and_(
            Pericia.comeco != None,
            Pericia.fim == None
            
        ))
    )
    return query.first()

        
def simular_atual() -> None:
    for time in interval_iterator(datetime.now(), datetime.now() + timedelta(minutes=5)):
        print(time)