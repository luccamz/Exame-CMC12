from plant import Plant
from controler import Controler
from control.matlab import *

class System:
    """Represents the combnation of plant and controller.
    """
    def __init__(self, controler: Controler, plant: Plant) -> None:
        self.controler = controler
        self.plant = plant
        self.generate_tfs()
    
    def generate_tfs(self)-> None:
        """iniitializes the system's open and closed circuit transfer functions.
        """
        self.Ga = self.controler.C*self.plant.tf
        self.Gf = feedback(self.Ga)

    def update_controler(self, x: list) -> None:
        """updates systems's controler gains and the transfer function accordingly

        Args:
            x (list): list of new gains values, assumed to be in the same order they
                      were originally loaded to the controller from a .json file 
                      i.e. Kp, alpha, T.
        """
        d = {}
        for k, v in zip(self.controler.gains, x):
            d[k] = v
        self.controler.update(d)
        self.generate_tfs()
         