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

ctrl = Controler("gains/initial.json")
plant = Plant(1., 1.0, 1.0, 0.001)
sys = System(ctrl, plant)
opt = Optimizer(cma.fmin2, [ctrl.get_gains(), 100])

def nelder_mead_opt(f: callable, *args):
    """the nelder mead method minimizer function.
       It's called with bounds in the objective function parameters,
       to avoid getting invalid results.

    Args:
        f (callable): objective function to be minimized

    Returns:
        result: the result object for the scipy.optimize.minimize interface
    """
    return minimize(f, *args, method='Nelder-Mead', bounds=[(0., None), (0.0, 1.0), (0.0, None)],callback = lambda sol: Optimizer.ND_log_loss(opt, sol))

def cma_es_opt(f: callable, *args):
    """the cma-es method minimizer function.
       It's called with bounds in the objective function parameters,
       to avoid getting invalid results.

    Args:
        f (callable): objective function to be minimized

    Returns:
        result: the result object for the pycma interface
    """
    return cma.fmin2(f, *args, options = {"bounds" : [[0., 0., 0.], [None, 1., None]], "verbose" : -2}, callback = lambda es: Optimizer.cma_log_loss(opt, es))

def benchmark(algo: str, wb: float, pm: float, t = np.linspace(0.,0.7,1000)):
    """benchmarks specified optimization algorithm. It produces the step response,
       along with the overshoot, steady state value, and saves the controller's optimized gains
       to a .json file.

    Args:
        algo (str): name of the algorithm, if not valid, then the benchmark is executed with the controller analytical gains.
        wb (float): bandwidth requirement (rad/s).
        pm (float): phase margin requirement (degrees).
        t (NumPy array, optional): the timespan along which to generate the step response. Defaults to np.linspace(0.,0.7,1000).
    """
    reqs = Requirements(wb = wb, pm = pm, err = 0.0)
    ctrl.project_analytical(plant, reqs) # obtain analytical gains for initial guess
    if algo.lower() == 'cma':
        opt.restart(cma_es_opt, [ctrl.get_gains(), 1e4])
        opt.minimize(reqs, sys)
    elif algo.lower() in ['nelder-mead', 'nd']:
        algo = 'ND'
        opt.restart(nelder_mead_opt, [ctrl.get_gains()])
        opt.minimize(reqs, sys)
    # optimized system's parameters
    print("wb: {:.2f}".format(mat.bandwidth(sys.Gf)))
    print("PM: {:.2f}".format(mat.margin(sys.Ga)[1]))
    # plots the loss history of the optimization
    plt.figure()
    plt.plot(opt.loss_history)
    plt.title('Fitness History')
    plt.ylabel('Fitness')
    plt.xlabel('# Iterations')
    plt.savefig('err_hist_'+algo+'_wb{}'.format(reqs.wb)+'.eps', bbox_inches='tight')
    #optimized gains
    print("Kp: ", ctrl.Kp)
    print("alpha: ",ctrl.alpha)
    print("T: ", ctrl.T)
    ctrl.save('gains/gains_'+algo+'_wb{}'.format(reqs.wb)+'.json')
    # plots step response
    y, _ =  mat.step(sys.Gf, T = t)
    res = mat.stepinfo(sys.Gf)
    plt.figure()
    plt.plot(t, y)
    plt.xlim(left = 0.0)
    plt.ylim(bottom = 0.0)
    inf_val = res['SteadyStateValue']
    overshoot = res['Peak']
    plt.axhline(y = inf_val, color = 'y', linestyle = '--')
    plt.axhline(y = overshoot, color = 'r', linestyle = '--')
    plt.xlabel('tempo (s)')
    plt.ylabel(r'$\theta$ (rad)')
    plt.savefig('step_response_'+algo+'_wb{}'.format(reqs.wb)+'.eps', bbox_inches='tight')

for wb in [50, 250, 500]:
    benchmark('none', wb, 60, t = np.linspace(0.,10,int(1e4)))