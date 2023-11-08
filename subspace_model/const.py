from subspace_model.types import *

U32_RANGE = 2 ** 32
U128_RANGE = 2 ** 128
MIB_IN_BYTES = 1048576

# Subspace Constants
MAX_CREDIT_ISSUANCE = 3_000_000_000 # TODO: check if true
KZG_COMMITMENT: Bytes = 32 # As per Subnomicon
WITNESS: Bytes = 32 # As per Subnomicon
CHUNK_SIZE: Bytes = 32 # As per Subnomicon
ARCHIVAL_DEPTH: Blocks = 100 # As per Subnomicon
BLOCK_TIME: Seconds = 6 # As per Subnomicon. Approximate value.
RAW_RECORD_IN_CHUNKS: Chunk = 2 ** 15 # As per Subnomicon
PIECE_SIZE: Bytes = RAW_RECORD_IN_CHUNKS * CHUNK_SIZE + KZG_COMMITMENT + WITNESS # As per Subnomicon
SECTOR_IN_PIECES: Piece = 1_000 # As per Subnomicon
SECTOR_SIZE = SECTOR_IN_PIECES * PIECE_SIZE
SEGMENT_SIZE: Bytes = 128 * MIB_IN_BYTES # As per discussions
SEGMENT_HISTORY_SIZE: Bytes = SEGMENT_SIZE * 2 # As per discussions