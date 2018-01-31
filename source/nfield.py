import sys
path = ''
sys.path.append(path + 'nfield/source/')
from multilangevinsolver import multilangevinsolver 
from Distribution import Distribution

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text',usetex=True)
import pylab as pl


class nfield:
# Initialize the code


    def __init__(self,path_to_nfield_directory,first_derivs_potential,Hubble_function,number_of_field_realisations,number_of_field_dimensions,solver_choice='IE'):
    # Initialise self...
       
        self.classical_terms
        self.quantum_terms
        self.zero_field_values
        self.stationary_field_values
        self.first_derivs_potential = first_derivs_potential
        self.Hubble_function = Hubble_function
        self.number_of_field_dimensions = number_of_field_dimensions
        self.number_of_field_realisations = number_of_field_realisations
        self.MLS = multilangevinsolver(path_to_nfield_directory,self.classical_terms,self.quantum_terms)

    def classical_terms(self,field_realisations,N):
        return -self.first_derivs_potential(field_realisations,N)/(3.0*(self.Hubble_function(field_realisations,N)**2.0))

    def quantum_terms(self,field_realisations,N):
        return (self.Hubble_function(field_realisations,N)/(2.0*np.pi))*np.ones((self.number_of_field_realisations,self.number_of_field_dimensions))

    def stationary_field_values(self,field_dimension):
    # Needs generalising to dimension number
        x = np.linspace(-100, 100, 512)
        pdf = np.exp(8.0*np.pi*np.pi*((-(6.0*(H(0.0)**2.0)*xi)*x**2)-((0.5*(m**2.0))*x**2)-((0.25*lambdah)*x**4))/(3.0*(H(0.0)**4.0)))
        return float(Distribution(pdf, transform=lambda i:i-256)(1)) 

    def zero_field_values(self,field_dimension):
        return 0.0 

    def output_IR_variances(self,name_data_file,Nstepsize,Nefolds_timesteps,stationary_start=False):
        if stationary_start == True:
            self.MLS.data_evolving_moments(name_data_file,self.number_of_field_realisations,self.number_of_field_dimensions,Nstepsize,Nefolds_timesteps,self.stationary_field_values)
        else:
            self.MLS.data_evolving_moments(name_data_file,self.number_of_field_realisations,self.number_of_field_dimensions,Nstepsize,Nefolds_timesteps,self.zero_field_values)

    def output_2D_PDF(self,name_data_file,Nstepsize,Nefolds_timesteps,number_of_outputs,stationary_start=False):
        if stationary_start == True:
            self.MLS.data_prob_densities_2D(name_data_file,self.number_of_field_realisations,number_of_outputs,Nstepsize,Nefolds_timesteps,self.stationary_field_values)
        else:
            self.MLS.data_prob_densities_2D(name_data_file,self.number_of_field_realisations,number_of_outputs,Nstepsize,Nefolds_timesteps,self.zero_field_values)



