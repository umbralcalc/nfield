# nfield - a stochastic tool for QFT on inflationary backgrounds

<a href="http://ascl.net/1807.011"><img src="https://img.shields.io/badge/ascl-1807.011-blue.svg?colorB=262255" alt="ascl:1807.011" /></a>

The numerical solver makes use of the stochastic formalism (see [https://arxiv.org/abs/1803.03521]) and computes the IR correlation functions of quantum fields during cosmic inflation in n-field dimensions. This is a necessary 1-loop resummation of the correlation functions to render them finite.

# Current version

The code now supports the implementation of n-numbers of coupled test fields (energetically sub-dominant) as well as non-test fields. The current example script: nfield/scripts/test_nfield.py solves for 5 test fields simultaneously. 

# Getting started

To fork, simply type into the terminal:

> git clone https://github.com/umbralcalc/nfield.git 

...then enter the scripts directory

> cd nfield/scripts

To run the test_nfield.py script immediately, you'll need to set the path to nfield on your computer. Check to make sure that you have imported all the correct modules too before runtime!
