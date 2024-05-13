# The Subspace Network Economic Digital Twin 

A cadCAD Design Digital Twin for Subspace Network Economic Dynamics.

![](resources/ssc-stock-flow.png)
*A stock and flow description for SSC on the tokenomics of Subspace. This model uses this as the departure point for the dynamics being simulated.*

## Quick Start Guide

### Installation

Requires:
- [>= Python 3.6](https://www.python.org/downloads/) 
- One of [`venv`](https://docs.python.org/3/library/venv.html) or [`poetry`](https://python-poetry.org/) for python virtual environment.

First clone the repository.
```bash
git clone https://github.com/blockscience/subspace && cd subspace
```

Installation Option 1: Using `venv` virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m subspace_model
```
Installation Option 2: Using python poetry
```bash
poetry install
poetry shell
python -m subspace_model
```

### Usage
Inside of the `subspace/` package directory and inside of your python virtual environment.

**Run tests:** 
```bash
pytest
```

**Running a the standard simulation:**  
```bash
python -m subspace_model -p
```

**Generating a PSuU Dataset:**  
```bash
python -m subspace_model -e psuu -s 2 -sw 2 
```

**Get Help on Available Options:**  
```bash
python -m subspace_model -h
```

**Analyzing Data in Jupyter:**  
```bash
jupyter lab
```

## Table of Contents
1. [Quick Start Guide](#quick-start-guide)
2. [Table of Contents](#table-of-contents)
3. [Introduction](#introduction)
4. [Background](#background)
5. [Methodology](#methodology)
6. [Analysis](#analysis-results)
7. [Advanced Usage](#advanced-usage)
8. [Additional Resources](#additional-resources)

## Introduction

### The Subspace Economic Model

The Subspace Economic Model is a Digital Twin Stock & Flow representation for the SSC token dynamics as they flow through Subspace's distinct mechanisms. The parameters, mechanisms and their constituent logic are based on The Subnomicon and Token Economics design documents provided by the Subspace Team. 

Balances on the system are split across economic sectors of interest, each one with distinct admissible actions: 
- Farmers
- Operators 
- Nominators
- Holders

The digital twin is implemented as a python software package that enables data
generation and analysis using cadcad and other python libraries. Model
construction and data generation are performed using cadCAD. Research analysis
is performed using python data analysis pipelines and machine learning for the
purpose of selecting configuration parameters that increase the likelihood of
achieving desired goals.

### Structure of the Model

The Subspace Network's economic model is built using cadCAD and is composed of the
following python modules:

| Python Module | Purpose |
|:--------|:--------|
|  [types.py](subspace_model/types.py)  |  Type definitions for the model state and parameters.  |
|  [const.py](subspace_model/const.py)  |  System constants  |
|  [params.py](subspace_model/params.py)  |  System parameters, environmental parameter, and governance surface.  |
|  [params.py](subspace_model/state.py)  |  System inital state.  |
|  [logic.py](subspace_model/logic.py)  |  Policy and state update logic. |
|  [structure.py](subspace_model/structure.py)  |  The block update structure of the model.  |


## Background

### Economic Modeling with cadCAD

Complex Adaptive Dynamics Computer-Aided Design (cadCAD) is a python based
modeling framework for modeling, simulation, and validation of complex systems
designs.

Given a model of a complex system, cadCAD can simulate the impact that a set of
actions might have on it. This helps users make informed, rigorously tested
decisions on how best to modify or interact with the system in order to achieve
their goals. cadCAD supports different system modeling approaches and can be
easily integrated with common empirical data science workflows. Monte Carlo
methods, A/B testing, and parameter sweeping features are natively supported.

For more information on cadCAD:

- https://community.cadcad.org/t/introduction-to-cadcad/15
- https://community.cadcad.org/t/putting-cadcad-in-context/19
- https://github.com/cadCAD-org/demos

### Subspace

Subspace is the first layer-one blockchain that can fully resolve the
blockchain trilemma. Subspace is built from first principles to
simultaneously achieve scalability, security and decentralization. At its core,
Subspace introduces a novel storage-based consensus protocol that separates
consensus from execution. This proposer-builder separation allows Subspace to
independently scale transaction throughput and storage requirements while
maintaining a fully decentralized blockchain. 

-[Subspace Subnomicon](https://subnomicon.subspace.network/docs/intro)

### Aligning Incentives for Optimal Scalability

Subspace includes a novel algorithm to dynamically adjust the cost of
blockspace in response to changes in supply and demand to economically secure
the network in an open environment. Such adjustment naturally keeps the network
incentive compatible for farmers, providing storage and data availability
bandwidth and for operators providing raw compute power.

Subspace creates the world's first two-sided marketplace for blockspace,
allowing it to have a dynamic on-chain cost-of-blockspace and a stable
off-chain price-of-blockspace without relying on centralized control or
coordination. On one side are the farmers, who collectively supply blockspace
bandwidth through their storage of the blockchain history. On the other side
are dApp developers and users, who demand blockspace to deploy and run their
applications. Subspace's marketplace algorithm adjusts the on-chain
cost-of-blockspace paid out to farmers based on real-time supply and demand.
When demand is high, the cost rises to incentivize more farmers to join. When
demand is low, the cost falls to disincentivize over-investment in storage.
This dynamic adjustment process occurs transparently on-chain through the
protocol rules.

When combined with existing scalability frameworks, Subspace can achieve linear
scaling of the blockspace as more nodes join the network without sacrificing
security or decentralization.

-[Subspace Subnomicon](https://subnomicon.subspace.network/docs/advancements#aligning-incentives-for-optimal-scalability)


### Terminology
- **Fees**: The payments for transactions on the network.
- **Rewards**: The compensation for the work performed by the participants of the network via the issuance of the newly minted tokens by the protocol.
- **Issuance:** The amount of tokens minted as a Reward per block, total for all recipients.
- **Proposer:** Farmer who won the block solution challenge.
- **Voter**: Farmer who won the vote solution challenge. The current ratio is, on average, 9 votes per block.

For additional terminology, please refer to the [terminology section of the subnomicon](https://subnomicon.subspace.network/docs/terminology/).

### Recommended Readings from the Subnomicon
- [Architecture Overview](https://subnomicon.subspace.network/docs/overview)
- [Advancing Blockchain](https://subnomicon.subspace.network/docs/advancements)
- [Consensus](https://subnomicon.subspace.network/docs/category/consensus)
- [Network Architecture](https://subnomicon.subspace.network/docs/category/network-architecture)
- [Decoupled Execution](https://subnomicon.subspace.network/docs/category/decoupled-execution)
- [Staking](https://subnomicon.subspace.network/docs/decex/staking)
- [Rewards and Fees](https://subnomicon.subspace.network/docs/rewards_fees)


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
2. **Community Incentivization:** Creating incentives that encourage participation from all defined stakeholders (farmers, operators, nominators).
3. **Supply and Demand Equilibrium / Distributional Equilibrium:** Balancing the issuance and distribution of tokens to support both the network's scalability and the fair distribution of resources among participants.

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


### Environmental Scenarios


The following behavioral inputs are modulated per run according to the defined environmental scenarios:
1. **Utilization Ratio**
2. **Operator Stake per Transaction**
3. **Nominator Stake per Transaction**
4. **Transfers from Operators to Farmers per Day**
5. **Transfers from Farmers to Nominators per Day**
6. **Transfers from Farmers to Operators per Day**


The four types of environmental scenarios include the following:
1. **Standard Run:** Value is sampled from a normal distribution with low coefficient of variation
2. **Volatile Run:** Value is sampled from a normal distribution with high coefficient of variation
3. **Standard Run with Instantaneous Shocks:** Value is sampled from a normal distribution with low coefficient of variation, with periodic instances of high variation.
4. **Standard Run with Sustained Shocks:** Value is sampled from a normal distribution with low coefficient of variation, with periodic durations of high variation.



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


### Machine Learning Analysis

**Utility Maximizing Decision Trees:**  
    - Decision trees are applied to the Utility Tensor to illustrate the importance of parameter selection values on utility criteria outcomes.

**Regressing Analysis of Parameter Impact on Goals:**  
    - Density plots and linear regression are used to indicate the effects of parameter selection on utility outcomes.


### Further Reading on Methodology
- [Subspace PSuU Methodology Document](https://hackmd.io/@blockscience/r1dHBNwC6?type=view)
- [Block Science Publication on PSuU Methodology](https://medium.com/block-science/how-to-perform-parameter-selection-under-uncertainty-976931ba7e5d)


## Analysis Results
- Sanity Check Run
- PSuU Analysis
- PSuU Single Run Analysis


## Advanced Usage
- Modifying Default State
- Modifying Default Parameters
- Modifying Controllable Parameters
- Modifying Environmental Scenarios

## Additional Resources

