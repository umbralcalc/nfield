import sys
path = '/home/robert/work/'
sys.path.append(path + 'nfield/source/')
from nfield import nfield 
import numpy as np

masssq1 = 1.0
masssq2 = 1.0
Hend = 1.0#10.0**(-6.0)
number_of_realisations = 10000
number_of_fields = 2
Nefolds = 100.0
Number_of_Nsteps = 1000

def first_derivs_potential(field_realisations,N):
    firstderivsfN = field_realisations
    firstderivsfN[:,0] = masssq1*(field_realisations[:,0]**1.0)
    firstderivsfN[:,1] = masssq2*(field_realisations[:,1]**1.0)
    return firstderivsfN

def Hubble_function(field_realisations,N):
    return Hend

nf = nfield(path + 'nfield/',first_derivs_potential,Hubble_function,number_of_realisations,number_of_fields) 
nf.output_IR_variances('nfield_test.txt',Nefolds/float(Number_of_Nsteps),Number_of_Nsteps)
