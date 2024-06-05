
import threading
import time
import math


class Calle():

    def __init__(self, carros: list[str], carsToRemove: int, sentido: str, turno: bool):
        super().__init__()
        self.carros = carros
        self.carsToRemove = carsToRemove
        self.sentido = sentido
        self.turno = turno

    def setCarsToRemove(self, carsToRemove: int):
        self.carsToRemove = carsToRemove

    def setTurno(self, turno: bool):
        self.turno = turno

    def run(self):
        carsToRemove = self.carsToRemove
        while carsToRemove > 0:
            print(f"Un carro en sentido {self.sentido} esta pasando.")
            self.carros.pop(0)
            carsToRemove -= 1
            time.sleep(1)
            print(f"**El carro en sentido {self.sentido} ya pasó.")
        print("Cambiando de sentido.")
        self.setTurno(False)
        

        
class PuenteEstrecho(threading.Thread):
    def __init__(self, norte: Calle, sur: Calle, ratioNorte: int, ratioSur: int):
        self.lock = threading.Lock()
        self.norte = norte
        self.sur = sur
        self.ratioNorte = ratioNorte
        self.ratioSur = ratioSur

    def conteo(self):
        print(f"Carros en el sentido Norte: {len(self.norte.carros)}")
        print(f"Carros en el sentido Sur: {len(self.sur.carros)}")

    def ratio(self):
        if len(self.norte.carros) == len(self.sur.carros):
            ratioNorte = 1
            ratioSur = 1
        elif len(self.norte.carros) > len(self.sur.carros):
            ratioNorte = math.floor(len(self.norte.carros) / len(self.sur.carros))
            ratioSur = 1
        elif len(self.norte.carros) < len(self.sur.carros):
            ratioSur = math.floor(len(self.sur.carros) / len(self.norte.carros))
            ratioNorte = 1
        else:
            ratioNorte = 1
            ratioSur = 1
        return ratioNorte, ratioSur
    

    def run(self):
        self.conteo()
        ratios = self.ratio()
        self.norte.setCarsToRemove(ratios[0])
        self.sur.setCarsToRemove(ratios[1])

        print("Todos los carros han pasado.")


def main():
    norte = Calle(["N","N","N","N","N","N"] , 0, "Norte", True)
    sur = Calle(["S","S","S"] , 0, "Sur", False)
    p = PuenteEstrecho(norte, sur, 0, 0)
    p.run()

if __name__ == "__main__":
    main()
