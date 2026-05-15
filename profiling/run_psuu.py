import os, sys
import matplotlib.pyplot as plt
import pandas as pd
sys.path.append("../..")
sys.path.append("..")

from subspace_model.__main__ import experiments

experiments['psuu'](SAMPLES=1, N_SWEEP_SAMPLES=10, SIMULATION_DAYS=365*4, PARALLELIZE=False, RETURN_SIM_DF=False)