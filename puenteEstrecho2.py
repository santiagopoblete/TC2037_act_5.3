import threading
import time
import math

class Calle(threading.Thread):
    def __init__(self, carros: list[str], carsToRemove: int, sentido: str, turno: bool):
        super().__init__()
        self.carros = carros
        self.carsToRemove = carsToRemove
        self.sentido = sentido
        self.turno = turno
        self.lock = threading.Lock()

    def setCarsToRemove(self, carsToRemove: int):
        self.carsToRemove = carsToRemove

    def setTurno(self, turno: bool):
        self.turno = turno

    def run(self):
        with self.lock:
            carsToRemove = self.carsToRemove
            while carsToRemove > 0 and self.carros:
                print(f"Un carro en sentido {self.sentido} esta pasando.")
                self.carros.pop(0)
                carsToRemove -= 1
                time.sleep(1)
                print(f"**El carro en sentido {self.sentido} ya pasó.")
                print("+"*50)
            print(f"Cambiando de sentido")
            print("#"*50)
            self.setTurno(False)

class PuenteEstrecho():
    def __init__(self, norte: Calle, sur: Calle, ratioNorte: int, ratioSur: int):
        self.lock = threading.Lock()
        self.norte = norte
        self.sur = sur
        self.ratioNorte = ratioNorte
        self.ratioSur = ratioSur

    def conteo(self):
        print(f"Carros en el sentido Norte: {len(self.norte.carros)}")
        print(f"Carros en el sentido Sur: {len(self.sur.carros)}")
        print("-" * 50)

    def ratio(self):
        if len(self.norte.carros) == len(self.sur.carros):
            ratioNorte = 1
            ratioSur = 1
        elif len(self.norte.carros) > len(self.sur.carros):
            ratioNorte = max(1, math.floor(len(self.norte.carros) / len(self.sur.carros)))
            ratioSur = 1
        else:
            ratioSur = max(1, math.floor(len(self.sur.carros) / len(self.norte.carros)))
            ratioNorte = 1
        return ratioNorte, ratioSur

    def run(self):
        while len(self.norte.carros) > 0 or len(self.sur.carros) > 0:
            self.conteo()
            ratios = self.ratio()
            self.norte.setCarsToRemove(ratios[0])
            self.sur.setCarsToRemove(ratios[1])

            if len(self.norte.carros) > 0:
                self.norte = Calle(self.norte.carros, ratios[0], self.norte.sentido, self.norte.turno)
                self.norte.start()
                self.norte.join()

            if len(self.sur.carros) > 0:
                self.sur = Calle(self.sur.carros, ratios[1], self.sur.sentido, self.sur.turno)
                self.sur.start()
                self.sur.join()

            print("-" * 50)
            
        print("Todos los carros han pasado.")

def main():
    norte = Calle(["N", "N", "N", "N", "N", "N", "N", "N", "N", "N"], 0, "Norte", True)
    sur = Calle(["S", "S", "S", "S", "S", "S", "S"], 0, "Sur", False)
    p = PuenteEstrecho(norte, sur, 0, 0)
    p.run()

if __name__ == "__main__":
    main()
