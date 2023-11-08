from typing import Annotated, TypedDict, Union, Callable, NamedTuple
from dataclasses import dataclass

# Time units
Blocks = Annotated[float, 'blocks'] # 1 block ~ 6s. Or 1 day ~ 14400 blocks
Days = Annotated[float, 'days']  # Number of days
Seconds = Annotated[float, 's']
PerYear = Annotated[float, "1/year"]  # Yearly rate
Year = Annotated[float, "year"]  # Number of years

# Measurement units
Credits = Annotated[float, "SSC"] 
CreditsPerComputeUnits = Annotated[float, 'SSC/CU']
CreditsPerDay = Annotated[float, 'SSC/day']
ComputeUnits = Annotated[float, 'CU']
Shannon = Annotated[float, "Shannon"] # 1e-18 SSC 
ShannonPerComputeUnits = Annotated[float, 'Shannon/CU']

Bytes = Annotated[int, 'bytes']
Chunk = Annotated[int, 'chunk'] # As per Subnomicon: 1 chunk = 32 Bytes
RawRecord = Annotated[Chunk, 'raw_record'] # As per Subnomicon: 2**15 Chunks (~1MB)
Piece = Annotated[int, 'piece'] # As per Subnomicon: 1 piece = 1 record + commitment + witness
Record = Annotated[Piece,'record'] # As per Subnomicon: a transformed raw record.
Sector = Annotated[Piece, 'sector'] # As per Subnomicon: 1000 Pieces or ~ 1 GiB

# As per Subnomicon: A collection of potential partial or full blocks.
# Can be either a fixed-size portion of the Blockchain History
# or a fixed-size portion of the Archived History
Segment = Annotated[Bytes, 'segment'] 
RecordedHistorySegment = Annotated[Record, 'record_segment']
ArchivedHistorySegment = Annotated[Piece, 'archive_segment'] 

# Misc units
Percentage = Annotated[float, '%']

# Taxonomy:
# Chunk < Record/Piece < Sector < Plot < History


class SubspaceModelState(TypedDict):
    # Time Variables
    days_passed: Days
    delta_days: Days
    delta_blocks: Blocks

    # Metrics
    circulating_supply: Credits
    user_supply: Credits
    issued_supply: Credits
    sum_of_stocks: Credits
    block_utilization: Percentage

    # Governance Variables
    dsf_relative_disbursal_per_day: Percentage

    # Stocks
    reward_issuance_balance: Credits
    other_issuance_balance: Credits
    operators_balance: Credits
    nominators_balance: Credits
    holders_balance: Credits
    farmers_balance: Credits
    staking_pool_balance: Credits
    fund_balance: Credits
    burnt_balance: Credits

    # Staking Pool Shares
    nominator_pool_shares: float
    operator_pool_shares: float

    # Deterministic Variables
    block_reward: Credits
    history_size: Bytes
    space_pledged: Bytes
    allocated_tokens: Credits
    buffer_size: Bytes

    # Stochastic Variables
    average_base_fee: ShannonPerComputeUnits
    average_priority_fee: ShannonPerComputeUnits
    average_compute_weight_per_tx: ComputeUnits
    average_transaction_size: Bytes
    transaction_count: int

    # Metrics
    compute_fee_volume: Credits
    storage_fee_volume: Credits


class SubspaceModelParams(TypedDict):
    label: str
    timestep_in_days: Days

    # Mechanisms to be determined
    issuance_function: Callable[[SubspaceModelState], CreditsPerDay]
    slash_function: Callable[[SubspaceModelState], Credits]

    # Implementation parameters
    block_time_in_seconds: Seconds
    archival_depth: Blocks
    archival_buffer_segment_size: Bytes
    replication_factor: float
    max_block_size: Bytes

    # Economic Parameters
    reward_proposer_share: Percentage
    max_credit_supply: Credits
    
    # Fees & Taxes
    fund_tax_on_proposer_reward: Percentage
    fund_tax_on_storage_fees: Percentage
    compute_fees_to_farmers: Percentage
    compute_fees_tax_to_operators: Percentage

    # Slash Parameters
    slash_to_fund: Percentage
    slash_to_holders: Percentage

    # Behavioral Parameters
    operator_stake_per_ts: Percentage
    nominator_stake_per_ts: Percentage
    transfer_farmer_to_holder_per_day: Percentage
    transfer_operator_to_holder_per_day: Percentage
    transfer_holder_to_nominator_per_day: Percentage
    transfer_holder_to_operator_per_day: Percentage

    # Environmental Parameters
    avg_base_fee: Credits
    std_base_fee: Credits
    min_base_fee: Credits
    avg_priority_fee: Credits
    std_priority_fee: Credits
    avg_compute_weights_per_tx: ComputeUnits
    std_compute_weights_per_tx: ComputeUnits
    min_compute_weights_per_tx: ComputeUnits
    avg_transaction_size: Bytes
    std_transaction_size: Bytes
    min_transaction_size: Bytes
    avg_transaction_count_per_day: float
    avg_slash_per_day: int # NOTE: tbc
    avg_new_sectors_per_day: float
    std_new_sectors_per_day: float
    