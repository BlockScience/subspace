from typing import Annotated, TypedDict, Union
from dataclasses import dataclass


Days = Annotated[float, 'days']  # Number of days
Credits = Annotated[float, "SSC"] 
PerYear = Annotated[float, "1/year"]  # Yearly rate
Year = Annotated[float, "year"]  # Number of years
Percentage = Annotated[float, '%']
CreditsPerComputeUnits = Annotated[float, 'SSC/CU']
ComputeUnits = Annotated[float, 'CU']
Shannon = Annotated[float, "Shannon"] # 1e-18 SSC 
ShannonPerComputeUnits = Annotated[float, 'Shannon/CU']
Bytes = Annotated[int, 'bytes']


@dataclass
class TokenDistribution():
    # Stocks
    issuance_balance: Credits
    operators_balance: Credits
    nominators_balance: Credits
    holders_balance: Credits
    farmers_balance: Credits
    staking_pool_balance: Credits
    fund_balance: Credits
    burnt_balance: Credits

    @property
    def circulating_supply(self):
        return (self.operators_balance 
                + self.nominators_balance 
                + self.holders_balance
                + self.farmers_balance)
    
    @property
    def user_supply(self):
        return self.circulating_supply + self.staking_pool_balance
    
    @property
    def issued_supply(self):
        return self.user_supply + self.fund_balance + self.burnt_balance

class SubspaceModelState(TypedDict):
    # Time Variables
    days_passed: Days
    delta_days: Days

    # Stocks
    token_distribution: TokenDistribution

    # Deterministic Variables
    block_reward: Credits

    # Stochastic Variables
    average_base_fee: ShannonPerComputeUnits
    average_priority_fee: ShannonPerComputeUnits
    average_compute_units: ComputeUnits
    average_transaction_size: Bytes
    transaction_count_per_timestep: int


class SubspaceModelParams(TypedDict):
    label: str
    timestep_in_days: Days
    reward_proposer_share: Percentage

    # Fees & Taxes
    fund_tax_on_proposer_reward: Percentage
    fund_tax_on_storage_fees: Percentage
    farmer_tax_on_compute_priority_fees: Percentage
    operator_tax_on_compute_revenue: Percentage

class SubspaceModelSweepParams(TypedDict):
    label: list[str]
    timestep_in_days: list[Days]