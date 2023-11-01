from subspace_model.types import *
from numpy import nan

SIMULATION_DAYS = 700
TIMESTEP_IN_DAYS = 1
TIMESTEPS = int(SIMULATION_DAYS / TIMESTEP_IN_DAYS) + 1
SAMPLES = 1

# Constants
MAX_CREDIT_ISSUANCE = 3_000_000_000 # TODO
CHUNK_SIZE: Bytes = 32 # As per Subnomiconcal
RECORD_SIZE: Chunk = 2 ** 15 # As per Subnomicon. 32*2^25 = 1 MiB.
ARCHIVAL_DEPTH: Blocks = 100 # As per Subnomicon
BLOCK_TIME: Seconds = 6 # As per Subnomicon. Approximate value.
SECTOR_SIZE: Piece = 1000 # As per Subnomicon.


ISSUANCE_FOR_FARMERS = MAX_CREDIT_ISSUANCE * 0.44

INITIAL_STATE = SubspaceModelState(
    days_passed=0,
    delta_days=0,

    # Metrics
    circulating_supply=nan,
    user_supply=nan,
    issued_supply=nan,
    sum_of_stocks=nan,

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
    block_reward=nan,
    history_size_in_bytes=0,
    commit_size_in_bytes=0,
    allocated_tokens=0.0,

    # Environmental Variables
    average_base_fee=nan,
    average_priority_fee=nan,
    average_compute_units=nan,
    average_transaction_size=nan,
    transaction_count=nan,

    compute_fee_volume=0.0,
    storage_fee_volume=0.0
)


def DEFAULT_ISSUANCE_FUNCTION(state: SubspaceModelState):
    return state['reward_issuance_balance'] * 0.02 # HACK

def DEFAULT_SLASH_FUNCTION(state: SubspaceModelState):
    return state['staking_pool_balance'] * 0.01 # HACK

SINGLE_RUN_PARAMS = SubspaceModelParams(
    label='standard',
    timestep_in_days=TIMESTEP_IN_DAYS,
    
    # Mechanisms TBD
    issuance_function=DEFAULT_ISSUANCE_FUNCTION, # TODO
    slash_function=DEFAULT_SLASH_FUNCTION, # TODO

    # Implementation params
    sector_size_in_bytes=SECTOR_SIZE * RECORD_SIZE,
    block_time_in_seconds=BLOCK_TIME,
    archival_duration_in_blocks=ARCHIVAL_DEPTH,
    archive_size_in_bytes=128 * 1e6, # TODO

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
    operator_stake_per_ts=0.2, # TODO
    nominator_stake_per_ts=0.5, # TODO
    transfer_farmer_to_holder_per_day=0.3, # TODO
    transfer_operator_to_holder_per_day=0.3, # TODO
    transfer_holder_to_nominator_per_day=0.1, # TODO
    transfer_holder_to_operator_per_day=0.05, # TODO

    # Environmental Parameters
    avg_base_fee=30,
    std_base_fee=5,
    min_base_fee=1,

    avg_priority_fee=5,
    std_priority_fee=10,

    avg_compute_units_per_tx=1_000, # TODO
    std_compute_units_per_tx=1_000, # TODO
    min_compute_units_per_tx=10, # TODO

    avg_transaction_size=1_000, # TODO
    std_transaction_size=5_000, # TODO

    min_transaction_size=100, # TODO
    avg_transaction_count=30, # TODO

    avg_slash_per_day=1, # TODO
    avg_new_sectors_per_day=700, # TODO
    std_new_sectors_per_day=200 # TODO

)
