from models import db_session, Pericia

def criar_pericias() -> None:
    for i in range(500):
        per = Pericia()
        per.n_celulares = 3