from subspace_model.experiments.experiment import (
    fund_inclusion,
    issuance_sweep,
    reward_split_sweep,
    sanity_check_run,
    standard_stochastic_run,
    sweep_credit_supply,
)


def test_sanity_check_run():
    sim_df = sanity_check_run(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=1)


def test_standard_stochastic_run():
    sim_df = standard_stochastic_run(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=2)


def test_issuance_sweep():
    sim_df = issuance_sweep(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=1)


def test_fund_inclusion():
    sim_df = fund_inclusion(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=1)


def test_reward_split_sweep():
    sim_df = reward_split_sweep(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=1)


def test_sweep_credit_supply():
    sim_df = sweep_credit_supply(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=1)
