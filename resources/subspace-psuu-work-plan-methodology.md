# Subspace PSuU Work Plan

*BlockScience (March 2024)*


## What is PSuU (Parameter Selection Under Uncertainty)?

*Fig. An overview of the PSuU Pipeline.*
![](https://hackmd.io/_uploads/SJRLVdwA6.png)

PSuU is a methodology that enables an agile process for evaluating the causal effect of the Governance Surface parameters into effects of interest (e.g. KPIs or Goal-as-Utilities). It employs machine learning classifiers to perform pattern learning at scale. More information can be found at the ["How to Perform Parameter Selection Under Uncertainty"](https://medium.com/block-science/how-to-perform-parameter-selection-under-uncertainty-976931ba7e5d) and ["From High Dimensional Data to Insights"](https://hackmd.io/1iTUMQoAS8WCQu4IvyXMzA) documents or the [OMNIPool Engineering & Simulation Lectures](https://youtu.be/lgug3f6Qz6I?si=UctEzJpueWl0_4BO) and [Informing the Filecoin Launch through Cryptoeconomics and Simulations](https://www.youtube.com/watch?v=kBzwgfnk91c&t=560s) public recordings.

Generally, the type of answer that PSuU can facilitate can be formulated, such as:

> "Under all tested scenarios, it is found that **(Higher/Lower)** values of **(Governable Parameter)** has a **(significant/somewhat/inconclusive/none)** effect on steering the system towards fullfing **(KPI/Goal)**."

An analyst can also utilize PSuU for trade-off analysis across differing parameters. For example, is overoptimizing for a specific goal synergistic or competitive with fulfilling other goals?

Based on the above, it is possible to develop a set of recommendations that can be tailored for optimizing either per-goals or through a combined approach, on which the goals are given equal or differing weights.


## Workflow

1. For each Environmental Group, compute all the Environmental Scenarios that belong to that group. The union of all will be our set of Environmental Scenarios.
    - eg. if EG1 has 3 scenarios, and EG2 has 4 scenarios, then we'll have 7 environmental scenarios. 
    - MC runs should be considered as independent scenarios. Eg. 10 MC runs should be interpreted as 10 env. scenarios. If a ESG has 3 base scenarios with 10 MC runs each, then we'll end up with 30 environmental trajectories
3. Compute all governable parameter combinations. This will be our set of Governable Scenarios
4. The cartesian product between the Governable Scenarios and the Environmental Scenarios will be our set of Trajectories to be simulated.
4. Compute the `Per-Timestep Tensor` by executing the `cadCAD` simulation on the entire set of trajectories.
5. For each Trajectory, compute the relevant Per-Trajectory metrics and genera the `Per-Trajectory Tensor`
6. For each Goal, compute the utility function by grouping over the GS parametrizations. (if we have 4 parameter combinations, this means that we'll have 4 computed utilities)
7. Perform Regression Analysis by taking the Per-Goal Utilities as outputs and the Governance Surface parameter values as inputs.
    - This can be done readily by applying the [`cadCAD_machine_search`](https://github.com/cadCAD-org/cadCAD_machine_search) library, although more sophisticated approaches can be implemented as time and requirements allows.
    - This analysis may also admit a variation on which trajectories are grouped per Controllable Parameters and per Environmental Group.

## Methodology

### Assumptions of the Model
To enable such an economic model, several assumptions were made. Assumption implementations are indicated with XXX tags through out the repository. Some of the assumptions of the model include:
- There is a hard cap on farmer rewards issuance
- Nominators and Operators will stake a portion of their free balance on every timestep
- average_priority_fee is stochastically sampled
- average_compute_weight_per_tx is stochastically sampled
- average_compute_weight_per_bundle is stochastically sampled

### Goals of the System
The overarching goals for the protocol issuance were designed to align the economic parameters with the broader objectives of the network:

1. **Rational Economic Incentives:** Ensuring the economic parameters encourage behaviors supporting the network's long-term viability and growth.
    - Incentives should be proportional to effort. 
    - Participation is smooth.
2. **Community Incentivization:** Creating incentives that encourage participation from all defined stakeholders (farmers, operators, nominators).
    - Community owned supply should be maximized
    - Rewards should be spread across as many actors as possible
    - Early adopters should be incentivized
3. **Supply and Demand Equilibrium / Distributional Equilibrium:** Balancing the issuance and distribution of tokens to support both the network's scalability and the fair distribution of resources among participants.
- Increase in supply (eg. space pledged and operator pools) should track increases in demand (eg. storage & compute fees).


### Key Performance Indicators
1. **Community Owned Supply Percentage:** How much of total supply is held by the community?
2. **Average Daily Farmer Subsidy Factor:** What percentage of farmer rewards are coming from the reference subsidy?
3. **Average Daily Proposer Rewards per Pledged Space:** How many SSC are proposers rewarded per pledged space?
4. **Average Daily Proposer Rewards Not Including Voting Rewards:** Proposer rewards without voting rewards.
5. **Cumulative Rewards Distributed in First Year:** Total block rewards in first year.
6. **Ratio of Storage Fees per Compute Fees:** How many storage fees are paid per compute fee paid?
7. **Cumulative Rewards:** Total block rewards distributed over the entire simulation (3 years).

### Controllable Parameters

The purpose of this economic modeling work is to advise the subspace team
towards the selection of initialization parameters for the subspace system. The
space of possible initialization configurations is known as the governance
surface. The purpose of the PSuU methodology is to identify points on the
governance surface that increasing the likely utility of KPIs that are
associated with desired goals. 

The following subspace network initialization parameters have been analyzed using the PSuU methodology:
1. **Reference Subsidy Component #1:** 
2. **Reference Subsidy Component #2:**
3. **Reward Proposer Share:**
4. **Compute Weight to Fee Parameter:**

### Governance Surface

| Parameter| Prioritization | Set of Values to Test |
| -------- | -------- | -------- |
| Ref. Subsidy Component 1 & 2 Start Time|Important|{0, 14 days, 30 days}|
| Ref. Subsidy Component 1, Initial Subsidy|Important|{1SSC/blk, 4SSC/blk, 7SSC/blk}|
| Ref. Subsidy Component 1, Maximum Cummulative Subsidy|Important|{10%, 30% and 50%}|
| Ref. Subsidy Component 2 Initial Subsidy Duration|Important|{6mo, 1yr, 2yr, 4yr}|
| Ref. Subsidy Component 2, Initial Subsidy|Important|{1SSC/blk, 4SSC/blk, 7SSC/blk}|
| Ref. Subsidy Component 2, Maximum Cummulative Subsidy|Important|{10%, 30% and 50%}|
|Proposer Share of Block Rewards|Important|{10%, 33%}|
|Compute Fee Weight To Fee (ComputePicosecond Per Shannon)| Important| {1, 100, 1,000, 10,000}|
|Global Reward Initialization Threshold in terms of Space Pledged (Space Race)|Nice to Have|{50PiB, 100PiB, 500PiB}|
|Percentage of Compute Fee to Farmers|Nice to Have|{0%}|
|Operator Tax|Nice to Have|{0, 10%, 50%}|
|Percentage of Slash to Burn|Optional|{100%, 50%}|
|Percentage of Slash to the Foundation|Optional|{0%, 50%}|
|Percentage of Slash to Farmers|Optional|{0%}|
|Expected Votes per Block|Out of Scope|{1}|
| Ref. Subsidy Component 1, Initial Subsidy Duration|Out of Scope|{0.0}|


### Environmental Scenarios

The following behavioral inputs are modulated per run according to the defined environmental scenarios:
1. **Utilization Ratio**
2. **Operator Stake per Transaction**
3. **Nominator Stake per Transaction**
4. **Transfers from Operators to Farmers per Day**
5. **Transfers from Farmers to Nominators per Day**
6. **Transfers from Farmers to Operators per Day**


### Scenario Groups

The four types of environmental scenarios include the following:
1. **Standard Run:** Value is sampled from a normal distribution with low coefficient of variation
2. **Volatile Run:** Value is sampled from a normal distribution with high coefficient of variation
3. **Standard Run with Instantaneous Shocks:** Value is sampled from a normal distribution with low coefficient of variation, with periodic instances of high variation.
4. **Standard Run with Sustained Shocks:** Value is sampled from a normal distribution with low coefficient of variation, with periodic durations of high variation.


### Environmental Variable Values
- DAo: Daily Average Of
- Parameters
    - DAo Utilization Ratio = `{0.5%, 1%, 2%}`
        - DAo Transaction Volume = DAo Utilization Ratio * max_block_size
        - DAo Transaction Size = Constant
        - DAo Transaction Count = DAo Transaction Volume / DAo Transaction Size
    -  Newly Pledged Space per Day = `{0.25 PB/d, 1 PB/d, 5 PB/d}`
    -  Priority Fee per Time = `{0% of ComputeFee, }`
    -  Slash Count per Time = `{0}`
    -  Operator Stake per Time = `{10%}`
    -  Nominator Stake per Time = `{10%}`
    -  Farmer-Holder Transfer per Time = `{100%}`
    -  Operator-Holder Transfer per Time = `{10%}`
    -  Holder-Nominator Transfer per Time = `{2.5%}`
    -  Holder-Operator Transfer per Time = `{2.5%}`


### Trajectory Datasets
Running the PSuU methodology across the parameters described above generates two key datasets:

**The Timestep Tensor:** An (CXSXTXRXM) Tensor  
- C = Controllable Parameter Sweeps
- S = Scenario Sweeps
- R = Number of Monte Carlo Runs per Simulation
- T = Number of Timesteps per Run
- M = Number of Measurements Observe per Timestep

**The Trajectory Tensor:** An (CXSXRXK) Tensor  
- K is the number of KPIs
- This is The Timestep Tensor aggregated over time by run
- Contains Controllable Parameters as Index
- Contains KPI Outcomes as Values
- Can be Used for Machine Learning Analysis

**The Utility Tensor:** An (CXSXRXK) Binary Tensor  
- This is the result of Utility Functions applied to the Trajectory Tensor
- KPI values are mapped to 0 or 1 to indicate whether or not they meet a success criteria

Observe that the size of the Trajectory Tensor is K/(T*M) the size of the
Timestep Tensor. Considering K=7, T=1096, M=40, then the Trajectory Tensor is
about 1/6000 the size of the Timestep Tensor. This is important to keep in mind
When running large simulations, as timestep tensors might not always fit in
memory or on disk.

### Per Trajectory Metrics

|Identifier|Metric|Applicable Goals|Threshold|Importance Weight|Meaning|
|-|-|-|-|-|-|
|T1|Average over Daily-Average Community Owned Supply Fraction|G2|LMaT|1|Higher average COSf is preferred|
|T2|Average over Daily-Average Farmer Subsidy Factor|G3|BMaT|1|Having less subsidies relative to fees is preferred|
|T3|Average over Daily-Sum of Proposing Rewards per Newly Pledged Space|G1|LMaT|1|Proposing rewards being higher than proposing costs is preferred|
|T4|Average over Daily-Sum of Proposer Reward Minus Per-Voter Reward|G1|LMaT|1|Proposers having a reward premium over voters is preferred|
|T5|Sum over Daily-Sum of Rewards for the first 1 year|G2|LMaT|1|Priotization of early adopters us preferred
|T6|Modulus of Average-1 over Daily-Sum of Storage Fees Per Daily-Sum of (Storage Fees + Compute Fees)|G3|BMaT|1|The order of magnitude of Storage and Compute Fees are as close as possible|
|T7|Sum over Daily-Sum of Rewards|G3|BMaT|1|Less Issuance is preferred|

### Threshold Rules

- BMaT: Below the Median across Trajectories
- LMaT: Larger than the Median across Trajectories


### Per-Goal Utility Functions

$$
\pi_j(C) = \sum k_i * T_i, \, T_i \in \mathcal{T}_j
$$


### Machine Learning Analysis

**Utility Maximizing Decision Trees:**  
    - Decision trees are applied to the Utility Tensor to illustrate the importance of parameter selection values on utility criteria outcomes.

**Regressing Analysis of Parameter Impact on Goals:**  
    - Density plots and linear regression are used to indicate the effects of parameter selection on utility outcomes.


## Additional Resources

- [How to Perform Parameter Selection Under Uncertainty (essay)](https://medium.com/block-science/how-to-perform-parameter-selection-under-uncertainty-976931ba7e5d)
- [From High Dimensional Data to Insights](https://hackmd.io/1iTUMQoAS8WCQu4IvyXMzA)
- [Informing the Filecoin Launch through Cryptoeconomics and Simulations (video)](https://www.youtube.com/watch?v=kBzwgfnk91c&t=560s)
- [Algorithms for Decision-Making (book)](https://algorithmsbook.com/#)
- [Algorithms for Optimization (book)](https://algorithmsbook.com/optimization/)
- [Data-Driven Decision Making for Token Economies (slides)](https://docs.google.com/presentation/d/1voi_cIvwBZt2TgnMkPdRX2uj3T6AcXxWFnAcu6tHxyw/edit#slide=id.gfc093b621d_0_813)
- [OMNIPool Engineering & Simulation Lectures (video)](https://youtu.be/lgug3f6Qz6I?si=UctEzJpueWl0_4BO)
- [Informing the Filecoin Launch through Cryptoeconomics and Simulations (slides)](https://docs.google.com/presentation/d/1EMpQ744QzL00a4T_VCj3xyrn6PqGSKBSEWxvhPnYYew/edit?usp=sharing)

