import sys
path = '/home/robert/work/'
sys.path.append(path + 'nfield/source/')
from multilangevinsolver import multilangevinsolver 

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text',usetex=True)
import pylab as pl


class nfield:
# Initialize the code


    def __init__(self,path_to_nfield_directory,potentials,solver_choice='IE'):
    # Initialise self...
