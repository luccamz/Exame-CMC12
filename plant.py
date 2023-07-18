import numpy as np
import control.matlab as mat

class Plant:
    def __init__(self, m: float, R: float, J: float, b: float, theta_0: float = 0.0, omega_0: float = 0.0) -> None:
        params = np.array([m, R, J, b])
        if np.any(params < 0.0):
            raise ValueError("Temporal, spatial and inertial parameters can't be negative")
        self.m = m
        self.R = R
        self.J = J
        self.b = b
        self.theta = theta_0
        self.omega = omega_0
        self.tf = mat.tf([R], [J+m*R**2, b, 0.])

    def change_mass(self, new_mass: float) -> None:
        if new_mass < 0.0:
            raise ValueError("Mass can't be negative")
        self.m = new_mass
        self.tf = mat.tf([self.R], [self.J+self.m*self.R**2, self.b, 0.])