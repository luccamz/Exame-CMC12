import cma
from scipy.optimize import minimize # method = 'Nelder-Mead'

class Optimizer:
    def __init__(self, optimizer, initial_guess, obj_func) -> None:
        self.optimizer = optimizer
        self.initial_guess = initial_guess
        self.obj_func = obj_func

    def minimize(self):
        return self.optimizer(self.obj_func, *self.initial_guess)
    
    def save_solution(self):
        pass