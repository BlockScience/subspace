from subspace_model.types import *


# Constants
MAX_CREDIT_ISSUANCE = 100_000 # TODO
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
    burnt_balance=0.0
)

SINGLE_RUN_PARAMS = SubspaceModelParams(
    label='standard',
    timestep_in_days=1
)