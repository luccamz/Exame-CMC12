import numpy as np
import control.matlab as mat

class Plant:
    """Represents the see-saw physical system.
    """
    def __init__(self, m: float, R: float, J: float, b: float, theta_0: float = 0.0, omega_0: float = 0.0) -> None:
        """initializes the physical system with its parameters.

        Args:
            m (float): mass (kg) of the object to be supported.
            R (float): distance (m) from see-saw's center to its extremes.
            J (float): see-saw support's inertia (km.m^2) around its rotation axis.
            b (float): viscous drag coefficient (kg m^2 s^-1).
            theta_0 (float, optional): Initial angle in rad. Defaults to 0.0.
            omega_0 (float, optional):Initial angular speed in rad/s. Defaults to 0.0.

        Raises:
            ValueError: if any of m, R, J, b is negative.
        """
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
        """Allows updating the supported mass.

        Args:
            new_mass (float):  new mass (kg) of the object being supported.

        Raises:
            ValueError: if the new_mass is negative
        """
        if new_mass < 0.0:
            raise ValueError("Mass can't be negative")
        self.m = new_mass
        self.tf = mat.tf([self.R], [self.J+self.m*self.R**2, self.b, 0.])