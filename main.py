import random


class RandomNumeroObjetos:
    def __init__(self):
        self.stat = {1: 50, 2: 45, 3: 35, 4: 25, 5: 15, 6: 10, 7: 2}
        self.values = list(self.stat.keys())
        total = sum(self.stat.values())
        self.probabilites = list(map(lambda x: x/total, self.stat.values()))

    def gerar(self) -> int:
        return random.choices(self.values, self.probabilites)[0]


class RandomTipoObjeto:
    def __init__(self):
        self.stat = {"celular": 90, "computador": 20}
        self.values = list(self.stat.keys())
        total = sum(self.stat.values())
        self.probabilites = list(map(lambda x: x/total, self.stat.values()))

    def gerar(self) -> str:
        return random.choices(self.values, self.probabilites)[0]


class RandomTipoExtracao:
    def __init__(self):
        self.stat = {"fisica": 90, "sistema_arquivos": 20, "logica": 10, "bloqueado": 20, "estragado": 10}
        self.values = list(self.stat.keys())
        total = sum(self.stat.values())
        self.probabilites = list(map(lambda x: x/total, self.stat.values()))

    def gerar(self) -> str:
        return random.choices(self.values, self.probabilites)[0]


class RandomCapacidade:
    def __init__(self):
        self.stat = {"500GB": 90, "1024GB": 20, "2048GB": 10}
        self.values = list(self.stat.keys())
        total = sum(self.stat.values())
        self.probabilites = list(map(lambda x: x/total, self.stat.values()))

    def gerar(self) -> str:
        return random.choices(self.values, self.probabilites)[0]


random_tipo = RandomTipoObjeto()
random_extracao = RandomTipoExtracao()
random_capacidade = RandomCapacidade()


def random_objeto() -> str:
    tipo = random_tipo.gerar()
    if tipo == "celular":
        ext = random_extracao.gerar()
        return f"{tipo}/{ext}"
    elif tipo == "computador":
        cap = random_capacidade.gerar()
        return f"{tipo}/{cap}"
    return ""


res: dict[str, int] = {}
for _ in range(500):
    value = random_objeto()
    try:
        res[value] += 1
    except KeyError:
        res[value] = 1
print(res)
