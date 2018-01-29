# nfield - a python class with tools to solve for the 1-loop resummation of the correlation functions of quantum fields during inflation.
The numerical solver makes use of the Stochastic formalism (see e.g. https://arxiv.org/abs/1506.04732) and computes the IR correlation functions of fields during cosmic inflation in n-field dimensions.

# Current version

The code currently only supports the implementation of n-numbers of coupled test fields (energetically sub-dominant), though there are plans in the immediate future to include inflationary fields as well. The current example script: nfield/scripts/test_nfield.py solves for 5 test fields simultaneously. 

# Getting started

To fork, simply type into the terminal:

> git clone https://github.com/umbralcalc/nfield.git 

...then enter the scripts directory

> cd nfield/scripts

To run the test_nfield.py script immediately, you'll need to set the path to nfield on your computer. Check to make sure that you have imported all the correct modules too before runtime!
