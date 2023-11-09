from subspace_model.types import *
from subspace_model.const import *
from numpy import nan

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
    dsf_relative_disbursal_per_day=0.0, # How much %/day of DSF's goes to farmers

    # Stock Balances
    reward_issuance_balance=ISSUANCE_FOR_FARMERS,
    other_issuance_balance=MAX_CREDIT_ISSUANCE-ISSUANCE_FOR_FARMERS,
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
    storage_fee_volume=0.0
)


def DEFAULT_ISSUANCE_FUNCTION(state: SubspaceModelState):
    return state['reward_issuance_balance'] * 0.01 # HACK

def DEFAULT_SLASH_FUNCTION(state: SubspaceModelState):
    return state['staking_pool_balance'] * 0.01 # HACK

SINGLE_RUN_PARAMS = SubspaceModelParams(
    label='standard',
    timestep_in_days=TIMESTEP_IN_DAYS,
    
    # Mechanisms TBD
    issuance_function=DEFAULT_ISSUANCE_FUNCTION, # TODO
    slash_function=DEFAULT_SLASH_FUNCTION, # TODO

    # Implementation params
    block_time_in_seconds=BLOCK_TIME,
    archival_depth=ARCHIVAL_DEPTH,
    archival_buffer_segment_size=SEGMENT_SIZE,
    replication_factor=10,
    max_block_size=int(3.75 * MIB_IN_BYTES), # 3.75 MiB

    # Economic Parameters
    reward_proposer_share=0.0, # TODO
    max_credit_supply=3_000_000_000, # TODO,

    # Fees & Taxes
    fund_tax_on_proposer_reward=0.0, # TODO
    fund_tax_on_storage_fees=0.0, # TODO
    compute_fees_to_farmers=0.0, # TODO
    compute_fees_tax_to_operators=0.3, # TODO

    # Slash Parameters
    slash_to_fund=0.0,
    slash_to_holders=0.05,

    # Behavioral Parameters
    operator_avg_stake_per_ts=0.01, # TODO
    nominator_avg_stake_per_ts=0.01, # TODO
    operator_std_stake_per_ts=0.02, # TODO
    nominator_std_stake_per_ts=0.02, #TODO
    transfer_farmer_to_holder_per_day=0.05, # TODO
    transfer_operator_to_holder_per_day=0.05, # TODO
    transfer_holder_to_nominator_per_day=0.01, # TODO
    transfer_holder_to_operator_per_day=0.01, # TODO

    # Environmental Parameters
    avg_base_fee=5,
    std_base_fee=15,
    min_base_fee=1,

    avg_priority_fee=3,
    std_priority_fee=5,

    avg_compute_weights_per_tx=200, # TODO
    std_compute_weights_per_tx=500, # TODO
    min_compute_weights_per_tx=10, # TODO

    avg_transaction_size=600_000, # TODO
    std_transaction_size=100_000, # TODO
    min_transaction_size=100, # TODO
    avg_transaction_count_per_day=1 * (24*60*60/BLOCK_TIME), # XXX: X tx per block

    avg_slash_per_day=1, # TODO
    avg_new_sectors_per_day=1_000, # TODO
    std_new_sectors_per_day=500 # TODO

)
