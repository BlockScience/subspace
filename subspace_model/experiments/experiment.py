from copy import deepcopy

import pandas as pd
import panel as pn
from cadCAD_tools import easy_run  # type: ignore
from pandas import DataFrame

from subspace_model.const import *
from subspace_model.experiments.logic import (
    DEFAULT_ISSUANCE_FUNCTION,
    ISSUANCE_FUNCTION,
)
from subspace_model.params import BASE_PARAMS, INITIAL_STATE, ISSUANCE_FOR_FARMERS
from subspace_model.structure import SUBSPACE_MODEL_BLOCKS
from subspace_model.types import SubspaceModelParams


@pn.cache(to_disk=True)
def standard_run() -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    # The number of timesteps for each simulation to run
    N_timesteps = 360

    # The number of monte carlo runs per set of parameters tested
    N_samples = 1
    # %%
    # Get the sweep params in the form of single length arrays
    sweep_params = {k: [v] for k, v in BASE_PARAMS.items()}

    # Load simulation arguments
    sim_args = (
        INITIAL_STATE,
        sweep_params,
        SUBSPACE_MODEL_BLOCKS,
        N_timesteps,
        N_samples,
    )

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df


@pn.cache(to_disk=True)
def sanity_check_run() -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    SIMULATION_DAYS = 700
    TIMESTEP_IN_DAYS = 1
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1
    SAMPLES = 1

    # print("BASE_PARAMS['deterministic']=", BASE_PARAMS["deterministic"])

    # %%
    # Get the sweep params in the form of single length arrays
    sweep_params = {k: [v] for k, v in BASE_PARAMS.items()}

    print(sweep_params)
    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df


@pn.cache(to_disk=True)
def sanity_check_deterministic_run() -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    SIMULATION_DAYS = 700
    TIMESTEP_IN_DAYS = 1
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1
    SAMPLES = 1

    BASE_PARAMS['deterministic'] = True
    # print("BASE_PARAMS['deterministic']=", BASE_PARAMS["deterministic"])

    # %%
    # Get the sweep params in the form of single length arrays
    sweep_params = {k: [v] for k, v in BASE_PARAMS.items()}

    print(sweep_params)
    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df


@pn.cache(to_disk=True)
def standard_stochastic_run() -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    SIMULATION_DAYS = 700
    TIMESTEP_IN_DAYS = 1
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1
    SAMPLES = 30

    # %%
    # Get the sweep params in the form of single length arrays
    sweep_params = {k: [v] for k, v in BASE_PARAMS.items()}

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df


@pn.cache(to_disk=True)
def escrow_inclusion_sweep_run(
    fund_tax_on_proposer_reward=0,
    fund_tax_on_storage_fees=0,
    slash_to_fund=0,
    SIMULATION_DAYS=700,
    SAMPLES=15,
) -> DataFrame:
    SIMULATION_DAYS = SIMULATION_DAYS
    TIMESTEP_IN_DAYS = 1
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1
    SAMPLES = SAMPLES

    # %%
    # Get the sweep params in the form of single length arrays

    param_set_1 = BASE_PARAMS
    param_set_2 = deepcopy(BASE_PARAMS)
    param_set_2['label'] = 'no-fund'
    param_set_2['fund_tax_on_proposer_reward'] = fund_tax_on_proposer_reward
    param_set_2['fund_tax_on_storage_fees'] = fund_tax_on_storage_fees
    param_set_2['slash_to_fund'] = slash_to_fundvf

    param_sets = [param_set_1, param_set_2]

    sweep_params: dict[str, list] = {k: [] for k in BASE_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df


@pn.cache(to_disk=True)
def issuance_sweep() -> DataFrame:
    SIMULATION_DAYS = 700
    TIMESTEP_IN_DAYS = 1
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1
    SAMPLES = 15

    # %%
    # Get the sweep params in the form of single length arrays

    param_set_1 = BASE_PARAMS
    param_set_2 = deepcopy(BASE_PARAMS)
    param_set_2['label'] = 'alternate-issuance-function'
    param_set_2['issuance_function'] = lambda _: ISSUANCE_FOR_FARMERS / 5 * 365

    param_sets = [param_set_1, param_set_2]

    sweep_params: dict[str, list] = {k: [] for k in BASE_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df


@pn.cache(to_disk=True)
def reward_split_sweep() -> DataFrame:
    SIMULATION_DAYS = 700
    TIMESTEP_IN_DAYS = 1
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1
    SAMPLES = 15

    # %%
    # Get the sweep params in the form of single length arrays

    param_set_1 = BASE_PARAMS
    param_set_2 = deepcopy(BASE_PARAMS)
    param_set_2['label'] = 'alternate-split'
    param_set_2['reward_proposer_share'] = 0.5

    param_sets = [param_set_1, param_set_2]

    sweep_params: dict[str, list] = {k: [] for k in BASE_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df
