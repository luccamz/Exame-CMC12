from control.matlab import *
import json

class Controler:
    def __init__(self, filepath: str, dt: float) -> None:
        d = self.load(filepath)
        for k, v in d.items():
            setattr(self, k, v)
        self.dt = dt
        self.lead = tf([self.T, 1.], [self.alpha*self.T, 1.0], self.dt)
        self.PD = tf([self.Kp, self.Kd], [1.], self.dt)
        self.C = self.lead*self.PD


    def load(self, filepath: str) -> dict:
        with open(filepath, "r") as f:
            d =  json.load(f)
        return d
    
    def save(self, filepath: str) -> None:
        gains = ["Kp","Kd","alpha","T"]
        d = vars(self)
        with open(filepath,"w") as f:
            json.dump({k: d[k] for k in gains}, f)