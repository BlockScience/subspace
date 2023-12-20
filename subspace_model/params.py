from numpy import nan

from subspace_model.const import *
from subspace_model.experiments.logic import (
    DEFAULT_ISSUANCE_FUNCTION,
    DEFAULT_SLASH_FUNCTION,
    MAGNITUDE,
    NORMAL_GENERATOR,
    POISSON_GENERATOR,
    POSITIVE_INTEGER,
    SUPPLY_EARNED,
    SUPPLY_EARNED_MINUS_BURNED,
    SUPPLY_ISSUED,
)
from subspace_model.types import *

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
    average_base_fee=0.0,
    average_priority_fee=0.0,
    average_compute_weight_per_tx=0.0,
    average_transaction_size=0.0,
    transaction_count=0.0,
    average_compute_weight_per_bundle=0.0,
    average_bundle_size=0.0,
    bundle_count=0.0,
    compute_fee_volume=0.0,
    storage_fee_volume=0.0,
    rewards_to_nominators=0.0,
)


DEFAULT_PARAMS = SubspaceModelParams(
    label='standard',
    environmental_label='standard',
    # Set system wide deterministic
    timestep_in_days=1,
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
    min_base_fee=1,
    min_compute_weights_per_tx=6_000_000,  # TODO
    min_compute_weights_per_bundle=2_000_000_000,  # TODO
    min_transaction_size=100,  # TODO
    min_bundle_size=250,  # TODO
    # Economic Parameters
    reward_proposer_share=0.0,  # TODO
    max_credit_supply=3_000_000_000,  # TODO,
    credit_supply_definition=SUPPLY_ISSUED,
    # Fees & Taxes
    fund_tax_on_proposer_reward=0.0,  # TODO
    fund_tax_on_storage_fees=1 / 10,
    compute_fees_to_farmers=0.0,  # TODO
    compute_fees_tax_to_operators=0.05,  # or `nomination_tax`
    # Slash Parameters
    slash_to_fund=0.0,
    slash_to_holders=0.05,
    # Behavioral Parameters Between 0 and 1
    operator_stake_per_ts_function=lambda p, s: 0.01,
    nominator_stake_per_ts_function=lambda p, s: 0.01,
    transfer_farmer_to_holder_per_day=lambda p, s: 0.05,
    transfer_operator_to_holder_per_day=lambda p, s: 0.05,
    transfer_holder_to_nominator_per_day=lambda p, s: 0.01,
    transfer_holder_to_operator_per_day=lambda p, s: 0.01,
    # Environmental Parameters (Integer positive in [0,inf])
    base_fee_function=lambda p, s: 1,
    priority_fee_function=lambda p, s: 3,
    compute_weights_per_tx_function=lambda p, s: 60_000_000,
    compute_weight_per_bundle_function=lambda p, s: 10_000_000_000,
    transaction_size_function=lambda p, s: 256,
    bundle_size_function=lambda p, s: 1500,
    transaction_count_per_day_function=lambda p, s: 1 * BLOCKS_PER_DAY,
    bundle_count_per_day_function=lambda p, s: 6 * BLOCKS_PER_DAY,
    slash_per_day_function=lambda p, s: 0.1,
    new_sectors_per_day_function=lambda p, s: 1000,
)
