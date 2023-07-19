import control.matlab as mat
import json
from plant import Plant
from requirements import Requirements
from numpy import sqrt, pi, sin, angle, roots

class Controler:
    """Represents the P + lead controler.
    """
    def __init__(self, filepath: str) -> None:
        """
        Args:
            filepath (str): path to .json file storing the controller gains.
        """
        d = self.load(filepath)
        for k, v in d.items():
            setattr(self, k, v)
        self.gains = d.keys()
        self.generate_tfs()

    def generate_tfs(self) -> None:
        """Generates the lead and final compensator transfer functions
        """
        self.lead = mat.tf([self.T, 1.], [self.alpha*self.T, 1.0])
        self.C = self.lead*self.Kp

    def get_gains(self) -> tuple:
        """Obtains the controller gains in the order Kp, alpha, T.

        Returns:
            tuple: controller gains in the order Kp, alpha, T.
        """
        return tuple([getattr(self, g) for g in self.gains])

    def update(self, new_gains: dict)-> None:
        """Updates gains and transfer functions

        Args:
            new_gains (dict): dict with keys naming the gains and containing their new values
        """
        for k in self.gains:
            setattr(self, k, new_gains[k])
        self.generate_tfs()

    def load(self, filepath: str) -> dict:
        """loads controller gains from json

        Args:
            filepath (str): path to .json file.

        Returns:
            dict: dict with keys naming the gains and containing their values
        """
        with open(filepath, "r") as f:
            d =  json.load(f)
        return d
    
    def save(self, filepath: str) -> None:
        """saves controller gains to .json

        Args:
            filepath (str): path to .json file
        """
        d = vars(self)
        with open(filepath,"w") as f:
            json.dump({k: d[k] for k in self.gains}, f)

    def project_analytical(self, plant: Plant, reqs: Requirements) -> None:
        """Generates controller gains based on requirements of bandwidth, phase margin
            and plant parameters, by using an analytical approximative project technique.

        Args:
            plant (Plant): contains the plant parameters.
            reqs (Requirements): contains the bandwidth and phase margin requirements.
        """
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
        y = roots([Jeq**2, b**2, -(self.Kp*R)**2])
        y.sort()
        wcp = sqrt(y[1])
        PMa=angle(-Jeq*wcp-b*1j)+pi
        phimax=PM*pi/180-PMa
        self.alpha=(1-sin(phimax))/(1+sin(phimax))
        self.T = 1/(wcp*sqrt(self.alpha))
        self.generate_tfs()