from copy import deepcopy

import pandas as pd

# import panel as pn
from cadCAD_tools import easy_run  # type: ignore
from pandas import DataFrame

from subspace_model.const import *
from subspace_model.experiments.logic import (
    DEFAULT_ISSUANCE_FUNCTION,
    MOCK_ISSUANCE_FUNCTION,
    MOCK_ISSUANCE_FUNCTION_2,
    NORMAL_GENERATOR,
    POISSON_GENERATOR,
)
from subspace_model.params import DEFAULT_PARAMS, INITIAL_STATE, ISSUANCE_FOR_FARMERS
from subspace_model.structure import SUBSPACE_MODEL_BLOCKS
from subspace_model.types import SubspaceModelParams


# @pn.cache(to_disk=True)
def sanity_check_run(
    SIMULATION_DAYS: int = 700, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 1
) -> DataFrame:
    """
    This experiment tests the model with default parameters and with deterministic parameters.

    Returns:
        DataFrame: A dataframe of simulation data
    """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep parameters in the form of single length arrays
    param_set_1 = DEFAULT_PARAMS
    param_set_2 = deepcopy(DEFAULT_PARAMS)
    param_set_2["label"] = "deterministic"
    param_set_2["base_fee_function"] = lambda p, s: 1
    param_set_2["priority_fee_function"] = lambda p, s: 3
    param_set_2["compute_weights_per_tx_function"] = lambda p, s: 60_000_000
    param_set_2["compute_weight_per_bundle_function"] = lambda p, s: 10_000_000_000
    param_set_2["transaction_size_function"] = lambda p, s: 256
    param_set_2["bundle_size_function"] = lambda p, s: 1500
    param_set_2["transaction_count_per_day_function"] = lambda p, s: 1 * BLOCKS_PER_DAY
    param_set_2["bundle_count_per_day_function"] = lambda p, s: 6 * BLOCKS_PER_DAY
    param_set_2["slash_per_day_function"] = lambda p, s: 0.1
    param_set_2["new_sectors_per_day_function"] = lambda p, s: 1000
    param_sets = [param_set_1, param_set_2]

    # Create the sweep parameters dictionary
    sweep_params: dict[str, list] = {k: [] for k in DEFAULT_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df


# @pn.cache(to_disk=True)
def standard_stochastic_run(
    SIMULATION_DAYS: int = 700, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 5
) -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep params in the form of single length arrays
    sweep_params = {k: [v] for k, v in DEFAULT_PARAMS.items()}

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df


# @pn.cache(to_disk=True)
def issuance_sweep(
    SIMULATION_DAYS: int = 700, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 2
) -> DataFrame:
    """Sweeps issuance functions.

    Returns:
        DataFrame: A dataframe of simulation data
    """

    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # %%
    # Get the sweep params in the form of single length arrays

    param_set_1 = DEFAULT_PARAMS
    param_set_1["label"] = "default-issuance-function"
    param_set_2 = deepcopy(DEFAULT_PARAMS)
    param_set_2["label"] = "mock-issuance-function"
    param_set_2["issuance_function"] = MOCK_ISSUANCE_FUNCTION
    param_set_3 = deepcopy(DEFAULT_PARAMS)
    param_set_3["label"] = "mock-issuance-function-2"
    param_set_3["issuance_function"] = MOCK_ISSUANCE_FUNCTION_2
    param_sets = [param_set_1, param_set_2, param_set_3]

    sweep_params: dict[str, list] = {k: [] for k in DEFAULT_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df


# @pn.cache(to_disk=True)
def fund_inclusion(
    SIMULATION_DAYS: int = 700, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 5
) -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep parameters in the form of single length arrays
    param_set_1 = DEFAULT_PARAMS
    param_set_2 = deepcopy(DEFAULT_PARAMS)
    param_set_2["label"] = "no-fund"
    param_set_2["fund_tax_on_proposer_reward"] = 0
    param_set_2["fund_tax_on_storage_fees"] = 0
    param_set_2["slash_to_fund"] = 0
    param_sets = [param_set_1, param_set_2]

    # Create the sweep parameters dictionary
    sweep_params: dict[str, list] = {k: [] for k in DEFAULT_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)

    # Return the simulation results dataframe
    return sim_df


# @pn.cache(to_disk=True)
def reward_split_sweep(
    SIMULATION_DAYS: int = 700,
    TIMESTEP_IN_DAYS: int = 1,
    SAMPLES: int = 15,
) -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # %%
    # Get the sweep params in the form of single length arrays

    param_set_1 = DEFAULT_PARAMS
    param_set_2 = deepcopy(DEFAULT_PARAMS)
    param_set_2["label"] = "alternate-split"
    param_set_2["reward_proposer_share"] = 0.5

    param_sets = [param_set_1, param_set_2]

    sweep_params: dict[str, list] = {k: [] for k in DEFAULT_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df
