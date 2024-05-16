# Issuance Function for Subspace

*the original version of [this document on HackMD](https://hackmd.io/@blockscience/rJDEKiQBa)*

## Elements for Designing an Issuance Function

### Desired function

One or many hypothesis on $B(t) = \int_t^{t+1}b(t) dt$, where $t$ is in any of Block/Day/Year unit and $B(t)$ is the cummulative reward on the period. An discrete version is also acceptable. 

### Properties

- Requirements
    - R1: Should have an capped supply 
        - :question: It is unclear if "capped supply" means "cap on cummulative issuance" or "cap on circulating supply" 
    - R2: The Available Token Supply should always be at least 51% Community Owned (eg. distributed through Issuance)
        - `Available Token Supply = Vested + Issued - Burnt`
        - `Community Owned Supply = k * Vested + Issued - Burnt`
        - Note: this is an system-wide rather than mechanism-wide requirement.
    - R3: Should have an notion of an "subsidy parameter"
        - This is understood as being an (possibly dynamical) multiplier on the Output Gap and/or Utilization rate
        - Can be either static, dynamical and periodically adjusted
    - R4: Should have an notion of an "target inflation rate"
        - This seems to be an multiplier on the rewards
        - Can be either static and dynamical
- Desirables
    - D1: "Farmers subsidies should be dynamic relative to the aggregate storage fees"
    - D2: "It should avoid that tokens are consistently issued at the maximum inflation rate when nobody is using the network"
    - D3: "When demand is low and storage rewards are few, block producers get increased issuance"
    - D4: Subsidy should be higher when shortfall is higher 
        - Definition 1: `Shortfall = Costs - Revenue`
        - Definition 2: `Shortfall = min(Costs - Revenue, 0)`
    - D5: Subsidy should be higher when output gap is lower.
        - `G(t) = MaxBlockSize - ActualBlockSize`


### Available State Information

- I1: Block Reward per block since launch
- I2: Storage Fees per block since launch
- I3: Compute Fees per block since launch
- I4: Staking Pool Volume per block since launch
- I5: Issued & Burnt Supply per block since launch
- I6: Vested Supply per block since launch
- I7: Transaction Count per block since launch
- I8: Block Utilization per block since launch
    - Defined as $u(t)=\frac{\sum_i \text{num}(t_i)*\text{size}(t_i)}{\text{MaxBlockSize}}$
- 

### Issuance Functions that were considered

- F1 (before DI): $B(t) = B_0 e^{-kt} \pi^T(1-u(t))$, where $B_0$ is the block reward at $t=0$, $k$ is an decay constant, $\pi^T$ is the target inflation rate and $u(t)$ is the utilization rate.
    - $B(t)$ is defined as the total block reward disbursed at year $t\in\mathbb{N}$.
    - Note: In order to be valid, an continuous Issuance function $b(t)$ would need to be defined such as $\int_{0+i*n_y}^{(i+1)n_y}b(t)dt = \pi(t), \forall i \in \mathbb{N}$ and $n_y$ is the count of blocks per year. The Block Reward between $t-1$ and $t$ would then be defined as $\int_{t-1}^t b(t) dt$
- F2 (DI): $\pi(t) = \int_{{t_i}}^{t_{i+1}} \alpha G(t)dt$, where $\alpha$ is the Subsidy Parameter and $G(t)$ is the Output Gap, defined as $G(t) =\text{MaxBlockSize} - \sum_i \text{num}(t_i)*\text{size}(t_i)$ (associated with the Utilization Rate).
    - Matt suggests using $\alpha=\frac{\text{FarmerRevenue(t)}-\text{FarmerCosts(t)}}{G(t)}$, which leads to $\pi(t) = \int_{t_i}^{t_{i+1}} \text{FarmerRevenue}(t) - \text{FarmerCosts}(t)$. He suggests defining $\text{FarmerRevenue(t)} = \sum_\tau \text{WillingnessToPay}(\tau) + Subsidy(\tau)$. He also did suggest using opportunity costs (such as average S3 storage costs) for the $\text{FarmerCosts}$
        - $\text{Subsidy}(t)$ probably means $\int_{t_1}^{t_2}b(t) dt$
        - $\text{WillingnessToPay}$ can be pretty much anything (incl. negative values associated with discount factors?)
    - The $\alpha$ parameter is an global parameter rather than per-farmer.
- F3 (for dev. testing): $\pi(t) = \int_{t_i}^{t_{i+1}} k (\hat{b}_p + N_v \hat{b}_v) dt$, where $k$ is an constant (0.1 TSSC), $\hat{b}_p$ is the unit vector for the Block Proposer and $\hat{b}_v$ is for Block Voters Group, and $N_v$ is the number of Block Voters. $t_i$ is the time associated with block $i$.

### Additional context

Todd's message on slack:

In the next implementation phase, we'll need further assistance:
- testing scenarios of the relevant system parameters
- determine the target inflation rate
    - is the target rate fixed or variable based on network conditions?
- determine the subsidy parameter
    - how and over what time period to we test blockspace utilization, and therefore adjust the subsidy parameter <> target rate?
        - emptier blocks increase the subsidy rate towards the target
        - fuller blocks decrease the subsidy rate toward zero
- once this issuance model has been fundamentally defined, Dariia may require assistance translating this into functional code
