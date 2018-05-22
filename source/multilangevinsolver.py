import numpy as np

class multilangevinsolver:
# Initialize the code


    def __init__(self,path_to_multilangevinsolver_directory,drift_functions,diffusion_functions,solver_choice='IE'):
    # Initialise self...

        self.path = path_to_multilangevinsolver_directory # Set path of directory upon declaration e.g. '.../multilangevinsolver/'
        self.A = drift_functions 
        self.B = diffusion_functions
        # Setup the system with drift A(x,t) and diffusion B(x,t) functions  
        self.solver_choice = solver_choice
        # Choose which solver to use - set to Improved Euler Scheme automatically

    def Improved_Euler_Iterator(self,walker_nd,time):
    # Iterate the solver with a strong order 1 Improved Euler Scheme from https://arxiv.org/abs/1210.0933

        random_number = np.random.normal(0.0,1.0,size=(len(walker_nd),len(walker_nd[0])))
        # Generate a random number for the Weiner process

        S_alternate = np.random.normal(0.0,1.0,size=(len(walker_nd),len(walker_nd[0])))
        # Generate a random number for alternator in Ito process

        K1 = (self.A(walker_nd,time)*self.deltat) + (np.sqrt(self.deltat)*(random_number-(S_alternate/abs(S_alternate)))*self.B(walker_nd,time)) 
        K2 = (self.A(walker_nd+K1,time+self.deltat)*self.deltat) + (np.sqrt(self.deltat)*(random_number+(S_alternate/abs(S_alternate)))*self.B(walker_nd+K1,time+self.deltat)) 

        return walker_nd + (0.5*(K1+K2)) 
        # Return next step from a group of realisations 

    def data_evolving_moments(self,datafilename,number_of_realisations,number_of_dimensions,deltat,number_of_timesteps,x0_dist):
    # Output data on the 1st and 2nd moments of solutions associated to many realisations of the Langevin equation using the requested solver
  
        self.deltat = deltat
        # Set spatial and temporal initial conditions as well as the timestep

        realisations_nd = np.asarray([[x0_dist(D) for D in range(0,number_of_dimensions)] for x_value in range(0,number_of_realisations)])
        # Initialise the realisations array        

        data_file = open(self.path + 'data/' + datafilename,'w')
        # Open a data file

        for i in range(0,number_of_timesteps):
        # Initialise loop over time
            
            time = float(i)*deltat*np.ones((number_of_realisations,number_of_dimensions))
            # Take a new step forward in time and set an appropriate dimension array of identical 'times'

            if self.solver_choice == 'IE': 
                realisations_nd = self.Improved_Euler_Iterator(realisations_nd,time)
                # Iterate the Improved Euler solver for the realisations array
                data_file.write(str(float(i)*deltat) + "\t" + "\t".join(map(str, np.sum(realisations_nd,axis=0)/float(number_of_realisations))) + "\t" + "\t".join(map(str, np.sum(realisations_nd**2,axis=0)/float(number_of_realisations))) + "\n") # Continuously output to the data file
    
        data_file.close()
        # Close the data file

    def data_realisations_ND(self,datafilename,number_of_realisations,output_values_t,number_of_dimensions,deltat,number_of_timesteps,x0_dist):
    # Output multiple snapshots of realisations to compute the probability density in N dimensions computed using the requested solver
  
        self.deltat = deltat
        # Set spatial and temporal initial conditions as well as the timestep

        realisations_nd = np.asarray([[x0_dist(D) for D in range(0,number_of_dimensions)] for x_value in range(0,number_of_realisations)])
        # Initialise the realisations array        

        output_indices = [int(output_values_t[i]/float(deltat)) for i in range(0,len(output_values_t))]
        # Prepare a list of indices to mark the timescales of each plot

        j = 0 
        for i in range(0,number_of_timesteps):
        # Initialise loop over time
            
            time = float(i)*deltat*np.ones((number_of_realisations,number_of_dimensions))
            # Take a new step forward in time and set an appropriate dimension array of identical 'times'

            if self.solver_choice == 'IE': 
                realisations_nd = self.Improved_Euler_Iterator(realisations_nd,time)
                # Iterate the Improved Euler solver for the realisations array

                if i == output_indices[j]:
                    data_file = open(self.path + 'data/' + 'time' + str(j) + '_' + datafilename,'w')
                    # Open a new data file

                    realisations_string_list = map(str, realisations_nd)
                    realisations_string_list = [rsl.strip('[]') for rsl in realisations_string_list]
                    # Remove tedious brackets from the output

                    data_file.write("\n".join(realisations_string_list)) 
                    # Continuously output to the data file

                    data_file.close()
                    # Close the data file

                    if j < len(output_indices)-1: j += 1 
                    # Iterate over j to move to the next plot output unless no more are required


    def data_realisations_ND_gen_init_cond(self,datafilename,number_of_realisations,output_values_t,number_of_dimensions,deltat,number_of_timesteps,x0_dist):
    # Output multiple snapshots of realisations to compute the probability density in N dimensions computed using the requested solver
    # This function allows for the user to insert an array of initial samples directly through x0_dist
  
        self.deltat = deltat
        # Set spatial and temporal initial conditions as well as the timestep

        realisations_nd = x0_dist
        # Initialise the realisations array        

        output_indices = [int(output_values_t[i]/float(deltat)) for i in range(0,len(output_values_t))]
        # Prepare a list of indices to mark the timescales of each plot

        j = 0 
        for i in range(0,number_of_timesteps):
        # Initialise loop over time
            
            time = float(i)*deltat*np.ones((number_of_realisations,number_of_dimensions))
            # Take a new step forward in time and set an appropriate dimension array of identical 'times'

            if self.solver_choice == 'IE': 
                realisations_nd = self.Improved_Euler_Iterator(realisations_nd,time)
                # Iterate the Improved Euler solver for the realisations array

                if i == output_indices[j]:
                    data_file = open(self.path + 'data/' + 'time' + str(j) + '_' + datafilename,'w')
                    # Open a new data file

                    realisations_string_list = map(str, realisations_nd)
                    realisations_string_list = [rsl.strip('[]') for rsl in realisations_string_list]
                    # Remove tedious brackets from the output

                    data_file.write("\n".join(realisations_string_list)) 
                    # Continuously output to the data file

                    data_file.close()
                    # Close the data file

                    if j <= len(output_indices)-1: 
                        j += 1
                        if j >= len(output_indices): j = 0 
                    # Iterate over j to move to the next plot output unless no more are required

   
