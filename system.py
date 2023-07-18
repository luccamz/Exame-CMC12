from plant import Plant
from controler import Controler
from control.matlab import *

class System:
    def __init__(self, controler: Controler, plant: Plant) -> None:
        self.controler = controler
        self.plant = plant
        self.generate_tfs()
    
    def generate_tfs(self)-> None:
        self.Ga = self.controler.C*self.plant.tf
        self.Gf = feedback(self.Ga)

    def update_controler(self, x) -> None:
        d = {}
        for k, v in zip(self.controler.gains, x):
            d[k] = v
        self.controler.update(d)
        self.generate_tfs()
         