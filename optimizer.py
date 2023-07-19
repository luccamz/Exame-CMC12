from requirements import Requirements
from system import System
import control.matlab as mat


class Optimizer:
    def __init__(self, optimizer, initial_guess: tuple) -> None:
        self.optimizer = optimizer
        self.initial_guess = initial_guess
        self.loss_history = []

    def restart(self, optimizer, initial_guess: tuple) -> None:
        self.optimizer = optimizer
        self.initial_guess = initial_guess
        self.loss_history.clear()

    def ND_log_loss(self, sol):
        self.loss_history.append(self.J(sol))

    def cma_log_loss(self, es):
        self.loss_history.append(es.best.f)

    def minimize(self, reqs: Requirements, system: System):
        self.make_obj_func(reqs, system)
        return self.optimizer(self.J, *self.initial_guess)

    def make_obj_func(self, reqs: Requirements, system: System) -> None:
        def J(x):
            system.update_controler(x)
            return  (
                    (mat.bandwidth(system.Gf) - reqs.wb - reqs.delta_wb)**2 
                    +(mat.margin(system.Ga)[1] - reqs.pm - reqs.delta_pm)**2
                    )
        self.J = J
        