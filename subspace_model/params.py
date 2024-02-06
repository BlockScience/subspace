from dataclasses import dataclass

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
    SUPPLY_ISSUED,
    TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50,
    TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS,
    WEEKLY_VARYING,
)


class SubspaceModelParams(TypedDict):
    label: str
    timestep_in_days: Days

    # Mechanisms to be determined
    issuance_function: Callable
    slash_function: Callable[[SubspaceModelState], Credits]

    # Implementation parameters
    block_time_in_seconds: Seconds
    archival_depth: Blocks
    archival_buffer_segment_size: Bytes
    header_size: Bytes
    min_replication_factor: float
    max_block_size: Bytes

    # Economic Parameters
    reward_proposer_share: Percentage
    max_credit_supply: Credits
    credit_supply_definition: Callable[[SubspaceModelState], Credits]

    # Fees & Taxes
    fund_tax_on_proposer_reward: Percentage
    fund_tax_on_storage_fees: Percentage
    compute_fees_to_farmers: Percentage
    compute_fees_tax_to_operators: Percentage

    # Slash Parameters
    slash_to_fund: Percentage
    slash_to_holders: Percentage

    # Behavioral Parameters
    operator_stake_per_ts_function: Callable[[bool], Percentage]
    nominator_stake_per_ts_function: Callable[[bool], Percentage]
    # operator_avg_stake_per_ts: Callable[[bool], Percentage]
    # nominator_avg_stake_per_ts: Callable[[bool], Percentage]
    # operator_std_stake_per_ts: Callable[[bool], Percentage]
    # nominator_std_stake_per_ts: Callable[[bool], Percentage]
    transfer_farmer_to_holder_per_day: Percentage
    transfer_operator_to_holder_per_day: Percentage
    transfer_holder_to_nominator_per_day: Percentage
    transfer_holder_to_operator_per_day: Percentage

    # Environmental Parameters
    base_fee_function: Callable[[bool], Percentage]
    # avg_base_fee: Credits
    # std_base_fee: Credits
    min_base_fee: Credits

    priority_fee_function: Callable[[bool], Percentage]
    # avg_priority_fee: Credits
    # std_priority_fee: Credits

    compute_weights_per_tx_function: Callable[[bool], ComputeWeights]
    # avg_compute_weights_per_tx: ComputeWeights
    # std_compute_weights_per_tx: ComputeWeights
    min_compute_weights_per_tx: ComputeWeights

    compute_weights_per_bundle_function: Callable[[bool], ComputeWeights]
    # avg_compute_weights_per_bundle: ComputeWeights
    # std_compute_weights_per_bundle: ComputeWeights
    min_compute_weights_per_bundle: ComputeWeights

    transaction_size_function: Callable[[bool], Bytes]
    # avg_transaction_size: Bytes
    # std_transaction_size: Bytes
    min_transaction_size: Bytes

    bundle_size_function: Callable[[bool], Bytes]
    # avg_bundle_size: Bytes # TODO: confirm
    # std_bundle_size: Bytes # TODO: confirm
    min_bundle_size: Bytes  # TODO: confirm

    transaction_count_per_day_function: Callable[[bool], float]
    # avg_transaction_count_per_day: float
    bundle_count_per_day_function: Callable[[bool], float]
    # avg_bundle_count_per_day: float

    slash_per_day_function: Callable[[bool], float]
    # avg_slash_per_day: float
    new_sectors_per_day_function: Callable[[bool], float]
    # avg_new_sectors_per_day: float
    # std_new_sectors_per_day: float


DEFAULT_PARAMS = SubspaceModelParams(
    label="standard",
    environmental_label="standard",
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
    min_replication_factor=10,
    max_block_size=int(3.75 * MIB_IN_BYTES),  # 3.75 MiB
    weight_to_fee=1 * SHANNON_IN_CREDITS,
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
    "stochastic": {
        # Behavioral Parameters Between 0 and 1
        "operator_stake_per_ts_function": MAGNITUDE(NORMAL_GENERATOR(0.01, 0.02)),
        "nominator_stake_per_ts_function": MAGNITUDE(NORMAL_GENERATOR(0.01, 0.02)),
        "transfer_farmer_to_holder_per_day_function": MAGNITUDE(
            NORMAL_GENERATOR(0.05, 0.05)
        ),
        "transfer_operator_to_holder_per_day_function": MAGNITUDE(
            NORMAL_GENERATOR(0.05, 0.05)
        ),
        "transfer_holder_to_nominator_per_day_function": MAGNITUDE(
            NORMAL_GENERATOR(0.01, 0.02)
        ),
        "transfer_holder_to_operator_per_day_function": MAGNITUDE(
            NORMAL_GENERATOR(0.01, 0.02)
        ),
        # Environmental Parameters (Integer positive in [0,inf])
        "environmental_label": "stochastic",
        "base_fee_function": POSITIVE_INTEGER(NORMAL_GENERATOR(1, 1)),
        "priority_fee_function": POSITIVE_INTEGER(NORMAL_GENERATOR(3, 5)),
        "compute_weights_per_tx_function": POSITIVE_INTEGER(
            NORMAL_GENERATOR(60_000_000, 15_000_000)
        ),
        "compute_weight_per_bundle_function": POSITIVE_INTEGER(
            NORMAL_GENERATOR(10_000_000_000, 5_000_000_000)
        ),
        "transaction_size_function": POSITIVE_INTEGER(NORMAL_GENERATOR(256, 100)),
        "bundle_size_function": POSITIVE_INTEGER(NORMAL_GENERATOR(1500, 1000)),
        "transaction_count_per_day_function": POISSON_GENERATOR(1 * BLOCKS_PER_DAY),
        "bundle_count_per_day_function": POISSON_GENERATOR(6 * BLOCKS_PER_DAY),
        "slash_per_day_function": POISSON_GENERATOR(0.1),
        "new_sectors_per_day_function": POSITIVE_INTEGER(NORMAL_GENERATOR(1000, 500)),
    },
    "weekly-varying": {
        "environmental_label": "weekly-varying",
        "base_fee_function": WEEKLY_VARYING,
        "priority_fee_function": WEEKLY_VARYING,
    },
    "constant-utilization": {
        "environmental_label": "constant-utilization",
        "transaction_count_per_day_function": TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50,
    },
    "growing-utilization": {
        "environmental_label": "growing-utilization",
        "transaction_count_per_day_function": TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS,
    },
}
