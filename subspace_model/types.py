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
Chunk = Annotated[int, 'chunk'] # As per Subnomicon: 1 chunk = 256 Bytes
Piece = Annotated[int, 'piece'] # As per Subnomicon: 1 piece = 1 record + proof
Sector = Annotated[int, 'sector'] # As per Subnomicon: 1000 Pieces or ~ 1 GiB

# Misc units
Percentage = Annotated[float, '%']


class SlashAffectedBalances(NamedTuple):
    operators_balance: Credits
    fund_balance: Credits
    holders_balance: Credits
    burnt_balance: Credits


# Taxonomy:
# Chunk < Record/Piece < Sector < Plot < History


class SubspaceModelState(TypedDict):
    # Time Variables
    days_passed: Days
    delta_days: Days

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

    # Deterministic Variables
    block_reward: Credits
    history_size_in_bytes: Bytes
    commit_size_in_bytes: Bytes
    allocated_tokens: Credits

    # Stochastic Variables
    average_base_fee: ShannonPerComputeUnits
    average_priority_fee: ShannonPerComputeUnits
    average_compute_units: ComputeUnits
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
    slash_function: Callable[[SubspaceModelState], SlashAffectedBalances]

    # Implementation parameters
    sector_size_in_bytes: int
    block_time_in_seconds: Seconds
    archival_duration_in_blocks: Blocks
    archive_size_in_bytes: Bytes

    # Economic Parameters
    reward_proposer_share: Percentage
    max_credit_supply: Credits
    
    # Fees & Taxes
    fund_tax_on_proposer_reward: Percentage
    fund_tax_on_storage_fees: Percentage
    farmer_tax_on_compute_priority_fees: Percentage
    operator_tax_on_compute_revenue: Percentage

    # Behavioral Parameters
    operator_balance_stake_per_ts: Percentage
    nominator_balance_stake_per_ts: Percentage

    # Environmental Parameters
    avg_base_fee: Credits
    std_base_fee: Credits
    min_base_fee: Credits
    avg_priority_fee: Credits
    std_priority_fee: Credits
    avg_compute_units_per_tx: ComputeUnits
    std_compute_units_per_tx: ComputeUnits
    min_compute_units_per_tx: ComputeUnits
    avg_transaction_size: Bytes
    std_transaction_size: Bytes
    min_transaction_size: Bytes
    avg_transaction_count: int
    avg_slash_per_day: int # NOTE: tbc
    avg_new_sectors_per_day: float
    std_new_sectors_per_day: float
    