
class RandomNumeroObjetos:
    def __init__(self):
        self.stat = {1: 50, 2: 45, 3: 35, 4: 25, 5: 15, 6: 10, 7: 2}
        self.values = list(self.stat.keys())
        total = sum(self.stat.values())
        self.probabilites = map(lambda x: x/total, self.stat.values())

numero_objetos_values = {1: 50, 2: 45, 3: 35, 4: 25, 5: 15, 6: 10, 7: 2}


def random_numero_objetos() -> int:
    values = [1, 2, 3, 4, 5, 6]
    
