
# Defining Credit Supply for Storage Fee Purposes

*Danilo Lessa Bernardineli (BlockScience), 20 December 2023*

## Conclusions

Based on the expressed requirements, adopting **Circulating Supply** as the measure of Credit Supply is the option that satifies most items, with concerns added on the game-ability due to the possibility of users staking / un-staking in order to interefere with the Storage Fee Price.

Another option that satisfies the listed requirements is the **Total Supply** (Issued Supply minus Burnt Supply), however it has a trade-off on which sensitivity towards user activity can be relatively small due to the huge weight of the future vesting supply.

Lastly, there's **Gross Circulating Supply** (Earned Supply minus Burnt Supply), which is sensitive to the vesting schedule and therefore does not fullfill R3. However, it is relatively sensitive to user activity while not being game-able.

## Requirements & Considerations

- R1: It is expected that mint/burn-based mechanisms will affect how credit supply is measured.
- R2: Burns will be core to the assymptotic cost of storage
- R3: The sudden shock on storage fee pricing due to the vesting schedule is undesirable and should be mitigated

## Candidate Solutions

![Screenshot 2023-12-20 at 13.38.58](https://hackmd.io/_uploads/BkH3d9lwp.png)
*Taxonomy for the different supply terminologies*


Below, we indicate candidate for the Credit Supply definitions in terms of Definitions, Meaning and Implications of Adopting. The ordering is based on an perceived ranking of responsiveness of storage fee prices towards user activity. Less volatile / More unresponsive definitions are listed first, and more volatile / more responsive are left for last.

- Issued Supply
    - Definitions
        1. `= EarnedSupply(t) + FutureVestingSupply(t)`
        2. `= Maximum Supply - FutureRewardsSupply(t)` 
    - Meaning: how much credits were put into existence
    - Implications of Adopting: 
        - Least sensitivity of the storage fee prices towards user activity, mediated solely by the inflation rate.
        - This number will always go up, which will generate an monotonic pressure for increasing the storage fee prices 
        - This number is not affected by the vesting schedule, which can mitigate a sudden shock on the storage fee price after 1 year.
        - R1: No
        - R2: No
        - R3: Yes
- Total Supply
    - Definitions
        1. `= IssuedSupply(t) - BurntSupply(t)`
    - Meaning: how much credits do exists
    - Implications of Adopting:  
        - Some sensitivity of the storage fee prices towards user activity.
        - This number can fluctuate up or down, which will generate varying pressures on the storage fee prices.
        - This number is not affected by the vesting schedule, which can mitigate a sudden shock on the storage fee price after 1 year.
    - Met Requirements?
        - R1: Yes
        - R2: Yes, with low sensitivity initially
        - R3: Yes
- Earned Supply
    - Definitions
        1. `= RewardedSupply(t) + VestedSupply(t)`
        2. `= IssuedSupply(t) - FutureVestingSupply(t)`
        3. `= ReserveSupply(t) + CirculatingSupply + LockedUserSupply(t)`
        4. `= MaximumSupply(t) - FutureIssuance(t)`
    - Meaning: how much credits were activated
    - Implications of Adopting: 
        - Some sensitivity of the storage fee prices towards user activity.
        - This number will always go up, which will generate an monotonic pressure for increasing the storage fee prices
        - The vesting schedule is likely to introduce a upward storage fee price shock.
    - Met Requirements?
        - R1: No
        - R2: No
        - R3: No
- Gross Circulating Supply
    - Definitions
        1. `= EarnedSupply(t) - BurntSupply(t)`
        2. `= TotalSupply(t) - FutureVestingSupply(t)`
    - Meaning: how much credits are active
    - Implications of Adopting: 
        - This number can fluctuate up or down, which will generate varying pressures on the storage fee prices.
        - The vesting schedule is likely to introduce a upward storage fee price shock.
    - Met Requirements?
        - R1: Yes
        - R2: Yes
        - R3: No
- Circulating Supply
    - Definitions
        1. `= GrossCirculatingSupply(t) - ReserveSupply(t) - LockedUserSupply(t)`
    - Meaning: how much credits are under immediate user control.
    - Implications of Adopting
        - Highest sensitivity of storage fee prices towards user activity. 
        - This number can fluctuate up or down, which will generate varying pressures on the storage fee prices.
        - Can imply high volatility of storage fee prices
        - Concerns on the game-ability on the storage fee price that is conditional on the staking period rules.
        - The effect of the vesting schedule is not trivial, as they need to be unlocked and transfered from the EVM domain, which temporarily smoothens the storage fee price shock.
    - Met Requirements?
        - R1: Yes
        - R2: Yes
        - R3: Yes

