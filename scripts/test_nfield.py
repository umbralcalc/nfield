import sys
path = '/home/robert/work/'
sys.path.append(path + 'nfield/source/')
from nfield import nfield 
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
mpl.rc('font',family='Computer Modern Roman')
mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams['ytick.labelsize'] = 20
import matplotlib.pyplot as plt
import pylab as pl

masssq1 = 3.0
masssq2 = 1.1
Hend = 1.0#10.0**(-6.0)
number_of_realisations = 10000
number_of_fields = 2
Nefolds = 100.0
Number_of_Nsteps = 1000

def first_derivs_potential(field_realisations,N):
    firstderivsfN = np.zeros((number_of_realisations,number_of_fields))# Very important to initialise to zeros!!
    firstderivsfN[:,0] = masssq1*field_realisations[:,0]
    firstderivsfN[:,1] = masssq2*(field_realisations[:,1])
    return firstderivsfN

def Hubble_function(field_realisations,N):
    return Hend

def test_variance1(field_realisations,N):
    return np.sqrt(3.0*(Hubble_function(field_realisations,N)**4.0)/(8.0*np.pi*np.pi*masssq1))

def test_variance2(field_realisations,N):
    return np.sqrt(3.0*(Hubble_function(field_realisations,N)**4.0)/(8.0*np.pi*np.pi*masssq2))

nf = nfield(path + 'nfield/',first_derivs_potential,Hubble_function,number_of_realisations,number_of_fields) 
nf.output_IR_variances('nfield_test.txt',Nefolds/float(Number_of_Nsteps),Number_of_Nsteps)

N_time_data = []
variance_data1 = []
variance_data2 = []
test_variance_data1 = []
test_variance_data2 = []
with open(path + 'nfield/data/nfield_test.txt') as file:
# Compute quantities in loop dynamically as with open(..) reads off the data file
    for line in file:
        columns = line.split()
        N_time_data.append(float(columns[0]))
        variance_data1.append(np.sqrt(float(columns[3])))
        variance_data2.append(np.sqrt(float(columns[4])))
        test_variance_data1.append(test_variance1(0,float(columns[0])))
        test_variance_data2.append(test_variance2(0,float(columns[0]))) 
    
figure = plt.plot(N_time_data,variance_data1,color='Red',linewidth=2,label=r'$\langle \chi^2_1\rangle$')
figure = plt.plot(N_time_data,variance_data2,color='Blue',linewidth=2,label=r'$\langle \chi^2_2\rangle$')
figure = plt.plot(N_time_data,test_variance_data1,'--',color='Red',linewidth=2)
figure = plt.plot(N_time_data,test_variance_data2,'--',color='Blue',linewidth=2)

axes = plt.gca()
axes.set_xlabel(r"$N$",fontsize=25.0)
#axes.set_ylabel(r"$\frac{\sqrt{\left\langle \sigma^2 \right\rangle }}{H_{\rm end}}$",fontsize=25.0,labelpad=45).set_rotation(0)
#axes.set_xlim([10.0**0.0,10.0**4.5])
#axes.set_ylim([10.0**0.0,10.0**7.0])
#axes.set_ylim(ylim)
axes.set_xscale("log")
axes.set_yscale("log")
plt.savefig(path + 'nfield/plots/test_nfield_plot.pdf', format='pdf',bbox_inches='tight',pad_inches=0.1,dpi=300)


