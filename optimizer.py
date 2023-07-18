import cma
from scipy.optimize import minimize # method = 'Nelder-Mead'
from requirements import Requirements
from numpy.typing import NDArray, Float64
from typing import Tuple
from system import System
from control.matlab import *


class Optimizer:
    def __init__(self, optimizer, initial_guess: Tuple[NDArray[Float64]]) -> None:
        self.optimizer = optimizer
        self.initial_guess = initial_guess

    def minimize(self, reqs: Requirements, system: System):
        return self.optimizer(self.make_obj_func(reqs, system), *self.initial_guess)
    
    def save_solution(self):
        pass

    def make_obj_func(self, reqs: Requirements, system: System) -> callable:
        J = lambda x: (
            system.update_controler(x)
            (bandwidth(system.Gf) - reqs.wb)**2 + (margin(system.Ga)[1] - reqs.pm)**2
            )
        return J
        
        