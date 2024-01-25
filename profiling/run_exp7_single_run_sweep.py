import os, sys
import matplotlib.pyplot as plt
import pandas as pd
sys.path.append("../..")
sys.path.append("..")

from subspace_model.__main__ import experiments

experiments['sweep_over_single_component_and_credit_supply'](SAMPLES=1, N_PARAM_SWEEP=1)