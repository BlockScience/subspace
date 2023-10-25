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


NON_ISSUED_CREDIT_AT_START = MAX_CREDIT_ISSUANCE 

INITIAL_STATE = SubspaceModelState(
    days_passed=0,
    delta_days=0,

    issuance_balance=NON_ISSUED_CREDIT_AT_START,
    operators_balance=0.0,
    nominators_balance=0.0,
    holders_balance=0.0,
    farmers_balance=0.0,
    staking_pool_balance=0.0,
    fund_balance=0.0,
    burnt_balance=0.0,

    block_reward=nan,
    history_size_in_bytes=0.0,
    commit_size_in_bytes=0.0,
    allocated_tokens=0.0,

    average_base_fee=nan,
    average_priority_fee=nan,
    average_compute_units=nan,
    average_transaction_size=nan,
    transaction_count=nan,

    compute_fee_volume=0.0,
    storage_fee_volume=0.0
)

SINGLE_RUN_PARAMS = SubspaceModelParams(
    label='standard',
    timestep_in_days=TIMESTEP_IN_DAYS,

    sector_size_in_bytes=SECTOR_SIZE * RECORD_SIZE,
    block_time_in_seconds=BLOCK_TIME,
    archival_duration_in_blocks=ARCHIVAL_DEPTH,
    archive_size_in_bytes=128 * 1e6, # TODO
    reward_proposer_share=0.0, # TODO
    max_credit_supply=3_000_000_000, # TODO,
    fund_tax_on_proposer_reward=0.0, # TODO
    fund_tax_on_storage_fees=0.0, # TODO
    farmer_tax_on_compute_priority_fees=0.0, # TODO
    operator_tax_on_compute_revenue=0.0 # TODO
)
