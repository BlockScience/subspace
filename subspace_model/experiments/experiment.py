from copy import deepcopy

import numpy as np
import pandas as pd
from cadCAD_tools import easy_run  # type: ignore
from cadCAD_tools.preparation import sweep_cartesian_product
from pandas import DataFrame

from subspace_model.const import *
from subspace_model.experiments.logic import (
    DEFAULT_ISSUANCE_FUNCTION,
    MOCK_ISSUANCE_FUNCTION,
    MOCK_ISSUANCE_FUNCTION_2,
    NORMAL_GENERATOR,
    POISSON_GENERATOR,
    POSITIVE_INTEGER,
    SUPPLY_EARNED,
    SUPPLY_EARNED_MINUS_BURNED,
    SUPPLY_ISSUED,
    SUPPLY_TOTAL,
    TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50,
    TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS,
    SubsidyComponent,
)
from subspace_model.params import DEFAULT_PARAMS, INITIAL_STATE, ISSUANCE_FOR_FARMERS
from subspace_model.structure import SUBSPACE_MODEL_BLOCKS
from subspace_model.types import SubspaceModelParams


def sanity_check_run(
    SIMULATION_DAYS: int = 700, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 1
) -> DataFrame:
    """
    This experiment tests the model with default parameters and with deterministic parameters.

    Returns:
        DataFrame: A dataframe of simulation data
    """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep params in the form of single length arrays
    sweep_params = {k: [v] for k, v in DEFAULT_PARAMS.items()}

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(
        *sim_args,
        assign_params={
            'label',
            'environmental_label',
            'timestep_in_days',
            'block_time_in_seconds',
            'max_credit_supply',
        },
    )
    return sim_df


def standard_stochastic_run(
    SIMULATION_DAYS: int = 700, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 5
) -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep parameters in the form of single length arrays
    param_set = deepcopy(DEFAULT_PARAMS)
    param_set['label'] = 'deterministic'
    param_set['base_fee_function'] = POSITIVE_INTEGER(NORMAL_GENERATOR(1, 1))
    param_set['priority_fee_function'] = POSITIVE_INTEGER(NORMAL_GENERATOR(3, 5))
    param_set['compute_weights_per_tx_function'] = POSITIVE_INTEGER(
        NORMAL_GENERATOR(60_000_000, 15_000_000)
    )
    param_set['compute_weight_per_bundle_function'] = POSITIVE_INTEGER(
        NORMAL_GENERATOR(10_000_000_000, 5_000_000_000)
    )
    param_set['transaction_size_function'] = POSITIVE_INTEGER(
        NORMAL_GENERATOR(256, 100)
    )
    param_set['bundle_size_function'] = POSITIVE_INTEGER(NORMAL_GENERATOR(1500, 1000))
    param_set['transaction_count_per_day_function'] = POISSON_GENERATOR(
        1 * BLOCKS_PER_DAY
    )

    param_set['bundle_count_per_day_function'] = POISSON_GENERATOR(6 * BLOCKS_PER_DAY)
    param_set['slash_per_day_function'] = POISSON_GENERATOR(0.1)
    param_set['new_sectors_per_day_function'] = POSITIVE_INTEGER(
        NORMAL_GENERATOR(1000, 500)
    )

    # Get the sweep params in the form of single length arrays
    sweep_params = {k: [v] for k, v in param_set.items()}

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(
        *sim_args,
        assign_params={
            'label',
            'environmental_label',
            'timestep_in_days',
            'block_time_in_seconds',
            'max_credit_supply',
        },
    )
    return sim_df


def issuance_sweep(
    SIMULATION_DAYS: int = 700, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 1
) -> DataFrame:
    """Sweeps issuance functions.

    Returns:
        DataFrame: A dataframe of simulation data
    """

    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep params in the form of single length arrays
    param_set_1 = DEFAULT_PARAMS
    param_set_1['label'] = 'default-issuance-function'
    param_set_2 = deepcopy(DEFAULT_PARAMS)
    param_set_2['label'] = 'mock-issuance-function'
    param_set_2['issuance_function'] = MOCK_ISSUANCE_FUNCTION
    param_set_3 = deepcopy(DEFAULT_PARAMS)
    param_set_3['label'] = 'mock-issuance-function-2'
    param_set_3['issuance_function'] = MOCK_ISSUANCE_FUNCTION_2
    param_sets = [param_set_1, param_set_2, param_set_3]

    sweep_params: dict[str, list] = {k: [] for k in DEFAULT_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(
        *sim_args,
        assign_params={
            'label',
            'environmental_label',
            'timestep_in_days',
            'block_time_in_seconds',
            'max_credit_supply',
        },
    )
    return sim_df


def fund_inclusion(
    SIMULATION_DAYS: int = 700, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 1
) -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep parameters in the form of single length arrays
    param_set_1 = DEFAULT_PARAMS
    param_set_2 = deepcopy(DEFAULT_PARAMS)
    param_set_2['label'] = 'no-fund'
    param_set_2['fund_tax_on_proposer_reward'] = 0
    param_set_2['fund_tax_on_storage_fees'] = 0
    param_set_2['slash_to_fund'] = 0
    param_sets = [param_set_1, param_set_2]

    # Create the sweep parameters dictionary
    sweep_params: dict[str, list] = {k: [] for k in DEFAULT_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(
        *sim_args,
        assign_params={
            'label',
            'environmental_label',
            'timestep_in_days',
            'block_time_in_seconds',
            'max_credit_supply',
        },
    )

    # Return the simulation results dataframe
    return sim_df


def reward_split_sweep(
    SIMULATION_DAYS: int = 700,
    TIMESTEP_IN_DAYS: int = 1,
    SAMPLES: int = 1,
) -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep params in the form of single length arrays
    param_set_1 = DEFAULT_PARAMS
    param_set_2 = deepcopy(DEFAULT_PARAMS)
    param_set_2['label'] = 'alternate-split'
    param_set_2['reward_proposer_share'] = 0.5

    param_sets = [param_set_1, param_set_2]

    sweep_params: dict[str, list] = {k: [] for k in DEFAULT_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(
        *sim_args,
        assign_params={
            'label',
            'environmental_label',
            'timestep_in_days',
            'block_time_in_seconds',
            'max_credit_supply',
        },
    )
    return sim_df


def sweep_credit_supply(
    SIMULATION_DAYS: int = 700,
    TIMESTEP_IN_DAYS: int = 1,
    SAMPLES: int = 1,
) -> DataFrame:
    """ """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep params in the form of single length arrays
    param_set_1 = deepcopy(DEFAULT_PARAMS)
    param_set_1['label'] = 'supply-issued'
    param_set_1['environmental_label'] = 'constant-utilization'
    param_set_1['credit_supply_definition'] = SUPPLY_ISSUED
    param_set_1[
        'transaction_count_per_day_function'
    ] = TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50

    param_set_2 = deepcopy(DEFAULT_PARAMS)
    param_set_2['label'] = 'supply-earned'
    param_set_2['environmental_label'] = 'constant-utilization'
    param_set_2['credit_supply_definition'] = SUPPLY_EARNED
    param_set_2[
        'transaction_count_per_day_function'
    ] = TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50

    param_set_3 = deepcopy(DEFAULT_PARAMS)
    param_set_3['label'] = 'supply-earned-minus-burned'
    param_set_3['environmental_label'] = 'constant-utilization'
    param_set_3['credit_supply_definition'] = SUPPLY_EARNED_MINUS_BURNED
    param_set_3[
        'transaction_count_per_day_function'
    ] = TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50

    param_set_4 = deepcopy(DEFAULT_PARAMS)
    param_set_4['label'] = 'supply-issued'
    param_set_4['environmental_label'] = 'growing-utilization'
    param_set_4['credit_supply_definition'] = SUPPLY_ISSUED
    param_set_4[
        'transaction_count_per_day_function'
    ] = TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS

    param_set_5 = deepcopy(DEFAULT_PARAMS)
    param_set_5['label'] = 'supply-earned'
    param_set_5['environmental_label'] = 'growing-utilization'
    param_set_5['credit_supply_definition'] = SUPPLY_EARNED
    param_set_5[
        'transaction_count_per_day_function'
    ] = TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS

    param_set_6 = deepcopy(DEFAULT_PARAMS)
    param_set_6['label'] = 'supply-earned-minus-burned'
    param_set_6['environmental_label'] = 'growing-utilization'
    param_set_6['credit_supply_definition'] = SUPPLY_EARNED_MINUS_BURNED
    param_set_6[
        'transaction_count_per_day_function'
    ] = TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS

    param_sets = [
        param_set_1,
        param_set_2,
        param_set_3,
        param_set_4,
        param_set_5,
        param_set_6,
    ]

    sweep_params: dict[str, list] = {k: [] for k in DEFAULT_PARAMS.keys()}
    for param_set in param_sets:
        for k, v in param_set.items():
            sweep_params[k].append(v)

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(
        *sim_args,
        assign_params={
            'label',
            'environmental_label',
            'timestep_in_days',
            'block_time_in_seconds',
            'max_credit_supply',
        },
    )
    return sim_df


def sweep_over_single_component_and_credit_supply(
    SIMULATION_DAYS: int = 700,
    TIMESTEP_IN_DAYS: int = 1,
    SAMPLES: int = 1,
) -> DataFrame:
    """ """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    c_params = np.linspace(start=0.1, stop=10, num=3)
    credit_supply_definition_params = [SUPPLY_ISSUED, SUPPLY_TOTAL]
    reference_subsidy_x_1_params = np.linspace(
        start=1 * BLOCKS_PER_MONTH, stop=2 * BLOCKS_PER_MONTH, num=3
    )
    reference_subsidy_x_2_params = np.linspace(
        start=0.1 * MAX_CREDIT_ISSUANCE, stop=0.2 * MAX_CREDIT_ISSUANCE, num=3
    )

    params = {
        'issuance_function_constant': c_params,
        'credit_supply_definition': credit_supply_definition_params,
        'reference_subsidy_x_1': reference_subsidy_x_1_params,
        'reference_subsidy_x_2': reference_subsidy_x_2_params,
    }

    sweep_params = sweep_cartesian_product(params)

    sweep_params['reference_subsidy_x_3'] = [
        x2 / x1
        for x1, x2 in zip(
            sweep_params['reference_subsidy_x_1'], sweep_params['reference_subsidy_x_2']
        )
    ]

    sweep_params['reference_subsidy_components'] = [
        [
            SubsidyComponent(0, x1, x2, x3),
        ]
        for x1, x2, x3 in zip(
            sweep_params['reference_subsidy_x_1'],
            sweep_params['reference_subsidy_x_2'],
            sweep_params['reference_subsidy_x_3'],
        )
    ]

    sweep_params.pop('reference_subsidy_x_1', None)
    sweep_params.pop('reference_subsidy_x_2', None)
    sweep_params.pop('reference_subsidy_x_3', None)

    sweep_params = {**{k: [v] for k, v in DEFAULT_PARAMS.items()}, **sweep_params}

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(
        *sim_args,
        assign_params={
            'label',
            'environmental_label',
            'timestep_in_days',
            'block_time_in_seconds',
            'max_credit_supply',
        },
    )
    return sim_df
