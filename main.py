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

ctrl = Controler("gains/initial.json", 1e-4)
plant = Plant(1., 1.0, 1.0, 0.001)
sys = System(ctrl, plant)
opt = Optimizer(cma.fmin2, [ctrl.get_gains(), 100])

def nelder_mead_opt(f, *args):
    return minimize(f, *args, method='Nelder-Mead', bounds=[(0., None), (0.0, 1.0), (0.0, None)],callback = lambda sol: Optimizer.ND_log_loss(opt, sol))

def cma_es_opt(f, *args):
    return cma.fmin2(f, *args, options = {"bounds" : [[0., 0., 0.], [None, 1., None]], "verbose" : -2}, callback = lambda es: Optimizer.cma_log_loss(opt, es))

def benchmark(algo: str, wb: float, pm: float, t = np.linspace(0.,0.7,1000)):
    reqs = Requirements(wb = wb, pm = pm, err = 0.0)
    ctrl.project_analytical(plant, reqs)
    if algo.lower() == 'cma':
        opt.restart(cma_es_opt, [ctrl.get_gains(), 1e4])
        opt.minimize(reqs, sys)
    elif algo.lower() in ['nelder-mead', 'nd']:
        algo = 'ND'
        opt.restart(nelder_mead_opt, [ctrl.get_gains()])
        opt.minimize(reqs, sys)
    print("wb: {:.2f}".format(mat.bandwidth(sys.Gf)))
    print("PM: {:.2f}".format(mat.margin(sys.Ga)[1]))
    plt.figure()
    plt.plot(opt.loss_history)
    plt.title('Fitness History')
    plt.ylabel('Fitness')
    plt.xlabel('# Iterations')
    plt.savefig('err_hist_'+algo+'_wb{}'.format(reqs.wb)+'.eps', bbox_inches='tight')
    print("Kp: ", ctrl.Kp)
    print("alpha: ",ctrl.alpha)
    print("T: ", ctrl.T)
    
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
    ctrl.save('gains/gains_'+algo+'_wb{}'.format(reqs.wb)+'.json')

for wb in [50, 250, 500]:
    benchmark('none', wb, 60, t = np.linspace(0.,10,int(1e4)))

