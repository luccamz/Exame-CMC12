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

ctrl = Controler("initial.json", 1e-4)
plant = Plant(1., 1.0, 5.0, 0.001)
sys = System(ctrl, plant)

def nelder_mead_opt(f, *args):
    return minimize(f, *args, method='Nelder-Mead', bounds=[(0., None), (0.0, 1.0), (0.0, None)])

def cma_es_opt(f, *args):
    return cma.fmin2(f, *args, options = {"bounds" : [[0., 0., 0.], [None, 1., None]], "verbose" : -2})

def benchmark(algo: str, wb: float, pm: float):
    reqs = Requirements(wb = wb, pm = pm, err = 0.0)
    ctrl.project_analytical(plant, reqs)
    if algo == 'cma':
        opt = Optimizer(cma_es_opt, [ctrl.get_gains(), 100])
    elif algo == 'nelder-mead':
        opt = Optimizer(nelder_mead_opt, [ctrl.get_gains()])
    else:
        raise ValueError("Invalid algorithm name")
    req = Requirements(wb = wb, pm = pm, err = 0.0)
    opt.minimize(req, sys)
    print(mat.margin(sys.Ga)[1])
    print(mat.bandwidth(sys.Gf))
    print("Kp: ", ctrl.Kp)
    print("alpha: ",ctrl.alpha)
    print("T: ", ctrl.T)
    y, t =  mat.step(sys.Gf, T = np.linspace(0.,0.7,1000))
    plt.plot(t, y)
    plt.savefig('step_response_'+algo+'.eps')
    ctrl.save('gains_'+algo+'.json')

benchmark('cma', 50, 60)

