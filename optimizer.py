from requirements import Requirements
from system import System
import control.matlab as mat


class Optimizer:
    def __init__(self, optimizer, initial_guess: tuple) -> None:
        self.optimizer = optimizer
        self.initial_guess = initial_guess

    def minimize(self, reqs: Requirements, system: System):
        return self.optimizer(self.make_obj_func(reqs, system), *self.initial_guess)
    
    def save_solution(self):
        pass

    def make_obj_func(self, reqs: Requirements, system: System) -> callable:
        def J(x):
            system.update_controler(x)
            return (mat.bandwidth(system.Gf) - reqs.wb)**2 + (mat.margin(system.Ga)[1] - reqs.pm)**2
        return J
        
        