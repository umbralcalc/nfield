import numpy as np
from mlsolver import mlsolver

class nfield(mlsolver):

    def __init__(self,first_derivs_potential,Hubble_function,number_of_field_realisations,number_of_field_dimensions,solver='IE'):
       
        super().__init__(self.classical_terms(), self.quantum_terms(), solver=solver)
        self.zero_field_values
        self.stationary_field_values
        self.initial_condition_function
        self.init_cond_list = []
        self.first_derivs_potential = first_derivs_potential
        self.Hubble_function = Hubble_function
        self.number_of_field_dimensions = number_of_field_dimensions
        self.number_of_field_realisations = number_of_field_realisations
        self.MLS = multilangevinsolver(path_to_nfield_directory,self.classical_terms,self.quantum_terms)

    def classical_terms(self,field_realisations,N):
        return -self.first_derivs_potential(field_realisations,N)/(3.0*(self.Hubble_function(field_realisations,N)**2.0))
        # Set the classical slow-roll inflation terms

    def quantum_terms(self,field_realisations,N):
        return (self.Hubble_function(field_realisations,N)/(2.0*np.pi))*np.ones((self.number_of_field_realisations,self.number_of_field_dimensions))
        # Set the quantum noise terms

    def stationary_field_values(self,field_dimension):
    # Needs generalising to dimension number and potential type before full implementation
        x = np.linspace(-100, 100, 512)
        pdf = np.exp(8.0*np.pi*np.pi*((-(6.0*(H(0.0)**2.0)*xi)*x**2)-((0.5*(m**2.0))*x**2)-((0.25*lambdah)*x**4))/(3.0*(H(0.0)**4.0)))
        return float(Distribution(pdf, transform=lambda i:i-256)(1)) 

    def zero_field_values(self,field_dimension):
    # Option to begin at zero for all field values
        return 0.0 

    def initial_condition_function(self,field_dimension):
    # Option to insert samples by hand as a set initial condition for the process
        return self.init_cond_list[field_dimension]

    def output_IR_variances(self,name_data_file,Nstepsize,Nefolds_timesteps,initial_condition=None):
    # Option to output the first and second moments for all fields
        if initial_condition:
            self.init_cond_list = initial_condition
            self.MLS.data_evolving_moments(name_data_file,self.number_of_field_realisations,self.number_of_field_dimensions,Nstepsize,Nefolds_timesteps,self.initial_condition_function)
        else:
            self.MLS.data_evolving_moments(name_data_file,self.number_of_field_realisations,self.number_of_field_dimensions,Nstepsize,Nefolds_timesteps,self.zero_field_values)

    def output_ND_PDF_data(self,name_data_file,Nstepsize,Nefolds_timesteps,output_Ns,initial_condition=None):
    # Option to output the direct samples of the process
        if initial_condition:
            self.init_cond_list = initial_condition
            self.MLS.data_realisations_ND(name_data_file,self.number_of_field_realisations,output_Ns,self.number_of_field_dimensions,Nstepsize,Nefolds_timesteps,self.initial_condition_function)
        else:
            self.MLS.data_realisations_ND(name_data_file,self.number_of_field_realisations,output_Ns,self.number_of_field_dimensions,Nstepsize,Nefolds_timesteps,self.zero_field_values)

    def output_ND_PDF_data_gen_init_cond(self,name_data_file,Nstepsize,Nefolds_timesteps,output_Ns,initial_condition_array):
    # Use this for a generic initial condition set by hands
        self.MLS.data_realisations_ND_gen_init_cond(name_data_file,self.number_of_field_realisations,output_Ns,self.number_of_field_dimensions,Nstepsize,Nefolds_timesteps,initial_condition_array)

    def PDF_at_condition_point_ND_gen_init_cond(self,name_data_file,Nstepsize,Nefolds_timesteps,output_cond_list,spec_func,initial_condition_array):
    # Use this to output pdf samples at a point given by a specific condition with generic initial conditions
        self.MLS.PDF_at_condition_point_ND_gen_init_cond(name_data_file,self.number_of_field_realisations,output_cond_list,spec_func,self.number_of_field_dimensions,Nstepsize,Nefolds_timesteps,initial_condition_array)



