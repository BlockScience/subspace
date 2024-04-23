from copy import deepcopy

import numpy as np
import pandas as pd
from cadCAD.tools import easy_run  # type: ignore
from cadCAD.tools.preparation import sweep_cartesian_product  # type: ignore
from pandas import DataFrame
from random import sample
from datetime import datetime
from joblib import Parallel, delayed  # type: ignore
from glob import glob
import re
from tqdm.auto import tqdm # type: ignore
import logging
from pathlib import Path

logger = logging.getLogger('subspace-digital-twin')


from subspace_model.const import *
from subspace_model.experiments.logic import (
    DEFAULT_ISSUANCE_FUNCTION,
    MOCK_ISSUANCE_FUNCTION,
    MOCK_ISSUANCE_FUNCTION_2,
    NORMAL_GENERATOR,
    POISSON_GENERATOR,
    POSITIVE_INTEGER,
    REFERENCE_SUBSIDY_CONSTANT_SINGLE_COMPONENT,
    REFERENCE_SUBSIDY_HYBRID_SINGLE_COMPONENT,
    REFERENCE_SUBSIDY_HYBRID_TWO_COMPONENTS,
    SUPPLY_EARNED,
    SUPPLY_EARNED_MINUS_BURNED,
    SUPPLY_ISSUED,
    SUPPLY_TOTAL,
    TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50,
    TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS,
    SubsidyComponent,
)
from subspace_model.params import (
    DEFAULT_PARAMS,
    ENVIRONMENTAL_SCENARIOS,
    SPECIAL_ENVIRONMENTAL_SCENARIOS,
    GOVERNANCE_SURFACE,
)
from subspace_model.state import INITIAL_STATE, ISSUANCE_FOR_FARMERS
from subspace_model.structure import SUBSPACE_MODEL_BLOCKS
from subspace_model.types import SubspaceModelParams


def sanity_check_run(
    SIMULATION_DAYS: int = 183, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 1
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
            "label",
            "environmental_label",
            "timestep_in_days",
            "block_time_in_seconds",
            "max_credit_supply",
        },
        exec_mode="single",
        deepcopy_off=True,
        supress_print=True
    )
    return sim_df


def standard_stochastic_run(
    SIMULATION_DAYS: int = 183, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 5
) -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep parameters in the form of single length arrays
    param_set = deepcopy(DEFAULT_PARAMS)

    sweep_params = {
        **{k: [v] for k, v in param_set.items()},
        **{k: [v] for k, v in SPECIAL_ENVIRONMENTAL_SCENARIOS["stochastic"].items()},
    }

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(
        *sim_args,
        assign_params={
            "label",
            "environmental_label",
            "timestep_in_days",
            "block_time_in_seconds",
            "max_credit_supply",
        },
        exec_mode="single",
        deepcopy_off=True,
        supress_print=True
    )
    return sim_df


def issuance_sweep(
    SIMULATION_DAYS: int = 183, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 1
) -> DataFrame:
    """Sweeps issuance functions.

    Returns:
        DataFrame: A dataframe of simulation data
    """

    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

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
    sim_df = easy_run(
        *sim_args,
        assign_params={
            "label",
            "environmental_label",
            "timestep_in_days",
            "block_time_in_seconds",
            "max_credit_supply",
        },
        exec_mode="single",
        deepcopy_off=True,
        supress_print=True
    )
    return sim_df


def fund_inclusion(
    SIMULATION_DAYS: int = 183, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 1
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
    sim_df = easy_run(
        *sim_args,
        assign_params={
            "label",
            "environmental_label",
            "timestep_in_days",
            "block_time_in_seconds",
            "max_credit_supply",
        },
        exec_mode="single",
        deepcopy_off=True,
        supress_print=True
    )

    # Return the simulation results dataframe
    return sim_df


def reward_split_sweep(
    SIMULATION_DAYS: int = 183,
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
    sim_df = easy_run(
        *sim_args,
        assign_params={
            "label",
            "environmental_label",
            "timestep_in_days",
            "block_time_in_seconds",
            "max_credit_supply",
        },
        exec_mode="single",
        deepcopy_off=True,
        supress_print=True
    )
    return sim_df


def sweep_credit_supply(
    SIMULATION_DAYS: int = 183,
    TIMESTEP_IN_DAYS: int = 1,
    SAMPLES: int = 1,
) -> DataFrame:
    """ """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep params in the form of single length arrays
    param_set_1 = deepcopy(DEFAULT_PARAMS)
    param_set_1["label"] = "supply-issued"
    param_set_1["credit_supply_definition"] = SUPPLY_ISSUED
    param_set_1["environmental_label"] = "constant-utilization"
    param_set_1["transaction_count_per_day_function"] = (
        TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50
    )

    param_set_2 = deepcopy(DEFAULT_PARAMS)
    param_set_2["label"] = "supply-earned"
    param_set_2["credit_supply_definition"] = SUPPLY_EARNED
    param_set_2["environmental_label"] = "constant-utilization"
    param_set_2["transaction_count_per_day_function"] = (
        TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50
    )

    param_set_3 = deepcopy(DEFAULT_PARAMS)
    param_set_3["label"] = "supply-earned-minus-burned"
    param_set_3["credit_supply_definition"] = SUPPLY_EARNED_MINUS_BURNED
    param_set_3["environmental_label"] = "constant-utilization"
    param_set_3["transaction_count_per_day_function"] = (
        TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50
    )

    param_set_4 = deepcopy(DEFAULT_PARAMS)
    param_set_4["label"] = "supply-issued"
    param_set_4["credit_supply_definition"] = SUPPLY_ISSUED
    param_set_4["environmental_label"] = "growing-utilization"
    param_set_4["transaction_count_per_day_function"] = (
        TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS
    )

    param_set_5 = deepcopy(DEFAULT_PARAMS)
    param_set_5["label"] = "supply-earned"
    param_set_5["credit_supply_definition"] = SUPPLY_EARNED
    param_set_5["environmental_label"] = "growing-utilization"
    param_set_5["transaction_count_per_day_function"] = (
        TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS
    )

    param_set_6 = deepcopy(DEFAULT_PARAMS)
    param_set_6["label"] = "supply-earned-minus-burned"
    param_set_6["credit_supply_definition"] = SUPPLY_EARNED_MINUS_BURNED
    param_set_6["environmental_label"] = "growing-utilization"
    param_set_6["transaction_count_per_day_function"] = (
        TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS
    )

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
            "label",
            "environmental_label",
            "timestep_in_days",
            "block_time_in_seconds",
            "max_credit_supply",
        },
        exec_mode="single",
        deepcopy_off=True,
        supress_print=True
    )
    return sim_df


# def sweep_over_single_component_and_credit_supply(
#     SIMULATION_DAYS: int = 183 / 2,
#     TIMESTEP_IN_DAYS: int = 1,
#     SAMPLES: int = 1,
#     N_PARAM_SWEEP: int = 1,
# ) -> DataFrame:
#     """ """
#     TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1
#
#     c_params = np.linspace(start=0.1, stop=10, num=N_PARAM_SWEEP)
#     credit_supply_definition_params = [SUPPLY_TOTAL]
#     reference_subsidy_x_1_params = np.linspace(
#         start=1 * BLOCKS_PER_MONTH, stop=2 * BLOCKS_PER_MONTH, num=N_PARAM_SWEEP
#     )
#     reference_subsidy_x_2_params = np.linspace(
#         start=0.1 * MAX_CREDIT_ISSUANCE,
#         stop=0.2 * MAX_CREDIT_ISSUANCE,
#         num=N_PARAM_SWEEP,
#     )
#
#     governance_surface = {
#         "issuance_function_constant": c_params,
#         "credit_supply_definition": credit_supply_definition_params,
#         "reference_subsidy_x_1": reference_subsidy_x_1_params,
#         "reference_subsidy_x_2": reference_subsidy_x_2_params,
#     }
#
#     controllable_params = sweep_cartesian_product(governance_surface)
#     governance_cardinality = max([len(v) for v in controllable_params.values()])
#
#     # Prepare for x_3 expansion
#     controllable_params = {k: v * 3 for k, v in controllable_params.items()}
#
#     # Generate x_3
#     controllable_params["reference_subsidy_x_3"] = [
#         x2 / x1
#         for x1, x2 in zip(
#             controllable_params["reference_subsidy_x_1"], controllable_params["reference_subsidy_x_2"]
#         )
#     ]
#
#     controllable_params["reference_subsidy_x_3"] = (
#         cardinality * [0]
#         + [
#             x_3 / 2
#             for x_3 in controllable_params["reference_subsidy_x_3"][
#                 cardinality : 2 * cardinality
#             ]
#         ]
#         + controllable_params["reference_subsidy_x_3"][2 * cardinality : 3 * cardinality]
#     )
#
#     # Generate reference_subsidy_components
#     controllable_params["reference_subsidy_components"] = [
#         [
#             SubsidyComponent(0, x1, x2, x3),
#         ]
#         for x1, x2, x3 in zip(
#             controllable_params["reference_subsidy_x_1"],
#             controllable_params["reference_subsidy_x_2"],
#             controllable_params["reference_subsidy_x_3"],
#         )
#     ]
#
#     # Drop x_1, x_2, x_3
#     controllable_params.pop("reference_subsidy_x_1", None)
#     controllable_params.pop("reference_subsidy_x_2", None)
#     controllable_params.pop("reference_subsidy_x_3", None)
#
#     # Used for adding environmental scenarios
#     governance_cardinality = max([len(v) for v in controllable_params.values()])
#
#     # Environmental scenarios
#     environmental_scenarios = list(SPECIAL_ENVIRONMENTAL_SCENARIOS.values())
#
#     # Repeat control scenarios for each environmental scenario
#     sweep_params = {
#         k: list(v * len(environmental_scenarios)) if len(v) == governance_cardinality else v
#         for k, v in controllable_params.items()
#     }
#
#     sweep_params = {**{k: [] for k in DEFAULT_PARAMS.keys()}, **sweep_params}
#
#     for (
#         k,
#         v,
#     ) in DEFAULT_PARAMS.items():
#         for param_set in environmental_scenarios:
#             if k in param_set.keys():
#                 sweep_params[k] += [param_set[k]] * cardinality
#             elif len(sweep_params[k]) != cardinality * len(environmental_scenarios):
#                 sweep_params[k] += [DEFAULT_PARAMS[k]] * cardinality
#
#     sweep_params = {
#         **{k: [v] for k, v in DEFAULT_PARAMS.items()},
#         **{k: v for k, v in sweep_params.items() if len(v) > 0},
#     }
#
#     # Load simulation arguments
#     sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)
#
#     # Run simulation
#     sim_df = easy_run(
#         *sim_args,
#         assign_params={
#             "label",
#             "environmental_label",
#             "timestep_in_days",
#             "block_time_in_seconds",
#             "max_credit_supply",
#         },
#         exec_mode="single",
#         deepcopy_off=True,
#         supress_print=True
#     )
#     return sim_df


def initial_conditions(
    SIMULATION_DAYS: int = 183, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 30
) -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep parameters in the form of single length arrays
    param_set = deepcopy(DEFAULT_PARAMS)

    sweep_params = {
        **{k: [v] for k, v in param_set.items()},
        **{k: [v] for k, v in SPECIAL_ENVIRONMENTAL_SCENARIOS["stochastic"].items()},
    }

    # Load simulation arguments
    sim_args = (INITIAL_STATE, sweep_params, SUBSPACE_MODEL_BLOCKS, TIMESTEPS, SAMPLES)

    # Run simulation
    sim_df = easy_run(
        *sim_args,
        assign_params={
            "label",
            "environmental_label",
            "timestep_in_days",
            "block_time_in_seconds",
            "max_credit_supply",
        },
        exec_mode="single",
        deepcopy_off=True,
        supress_print=True
    )
    return sim_df


def reference_subsidy_sweep(
    SIMULATION_DAYS: int = 360, TIMESTEP_IN_DAYS: int = 1, SAMPLES: int = 1
) -> DataFrame:
    """Sweeps issuance functions.

    Returns:
        DataFrame: A dataframe of simulation data
    """

    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    # Get the sweep params in the form of single length arrays
    param_set_1 = deepcopy(DEFAULT_PARAMS)
    param_set_1["label"] = "constant-single-component"
    param_set_1["reference_subsidy_components"] = (
        REFERENCE_SUBSIDY_CONSTANT_SINGLE_COMPONENT
    )

    param_set_2 = deepcopy(DEFAULT_PARAMS)
    param_set_2["label"] = "hybrid-single-component"
    param_set_2["reference_subsidy_components"] = (
        REFERENCE_SUBSIDY_HYBRID_SINGLE_COMPONENT
    )

    param_set_3 = deepcopy(DEFAULT_PARAMS)
    param_set_3["label"] = "hybrid-two-components"
    param_set_3["reference_subsidy_components"] = (
        REFERENCE_SUBSIDY_HYBRID_TWO_COMPONENTS
    )
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
            "label",
            "environmental_label",
            "timestep_in_days",
            "block_time_in_seconds",
            "max_credit_supply",
        },
        exec_mode="single",
        deepcopy_off=True,
        supress_print=True
    )
    return sim_df


def psuu(
    SIMULATION_DAYS: int = 3 * 365,
    TIMESTEP_IN_DAYS: int = 1,
    SAMPLES: int = 2,
    N_SWEEP_SAMPLES: int = 48,
    SWEEPS_PER_PROCESS: int = 20,
    PROCESSES: int = 4,
    PARALLELIZE: bool = True,
    USE_JOBLIB: bool = True,
    RETURN_SIM_DF: bool = False
) -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """

    invoke_time = datetime.now()
    logger.info(f"PSuU Exploratory Run invoked at {invoke_time}")

    TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1

    default_params = deepcopy(DEFAULT_PARAMS)

    sweep_params = sweep_cartesian_product(
        {
            **{k: [v] for k, v in default_params.items()},
            **ENVIRONMENTAL_SCENARIOS,
            **GOVERNANCE_SURFACE,
        }
    )

    # Sample the sweep space
    sweep_params_samples = {
        k: sample(v, N_SWEEP_SAMPLES) if N_SWEEP_SAMPLES > 0 else v
        for k, v in sweep_params.items()
    }

    # Load simulation arguments
    sim_args = (
        INITIAL_STATE,
        sweep_params_samples,
        SUBSPACE_MODEL_BLOCKS,
        TIMESTEPS,
        SAMPLES,
    )
    assign_params = {
        "label",
        "environmental_label",
        "timestep_in_days",
        "block_time_in_seconds",
        "max_credit_supply",
        *GOVERNANCE_SURFACE.keys(),
    }

    sweep_combinations = len(sweep_params['label'])

    n_sweeps = N_SWEEP_SAMPLES if N_SWEEP_SAMPLES > 0 else sweep_combinations
    N_measurements = n_sweeps * TIMESTEPS * SAMPLES


    traj_combinations = n_sweeps * SAMPLES

    logger.info(f"PSuU Exploratory Run Dimensions: N_jobs={PROCESSES=:,}, N_t={TIMESTEPS=:,}, N_sweeps={n_sweeps:,}, N_mc={SAMPLES:,}, N_trajectories={traj_combinations:,}, N_measurements={N_measurements:,}")


    parallelize = PARALLELIZE
    use_joblib = USE_JOBLIB


    sim_start_time = datetime.now()
    logger.info(f"PSuU Exploratory Run starting at {sim_start_time}, ({sim_start_time - invoke_time} since invoke)")
    if parallelize is False:
        # Load simulation arguments
        sim_args = (
            INITIAL_STATE,
            sweep_params_samples,
            SUBSPACE_MODEL_BLOCKS,
            TIMESTEPS,
            SAMPLES,
        )
        # Run simulation and write results to disk
        sim_df = easy_run(
            *sim_args,
            exec_mode="single",
            assign_params=assign_params,
            deepcopy_off=True,
            supress_print=True
        )
    else:
        sweeps_per_process = SWEEPS_PER_PROCESS
        processes = PROCESSES

        chunk_size = sweeps_per_process
        split_dicts = [
            {k: v[i : i + chunk_size] for k, v in sweep_params_samples.items()}
            for i in range(0, len(list(sweep_params_samples.values())[0]), chunk_size)
        ]
        sim_folder_path = Path("data/simulations")
        output_folder_path =sim_folder_path / f"psuu_run-{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}"
        output_folder_path.mkdir(parents=True, exist_ok=True)
        output_path = str(output_folder_path / "timestep_tensor")

        def run_chunk(i_chunk, sweep_params):
            logger.debug(f"{i_chunk}, {datetime.now()}")
            sim_args = (
                INITIAL_STATE,
                sweep_params,
                SUBSPACE_MODEL_BLOCKS,
                TIMESTEPS,
                SAMPLES,
            )
            # Run simulationz
            sim_df = easy_run(
                *sim_args,
                exec_mode="single",
                assign_params=assign_params,
                deepcopy_off=True,
                supress_print=True
            )
            sim_df["subset"] = i_chunk * SWEEPS_PER_PROCESS + sim_df["subset"]
            output_filename = output_path + f"-{i_chunk}.pkl.gz"
            sim_df.to_pickle(output_filename)

        args = enumerate(split_dicts)
        if use_joblib:
            Parallel(n_jobs=processes)(
                delayed(run_chunk)(i_chunk, sweep_params)
                for (i_chunk, sweep_params) in tqdm(args, desc='Simulation Chunks', total=len(split_dicts))
            )
        else:
            for i_chunk, sweep_params in tqdm(args):
                run_chunk(i_chunk, sweep_params)


        if RETURN_SIM_DF:
            # TODO: this code needs to be checked.
                        # Combine all of the chunks and write simulation results to disk
            latest_folder = "-".join(
                sorted(glob(f"./{str(sim_folder_path)}/psuu_run*"))[-1].split("-")[:-1]
            )
            parts = glob(f"{latest_folder}*")
            sorted_parts = sorted(parts, key=lambda x: int(re.search(r"-([0-9]+)\.pkl\.gz$", x).group(1)))  # type: ignore
            sim_df = pd.concat(
                [pd.read_pickle(part, compression="gzip") for part in sorted_parts]
            )
    end_start_time = datetime.now()
    duration: float = (end_start_time - sim_start_time).total_seconds()
    logger.info(f"PSuU Run finished at {end_start_time}, ({end_start_time - sim_start_time} since sim start)")
    logger.info(f"PSuU Run Performance Numbers; Duration (s): {duration:,.2f}, Measurements Per Second: {N_measurements/duration:,.2f} M/s, Measurements per Job * Second: {N_measurements/(duration * PROCESSES):,.2f} M/(J*s)")
    if RETURN_SIM_DF == True:
        return sim_df
    else:
        pass