from numpy import nan

from subspace_model.const import *
from subspace_model.experiments.logic import (
    DEFAULT_ISSUANCE_FUNCTION,
    DEFAULT_SLASH_FUNCTION,
    NORMAL,
    POISSON,
)
from subspace_model.types import *

SIMULATION_DAYS = 700
TIMESTEP_IN_DAYS = 1
TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1
SAMPLES = 1

ISSUANCE_FOR_FARMERS = MAX_CREDIT_ISSUANCE * 0.44

INITIAL_STATE = SubspaceModelState(
    days_passed=0,
    delta_days=None,
    delta_blocks=None,
    # Metrics
    circulating_supply=None,
    user_supply=None,
    issued_supply=None,
    sum_of_stocks=None,
    block_utilization=None,
    # Governance Variables
    dsf_relative_disbursal_per_day=0.0,  # How much %/day of DSF's goes to farmers
    # Stock Balances
    reward_issuance_balance=ISSUANCE_FOR_FARMERS,
    other_issuance_balance=MAX_CREDIT_ISSUANCE - ISSUANCE_FOR_FARMERS,
    operators_balance=0.0,
    nominators_balance=0.0,
    holders_balance=0.0,
    farmers_balance=0.0,
    staking_pool_balance=0.0,
    fund_balance=0.0,
    burnt_balance=0.0,
    # Staking Pool Shares
    nominator_pool_shares=0.0,
    operator_pool_shares=0.0,
    # Variables
    block_reward=None,
    history_size=0,
    space_pledged=0,
    allocated_tokens=0.0,
    buffer_size=0,
    # Environmental Variables
    average_base_fee=None,
    average_priority_fee=None,
    average_compute_weight_per_tx=None,
    average_transaction_size=None,
    transaction_count=None,
    compute_fee_volume=0.0,
    storage_fee_volume=0.0,
    rewards_to_nominators=0.0,
)


BASE_PARAMS = SubspaceModelParams(
    label='standard',
    stochastic_params=dict(
        operator_stake_per_ts_function=dict(
            mu=0.01,
            sigma=0.01,
            deterministic=False,
        ),
        nominator_stake_per_ts_function=dict(
            mu=0.01,
            sigma=0.01,
            deterministic=False,
        ),
        base_fee_function=dict(
            mu=1,
            sigma=1,
            deterministic=False,
        ),
        priority_fee_function=dict(
            mu=3,
            sigma=5,
            deterministic=False,
        ),
        compute_weight_per_tx_function=dict(
            mu=60_000_000,
            sigma=15_000_000,
            deterministic=False,
        ),
        # bundles are usually compute heavy
        compute_weight_per_bundle_function=dict(
            mu=10_000_000_000,
            sigma=5_000_000_000,
            deterministic=False,
        ),
        transaction_size_function=dict(
            mu=256,
            sigma=100,
            deterministic=False,
        ),
        bundle_size_function=dict(
            mu=1500,
            sigma=1000,
            deterministic=False,
        ),
        # Transactions per block
        transaction_count_per_day_function=dict(
            mu=1 * (24 * 60 * 60 / BLOCK_TIME),
            deterministic=False,
        ),
        # Bundles per block
        bundle_count_per_day_function=dict(
            mu=6 * (24 * 60 * 60 / BLOCK_TIME),
            deterministic=False,
        ),
        slash_per_day_function=dict(
            mu=0.1,
            deterministic=False,
        ),
        new_sectors_per_day_function=dict(
            mu=1000,
            sigma=500,
            deterministic=False,
        ),
    ),
    timestep_in_days=TIMESTEP_IN_DAYS,
    # Mechanisms TBD
    issuance_function=DEFAULT_ISSUANCE_FUNCTION,  # TODO
    slash_function=DEFAULT_SLASH_FUNCTION,  # TODO
    # Implementation params
    block_time_in_seconds=BLOCK_TIME,
    archival_depth=ARCHIVAL_DEPTH,
    archival_buffer_segment_size=SEGMENT_SIZE,
    header_size=6_500,  # how much data does every block contain on top of txs: signature, solution, consensus logs, etc. + votes + PoT
    replication_factor=10,
    max_block_size=int(3.75 * MIB_IN_BYTES),  # 3.75 MiB
    # Economic Parameters
    reward_proposer_share=0.0,  # TODO
    max_credit_supply=3_000_000_000,  # TODO,
    # Fees & Taxes
    fund_tax_on_proposer_reward=0.0,  # TODO
    fund_tax_on_storage_fees=1 / 10,
    compute_fees_to_farmers=0.0,  # TODO
    compute_fees_tax_to_operators=0.05,  # or `nomination_tax`
    # Slash Parameters
    slash_to_fund=0.0,
    slash_to_holders=0.05,
    # Behavioral Parameters
    operator_stake_per_ts_function=NORMAL,
    nominator_stake_per_ts_function=NORMAL,
    transfer_farmer_to_holder_per_day=0.05,  # TODO
    transfer_operator_to_holder_per_day=0.05,  # TODO
    transfer_holder_to_nominator_per_day=0.01,  # TODO
    transfer_holder_to_operator_per_day=0.01,  # TODO
    # Environmental Parameters
    base_fee_function=NORMAL,
    min_base_fee=1,
    priority_fee_function=NORMAL,
    compute_weight_per_tx_function=NORMAL,
    min_compute_weights_per_tx=6_000_000,  # TODO
    compute_weight_per_bundle_function=NORMAL,
    min_compute_weights_per_bundle=2_000_000_000,  # TODO
    transaction_size_function=NORMAL,
    min_transaction_size=100,  # TODO
    bundle_size_function=NORMAL,
    min_bundle_size=250,  # TODO
    transaction_count_per_day_function=POISSON,  # XXX: X tx per block
    bundle_count_per_day_function=POISSON,
    slash_per_day_function=POISSON,
    new_sectors_per_day_function=NORMAL,
)
