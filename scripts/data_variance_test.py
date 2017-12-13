import sys
path = '/home/robert/work/'
sys.path.append(path + 'nfield/source/')
from nfield import nfield 
import numpy as np

def drift_function(x,t):
    drifxt = x
    drifxt[:,0] = (x[:,0]**2.0)/(t[:,0]+0.1)
    drifxt[:,1] = (4.0*x[:,1]**2.0)/(t[:,1]+0.1)
    return drifxt

def diffusion_function(x,t):
    diffxt = x
    diffxt[:,0] = (t[:,0]+0.1)**2.0
    diffxt[:,1] = (t[:,1]+0.1)**2.0
    return diffxt 

def init_value(dimension):
    if dimension == 0:
        output = 0.0
    if dimension == 1:
        output = 0.0
    return output

mls = multilangevinsolver(path + 'nfield/',drift_function,diffusion_function) 
mls.data_evolving_moments('data_variance_test.txt',100,2,0.01,100,init_value)
