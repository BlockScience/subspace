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


## Goals

- G1: Rational Economic Incentives
    - E.g. Incentives should be proportional to effort. Participation is smooth.
- G2: Community Incentivization
    - E.g. COS should somehow be maximized or required to fullfill certain requirements.
    - E.g. Rewards should be spread across as many actors as possible
    - E.g. Early adopters should be incentivized
- G3: Supply and Demand Equilibrium / Distributional Equilibrium
    - E.g. Increases in supply (eg. space pledged and operator pools) should track increases in demand (eg. storage & compute fees). 

### Per-Goal Utility Functions

\begin{align}
\pi_j(C) &= \sum k_i * T_i,  T_i \in \mathcal{T}_j\\
\end{align}


## Per Trajectory Metrics

### Threshold Rules

- BMaT: Below the Median across Trajectories
- LMaT: Larger than the Median across Trajectories

### Metrics

- Missing Metrics: 
    - How to measure optimized distribution between proposers & voters?
    - How to measure Reasonable rewards per-block/hour/month/etc. In USD terms
    - How to measure operator incentivization
    - How to measure network usage
    - How to measure resilence towards usage shocks

|Identifier|Metric|Applicable Goals|Threshold|Importance Weight|Meaning|
|-|-|-|-|-|-|
|T1|Average over Daily-Average Community Owned Supply Fraction|G2|LMaT|1|Higher average COSf is preferred|
|T2|Average over Daily-Average Farmer Subsidy Factor|G3|BMaT|1|Having less subsidies relative to fees is preferred|
|T3|Average over Daily-Sum of Proposing Rewards per Newly Pledged Space|G1|LMaT|1|Proposing rewards being higher than proposing costs is preferred|
|T4|Average over Daily-Sum of Proposer Reward Minus Per-Voter Reward|G1|LMaT|1|Proposers having a reward premium over voters is preferred|
|T5|Sum over Daily-Sum of Rewards for the first 1 year|G2|LMaT|1|Priotization of early adopters us preferred
|T6|Modulus of Average-1 over Daily-Sum of Storage Fees Per Daily-Sum of (Storage Fees + Compute Fees)|G3|BMaT|1|The order of magnitude of Storage and Compute Fees are as close as possible|
|T7|Sum over Daily-Sum of Rewards|G3|BMaT|1|Less Issuance is preferred|


## Governance Surface





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

## Environmental Scenarios

### Environmental Variables

| Variable | Type | Observable? |
| -------- | -------- | -------- |
|Priority Fee per Time | Possibly Dynamical| Yes     |
|Compute Weights per Transaction|Random|Yes||
|Compute Weights per Bundle|Random|Yes||
|Size per Transaction|Random|Yes||
|Size per Bundle|Random|Yes||
|Slash Count per Time|Random|Yes||
|Transaction Count per Time|Behavioral|Yes||
|Bundle Count per Time|Behavioral|Yes||
|New Sectors per Time|Behavioral|Yes||
|Operator Stake per Time|Behavioral|Yes||
|Nominator Stake per Time|Behavioral|Yes||
|Farmer-Holder Transfer per Time|Behavioral|No||
|Operator-Holder Transfer per Time|Behavioral|No||
|Holder-Nominator Transfer per Time|Behavioral|No||
|Holder-Operator Transfer per Time|Behavioral|No||

### Scenario Groups

- Scenario Group 1: Predictable Trajectory
    - All behavioral variables are assigned a low-volatility distribution. (eg. CoV of 30%)
- Scenario Group 2: High-Volatility Trajectory
    - All behavioral variables are assigned a high-volatility distribution. (eg. CoV of 500%)
- Scenario Group 3: Predictable Trajectory with Instantaeous Shocks
    - All behavioral variables are assigned a low-volatility distribution (eg. CoV of 30%), with intermittent shocks (eg. an order of magnitude decrease or increase) occuring on average every N weeks
- Scenario Group 4: Predictable Trajectory with Sustained Shocks
    - All behavioral variables are assigned a low-volatility distribution (eg. CoV of 30%), with intermittent shocks (eg. an order of magnitude decrease or increase) occuring on average every N weeks. Those shocks will be sustained by an certain amount of days (eg. M days on average)

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







## Resources

- [How to Perform Parameter Selection Under Uncertainty (essay)](https://medium.com/block-science/how-to-perform-parameter-selection-under-uncertainty-976931ba7e5d)
- [From High Dimensional Data to Insights](https://hackmd.io/1iTUMQoAS8WCQu4IvyXMzA)
- [Informing the Filecoin Launch through Cryptoeconomics and Simulations (video)](https://www.youtube.com/watch?v=kBzwgfnk91c&t=560s)
- [Algorithms for Decision-Making (book)](https://algorithmsbook.com/#)
- [Algorithms for Optimization (book)](https://algorithmsbook.com/optimization/)
- [Data-Driven Decision Making for Token Economies (slides)](https://docs.google.com/presentation/d/1voi_cIvwBZt2TgnMkPdRX2uj3T6AcXxWFnAcu6tHxyw/edit#slide=id.gfc093b621d_0_813)
- [OMNIPool Engineering & Simulation Lectures (video)](https://youtu.be/lgug3f6Qz6I?si=UctEzJpueWl0_4BO)
- [Informing the Filecoin Launch through Cryptoeconomics and Simulations (slides)](https://docs.google.com/presentation/d/1EMpQ744QzL00a4T_VCj3xyrn6PqGSKBSEWxvhPnYYew/edit?usp=sharing)

