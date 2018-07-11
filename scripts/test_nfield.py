import sys
path = ''
sys.path.append(path + 'nfield/source/')
from nfield import nfield 
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
mpl.rc('font',family='CMU Serif')
mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams['ytick.labelsize'] = 20
import matplotlib.pyplot as plt
import pylab as pl
from matplotlib import rc
rc('text',usetex=True)
rc('text.latex',preamble=r'\usepackage{mathrsfs}')
rc('text.latex',preamble=r'\usepackage{sansmath}')

masssq1 = 3.0
masssq2 = 1.1
masssq3 = 0.2
masssq4 = 0.08
masssq5 = 0.01
Hend = 1.0#10.0**(-6.0)
number_of_realisations = 10000
number_of_fields = 5
Nefolds = 100.0
Number_of_Nsteps = 1000

def first_derivs_potential(field_realisations,N):
    firstderivsfN = np.zeros((number_of_realisations,number_of_fields))# Very important to initialise to zeros!!
    firstderivsfN[:,0] = masssq1*field_realisations[:,0]
    firstderivsfN[:,1] = masssq2*(field_realisations[:,1])
    firstderivsfN[:,2] = masssq3*(field_realisations[:,2])
    firstderivsfN[:,3] = masssq4*(field_realisations[:,3])
    firstderivsfN[:,4] = masssq5*(field_realisations[:,4])
    return firstderivsfN

def Hubble_function(field_realisations,N):
    return Hend

def test_variance1(field_realisations,N):
    return np.sqrt(3.0*(Hubble_function(field_realisations,N)**4.0)/(8.0*np.pi*np.pi*masssq1))

def test_variance2(field_realisations,N):
    return np.sqrt(3.0*(Hubble_function(field_realisations,N)**4.0)/(8.0*np.pi*np.pi*masssq2))

def test_variance3(field_realisations,N):
    return np.sqrt(3.0*(Hubble_function(field_realisations,N)**4.0)/(8.0*np.pi*np.pi*masssq3))

def test_variance4(field_realisations,N):
    return np.sqrt(3.0*(Hubble_function(field_realisations,N)**4.0)/(8.0*np.pi*np.pi*masssq4))

def test_variance5(field_realisations,N):
    return np.sqrt(3.0*(Hubble_function(field_realisations,N)**4.0)/(8.0*np.pi*np.pi*masssq5))

nf = nfield(path + 'nfield/',first_derivs_potential,Hubble_function,number_of_realisations,number_of_fields) 
nf.output_IR_variances('nfield_test.txt',Nefolds/float(Number_of_Nsteps),Number_of_Nsteps)

N_time_data = []
variance_data1 = []
variance_data2 = []
variance_data3 = []
variance_data4 = []
variance_data5 = []
test_variance_data1 = []
test_variance_data2 = []
test_variance_data3 = []
test_variance_data4 = []
test_variance_data5 = []
with open(path + 'nfield/data/nfield_test.txt') as file:
# Compute quantities in loop dynamically as with open(..) reads off the data file
    for line in file:
        columns = line.split()
        N_time_data.append(float(columns[0]))
        variance_data1.append(np.sqrt(float(columns[6])))
        variance_data2.append(np.sqrt(float(columns[7])))
        variance_data3.append(np.sqrt(float(columns[8])))
        variance_data4.append(np.sqrt(float(columns[9])))
        variance_data5.append(np.sqrt(float(columns[10])))
        test_variance_data1.append(test_variance1(0,float(columns[0])))
        test_variance_data2.append(test_variance2(0,float(columns[0]))) 
        test_variance_data3.append(test_variance3(0,float(columns[0]))) 
        test_variance_data4.append(test_variance4(0,float(columns[0]))) 
        test_variance_data5.append(test_variance5(0,float(columns[0]))) 
    
figure = plt.plot(N_time_data,variance_data1,color='Red',linewidth=2,label=r'$i=1$')
figure = plt.plot(N_time_data,variance_data2,color='Blue',linewidth=2,label=r'$i=2$')
figure = plt.plot(N_time_data,variance_data3,color='Green',linewidth=2,label=r'$i=3$')
figure = plt.plot(N_time_data,variance_data4,color='Pink',linewidth=2,label=r'$i=4$')
figure = plt.plot(N_time_data,variance_data5,color='Brown',linewidth=2,label=r'$i=5$')
figure = plt.plot(N_time_data,test_variance_data1,'--',color='Red',linewidth=2)
figure = plt.plot(N_time_data,test_variance_data2,'--',color='Blue',linewidth=2)
figure = plt.plot(N_time_data,test_variance_data3,'--',color='Green',linewidth=2)
figure = plt.plot(N_time_data,test_variance_data4,'--',color='Pink',linewidth=2)
figure = plt.plot(N_time_data,test_variance_data5,'--',color='Brown',linewidth=2)

axes = plt.gca()
leg=axes.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),ncol=3, fancybox=True, shadow=True,fontsize=20)
axes.set_xlabel(r"$N$",fontsize=25.0)
axes.set_ylabel(r"$\frac{\sqrt{\left\langle \chi^2_i \right\rangle }}{H_{\rm end}}$",fontsize=25.0,labelpad=35).set_rotation(0)
axes.set_yscale("log")
plt.savefig(path + 'nfield/plots/test_nfield_plot.pdf', format='pdf',bbox_inches='tight',pad_inches=0.1,dpi=300)


