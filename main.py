from controler import Controler
from plant import Plant
from system import System
from requirements import Requirements
from optimizer import Optimizer
import cma
from scipy.optimize import minimize # method = 'Nelder-Mead'
import control.matlab as mat
import matplotlib.pyplot as plt
import numpy as np

c = Controler("gains.json", 1e-4)
plant = Plant(1.0, 1.0, 1.0, 0.01)
sys = System(c, plant)
req = Requirements(wb = 2000, pm = 60, err = 0.0)
opt_cma = Optimizer(lambda J, x, sig: cma.fmin2(J, x, sig, incpopsize= 5), [(1.0, 0.2, 0.3, 0.5), 10.0])
opt_cma.minimize(req, sys)
print(mat.margin(sys.Ga)[1])
print(mat.bandwidth(sys.Gf))
# opt_nelder_mead = Optimizer(lambda f, x: minimize(f, x, method='Nelder-Mead'), [(1.0, 0.2, 0.3, 0.5)])
# opt_nelder_mead.minimize(req, sys)
# print(mat.margin(sys.Ga)[1])
# print(mat.bandwidth(sys.Gf))
y, t =  mat.step(sys.Gf, T = np.linspace(0.,0.1,1000))
print(mat.pole(sys.Gf))
print(mat.zero(sys.Gf))
print(sys.Gf)
print("Kp: ", c.Kp)
print("alpha: ",c.alpha)
print("T: ", c.T)
plt.plot(t, y)
plt.show()

