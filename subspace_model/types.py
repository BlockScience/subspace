from typing import Annotated, Callable, NamedTuple, Optional, TypedDict, Union
import math
from dataclasses import dataclass

# Time units
Blocks = Annotated[float, "blocks"]  # 1 block ~ 6s. Or 1 day ~ 14400 blocks
Days = Annotated[float, "days"]  # Number of days
Seconds = Annotated[float, "s"]
PerYear = Annotated[float, "1/year"]  # Yearly rate
Year = Annotated[float, "year"]  # Number of years
Picoseconds = Annotated[float, "ps"]  # Number of Picoseconds

# Measurement units
Credits = Annotated[float, "SSC"]
CreditsPerComputeWeights = Annotated[float, "SSC/CW"]
CreditsPerDay = Annotated[float, "SSC/day"]
ComputeWeights = Annotated[float, "CW"]
Shannon = Annotated[float, "Shannon"]  # 1e-18 SSC
ShannonPerComputeWeights = Annotated[float, "Shannon/CW"]

# Storage
Bytes = Annotated[int, "bytes"]
Chunk = Annotated[int, "chunk"]  # As per Subnomicon: 1 chunk = 32 Bytes
RawRecord = Annotated[Chunk, "raw_record"]  # As per Subnomicon: 2**15 Chunks (~1MB)
Piece = Annotated[
    int, "piece"
]  # As per Subnomicon: 1 piece = 1 record + commitment + witness
Record = Annotated[Piece, "record"]  # As per Subnomicon: a transformed raw record.
Sector = Annotated[Piece, "sector"]  # As per Subnomicon: 1000 Pieces or ~ 1 GiB

# As per Subnomicon: A collection of potential partial or full blocks.
# Can be either a fixed-size portion of the Blockchain History
# or a fixed-size portion of the Archived History
Segment = Annotated[Bytes, "segment"]
RecordedHistorySegment = Annotated[Record, "record_segment"]
ArchivedHistorySegment = Annotated[Piece, "archive_segment"]

# Taxonomy:
# Chunk < Record/Piece < Sector < Plot < History

# Misc units
Percentage = Annotated[float, "%"]



@dataclass
class SubsidyComponent:
    initial_period_start: float  # τ_{0, i}
    initial_period_end: float  # τ_{1, i}
    max_cumulative_subsidy: float  # Ω_i
    max_reference_subsidy: float  # α_i

    def __call__(self, t: float) -> float:
        """Allow the instance to be called as a function to calculate the subsidy."""
        return self.calculate_subsidy(t)

    def calculate_subsidy(self, t: float) -> float:
        """Calculate S(t) the subsidy for a given time."""
        if t < self.initial_period_start:
            return 0
        elif self.initial_period_start <= t <= self.initial_period_end:
            return self.calculate_linear_subsidy(t)
        else:
            return self.calculate_exponential_subsidy(t)

    def calculate_linear_subsidy(self, t: float) -> float:
        """Calculate S_l(t) the linear subsidy for a given time."""
        already_distributed = self.max_reference_subsidy * (
            t - self.initial_period_start
        )
        if already_distributed >= self.max_cumulative_subsidy:
            return 0
        elif (
            already_distributed + self.max_reference_subsidy
            > self.max_cumulative_subsidy
        ):
            return self.max_cumulative_subsidy - already_distributed
        else:
            return self.max_reference_subsidy

    def calculate_exponential_subsidy(self, t: float) -> float:
        """Calculate S_e(t) the exponential subsidy for a given time."""
        K = self.max_total_subsidy_during_exponential_period
        if K > 0:
            return self.max_reference_subsidy * math.exp(
                -self.max_reference_subsidy / max(1, K * (t - self.initial_period_end))
            )
        else:
            return 0

    @property
    def max_total_subsidy_during_exponential_period(self) -> float:
        """Calculate K the maximum total subsidy during the exponential period."""
        return self.max_cumulative_subsidy - self.max_reference_subsidy * (
            self.initial_period_end - self.initial_period_start
        )

    @property
    def halving_period(self) -> float:
        """Calculate L the halving period for the component rewards."""
        K = self.max_total_subsidy_during_exponential_period
        return K * math.log(2) / self.max_reference_subsidy




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
    initial_community_owned_supply_pct_of_max_credits: Percentage

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
    blockchain_history_size: Bytes
    total_space_pledged: Bytes
    allocated_tokens: Credits
    buffer_size: Bytes

    # Stochastic Variables
    average_base_fee: Optional[ShannonPerComputeWeights]
    average_priority_fee: Optional[ShannonPerComputeWeights]

    average_compute_weight_per_tx: ComputeWeights
    average_transaction_size: Bytes
    transaction_count: int

    average_compute_weight_per_bundle: ComputeWeights
    average_bundle_size: Bytes
    bundle_count: int

    # Metrics
    compute_fee_volume: Credits
    storage_fee_volume: Credits
    rewards_to_nominators: Credits

    # max_normal_weight:
    # max_bundle_weight:
    # target_block_fullness:
    # block_weight_utilization:
    # adjustment_variable:
    # priority_fee_volume:


class SubspaceModelParams(TypedDict):
    # Meta
    label: str
    environmental_label: str
    timestep_in_days: Days

    # Mechanism Parameters
    issuance_function: Callable
    slash_function: Callable[['SubspaceModelParams', SubspaceModelState], Credits]
    reference_subsidy_components: list[SubsidyComponent]
    issuance_function_constant: float
    utilization_ratio_smooth_num_blocks: int

    # Implementation parameters
    block_time_in_seconds: Seconds
    archival_depth: Blocks
    archival_buffer_segment_size: Bytes
    header_size: Bytes
    min_replication_factor: float
    max_block_size: Bytes
    weight_to_fee: Credits

    # Economic Parameters
    reward_proposer_share: Percentage
    max_credit_supply: Credits
    credit_supply_definition: Callable[[SubspaceModelState], Credits]
    community_vested_supply_fraction: Percentage

    # Fees & Taxes
    fund_tax_on_proposer_reward: Percentage
    fund_tax_on_storage_fees: Percentage
    compute_fees_to_farmers: Percentage
    compute_fees_tax_to_operators: Percentage

    # Slash Parameters
    slash_to_fund: Percentage
    slash_to_holders: Percentage

    # Behavioral Parameters
    operator_stake_per_ts_function: Callable[['SubspaceModelParams', SubspaceModelState], Percentage]
    nominator_stake_per_ts_function: Callable[['SubspaceModelParams', SubspaceModelState], Percentage]
    transfer_farmer_to_holder_per_day_function: Callable[['SubspaceModelParams', SubspaceModelState], Percentage]
    transfer_operator_to_holder_per_day_function: Callable[['SubspaceModelParams', SubspaceModelState], Percentage]
    transfer_holder_to_nominator_per_day_function: Callable[['SubspaceModelParams', SubspaceModelState], Percentage]
    transfer_holder_to_operator_per_day_function: Callable[['SubspaceModelParams', SubspaceModelState], Percentage]

    # Environmental Parameters
    ## Environmental: Fees
    #base_fee_function: Callable[[bool], Percentage]
    #min_base_fee: Credits
    priority_fee_function: Callable[['SubspaceModelParams', SubspaceModelState], Percentage]

    ## Enviromental: Compute Weights per Tx
    compute_weights_per_tx_function: Callable[['SubspaceModelParams', SubspaceModelState], ComputeWeights]
    min_compute_weights_per_tx: ComputeWeights
    compute_weight_per_bundle_function: Callable[['SubspaceModelParams', SubspaceModelState], ComputeWeights]
    min_compute_weights_per_bundle: ComputeWeights

    ## Environmental: Tx Sizes
    transaction_size_function: Callable[['SubspaceModelParams', SubspaceModelState], Bytes]
    min_transaction_size: Bytes
    bundle_size_function: Callable[['SubspaceModelParams', SubspaceModelState], Bytes]
    min_bundle_size: Bytes  # TODO: confirm

    ## Environmental: Tx Count
    transaction_count_per_day_function: Callable[['SubspaceModelParams', SubspaceModelState], float]
    bundle_count_per_day_function: Callable[['SubspaceModelParams', SubspaceModelState], float]

    ## Environmental: Slash Count
    slash_per_day_function: Callable[['SubspaceModelParams', SubspaceModelState], float]

    ## Environmental: Space Pledged per Time
    new_sectors_per_day_function: Callable[['SubspaceModelParams', SubspaceModelState], float]


# Logic implementation types
StochasticFunction = Callable[[SubspaceModelParams, SubspaceModelState], float]


