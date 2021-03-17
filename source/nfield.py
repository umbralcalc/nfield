import numpy as np
from mlsolver import mlsolver

class nfield(mlsolver):

    def __init__(self, gradV, H, solver='IE'):
        """
        Class implementing mlsolver in the context of stochastic inflation.

        Args:
        gradV
            gradient of the potential
        H
            the hubble parameter function H(phi,N)
        
        """
       
        self.gradV = gradV
        self.H = H
        super().__init__(self.classical_terms, self.quantum_terms, solver=solver)

    def classical_terms(self, phi : np.ndarray, N : float) -> np.ndarray:
        """Slow-roll drift term"""
        return -self.gradV(phi, N)/(3.0*(self.H(phi,N)**2.0))

    def quantum_terms(self, phi : np.ndarray, N : float) -> np.ndarray:
        """Stochastic noise sourced by quantum diffusion"""
        return (self.H(phi,N)/(2.0*np.pi))*np.ones((self.dimensions,self.realisations))


