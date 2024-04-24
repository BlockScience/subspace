from subspace_model.experiments.experiment import (
    fund_inclusion,
    reward_split_sweep,
    sanity_check_run,
    standard_stochastic_run,
    sweep_credit_supply,
    reference_subsidy_sweep,
)


def test_sanity_check_run():
    sim_df = sanity_check_run(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=1)


def test_standard_stochastic_run():
    sim_df = standard_stochastic_run(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=2)


def test_reward_split_sweep():
    sim_df = reward_split_sweep(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=1)


def test_sweep_credit_supply():
    sim_df = sweep_credit_supply(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=1)


def test_reference_subsidy_sweep():
    sim_df = reference_subsidy_sweep(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=1)


# def test_sweep_over_single_component_and_credit_supply():
#     sim_df = sweep_over_single_component_and_credit_supply(
#         SIMULATION_DAYS=1, TIMESTEP_IN_DAYS=1, SAMPLES=1
#     )
