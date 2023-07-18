import control.matlab as mat
import json
from plant import Plant
from requirements import Requirements

class Controler:
    def __init__(self, filepath: str, dt: float) -> None:
        d = self.load(filepath)
        for k, v in d.items():
            setattr(self, k, v)
        self.gains = d.keys()
        self.dt = dt
        self.generate_tfs()

    def generate_tfs(self) -> None:
        self.lead = mat.tf([self.T, 1.], [self.alpha*self.T, 1.0])
        self.PD = mat.tf([self.Kd, self.Kp], [1.])
        self.C = self.lead*self.PD

    def update(self, new_gains: dict)-> None:
        for k in self.gains:
            setattr(self, k, new_gains[k])
        self.generate_tfs()

    def load(self, filepath: str) -> dict:
        with open(filepath, "r") as f:
            d =  json.load(f)
        return d
    
    def save(self, filepath: str) -> None:
        d = vars(self)
        with open(filepath,"w") as f:
            json.dump({k: d[k] for k in self.gains}, f)

    def project_analytical(self, plant: Plant, reqs: Requirements) -> None:
        pass