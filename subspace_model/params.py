from numpy import nan

from subspace_model.const import *
from subspace_model.experiments.logic import (
    DEFAULT_ISSUANCE_FUNCTION,
    DEFAULT_REFERENCE_SUBSIDY_COMPONENTS,
    DEFAULT_SLASH_FUNCTION,
    MAGNITUDE,
    NORMAL_GENERATOR,
    POISSON_GENERATOR,
    POSITIVE_INTEGER,
    SUPPLY_EARNED,
    SUPPLY_EARNED_MINUS_BURNED,
    SUPPLY_ISSUED,
    TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50,
    TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS,
    WEEKLY_VARYING,
)
from subspace_model.types import *

ISSUANCE_FOR_FARMERS = MAX_CREDIT_ISSUANCE * 0.44

INITIAL_STATE = SubspaceModelState(
    days_passed=0,
    blocks_passed=0,
    # Metrics
    circulating_supply=0.0,
    user_supply=0.0,
    earned_supply=0.0,
    issued_supply=0.0,
    earned_minus_burned_supply=0.0,
    total_supply=0.0,
    sum_of_stocks=0.0,
    block_utilization=0.0,
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
    reference_subsidy=0.0,
    # Environmental Variables
    average_base_fee=0.0,
    average_priority_fee=0.0,
    average_compute_weight_per_tx=0.0,
    average_transaction_size=256,
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
    reference_subsidy_components=DEFAULT_REFERENCE_SUBSIDY_COMPONENTS,
    issuance_function=DEFAULT_ISSUANCE_FUNCTION,
    issuance_function_constant=1,
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
    transfer_farmer_to_holder_per_day_function=lambda p, s: 0.05,
    transfer_operator_to_holder_per_day_function=lambda p, s: 0.05,
    transfer_holder_to_nominator_per_day_function=lambda p, s: 0.01,
    transfer_holder_to_operator_per_day_function=lambda p, s: 0.01,
    # Environmental Parameters (Integer positive in [0,inf])
    base_fee_function=lambda p, s: 1,
    priority_fee_function=lambda p, s: 3,
    compute_weights_per_tx_function=lambda p, s: 60_000_000,
    compute_weight_per_bundle_function=lambda p, s: 10_000_000_000,
    transaction_size_function=lambda p, s: 256,
    bundle_size_function=lambda p, s: 1500,
    transaction_count_per_day_function=TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50,
    bundle_count_per_day_function=lambda p, s: 6 * BLOCKS_PER_DAY,
    slash_per_day_function=lambda p, s: 0.1,
    new_sectors_per_day_function=lambda p, s: 1000,
)

ENVIRONMENTAL_SCENARIOS = {
    'stochastic': {
        # Behavioral Parameters Between 0 and 1
        'operator_stake_per_ts_function': MAGNITUDE(NORMAL_GENERATOR(0.01,0.02)),
        'nominator_stake_per_ts_function': MAGNITUDE(NORMAL_GENERATOR(0.01,0.02)),
        'transfer_farmer_to_holder_per_day_function': MAGNITUDE(NORMAL_GENERATOR(0.05,0.05)),
        'transfer_operator_to_holder_per_day_function': MAGNITUDE(NORMAL_GENERATOR(0.05,0.05)),
        'transfer_holder_to_nominator_per_day_function': MAGNITUDE(NORMAL_GENERATOR(0.01,0.02)),
        'transfer_holder_to_operator_per_day_function': MAGNITUDE(NORMAL_GENERATOR(0.01,0.02)),

        # Environmental Parameters (Integer positive in [0,inf])
        'environmental_label': 'stochastic',
        'base_fee_function': POSITIVE_INTEGER(NORMAL_GENERATOR(1, 1)),
        'priority_fee_function': POSITIVE_INTEGER(NORMAL_GENERATOR(3, 5)),
        'compute_weights_per_tx_function': POSITIVE_INTEGER(
            NORMAL_GENERATOR(60_000_000, 15_000_000)
        ),
        'compute_weight_per_bundle_function': POSITIVE_INTEGER(
            NORMAL_GENERATOR(10_000_000_000, 5_000_000_000)
        ),
        'transaction_size_function': POSITIVE_INTEGER(NORMAL_GENERATOR(256, 100)),
        'bundle_size_function': POSITIVE_INTEGER(NORMAL_GENERATOR(1500, 1000)),
        'transaction_count_per_day_function': POISSON_GENERATOR(1 * BLOCKS_PER_DAY),
        'bundle_count_per_day_function': POISSON_GENERATOR(6 * BLOCKS_PER_DAY),
        'slash_per_day_function': POISSON_GENERATOR(0.1),
        'new_sectors_per_day_function': POSITIVE_INTEGER(NORMAL_GENERATOR(1000, 500)),
    },
    'weekly-varying': {
        'environmental_label': 'weekly-varying',
        'base_fee_function': WEEKLY_VARYING,
        'priority_fee_function': WEEKLY_VARYING,
    },
    'constant-utilization': {
        'environmental_label': 'constant-utilization',
        'transaction_count_per_day_function': TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50,
    },
    'growing-utilization': {
        'environmental_label': 'growing-utilization',
        'transaction_count_per_day_function': TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS,
    },
}
