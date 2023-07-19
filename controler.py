import control.matlab as mat
import json
from plant import Plant
from requirements import Requirements
from numpy import sqrt, pi, sin, angle, roots

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
        self.C = self.lead*self.Kp

    def get_gains(self) -> tuple:
        return tuple([getattr(self, g) for g in self.gains])

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

    # consertar isso?
    def project_analytical(self, plant: Plant, reqs: Requirements) -> None:
        wb = reqs.wb
        PM = reqs.pm
        J = plant.J
        R = plant.R
        m = plant.m
        b = plant.b
        Jeq = J + m*R**2
        x = roots([R**2, 2*Jeq*wb ,-(Jeq*wb**2)**2-(wb*b)**2])
        x.sort()
        self.Kp = x[1]
        y = roots([Jeq**2, b**2, -self.Kp**2])
        y.sort()
        wcp = sqrt(y[1])
        PMa=angle(-Jeq*wcp-b*1j)+pi
        phimax=PM*pi/180-PMa
        self.alpha=(1-sin(phimax))/(1+sin(phimax))
        self.T = 1/(wcp*sqrt(self.alpha))
        self.generate_tfs()