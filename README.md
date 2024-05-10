# The Subspace Network Economic Digital Twin 

A cadCAD Design Digital Twin for Subspace Network Economic Dynamics.

![](resources/ssc-stock-flow.png)
*A stock and flow description for SSC on the tokenomics of Subspace. This model uses this as the departure point for the dynamics being simulated.*

## Quick Start Guide
Requires:
- [>= Python 3.6](https://www.python.org/downloads/) 
- One of [`venv`](https://docs.python.org/3/library/venv.html) or [`poetry`](https://python-poetry.org/) for python virtual environment.

First clone the repository.
```bash
git clone https://github.com/blockscience/subspace && cd subspace
```

Option 1: Using `venv` virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m subspace_model
```
Option 2: Using python poetry
```bash
poetry install
poetry shell
python -m subspace_model
```

## Table of Contents
- Quick Start Guide
- Introduction
    - The Subspace Network Economic Model
- Background
    - Subspace
    - Decoupled Consensus
    - Aligning Incentives for Optimal Scalability
    - Terminology
    - Economic Modeling with cadCAD
- Methodology
    - Structure of the Model
    - Assumptions of the Model
    - Goals of the System
    - Key Performance Indicators
    - Controllable Parameters
    - Environmental Scenarios
    - Further Reading on Methodology
- Usage
    - Running Tests
    - Running a Simulation
    - Generating a PSuU Dataset
- Advanced Usage
    - Modifying Default State
    - Modifying Default Parameters
    - Modifying Controllable Parameters
    - Modifying Environmental Scenarios
- Research Analysis
    - Sanity Check Run
    - PSuU Analysis
    - PSuU Single Run Analysis
- Additional Resources

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

## Background

### Subspace

Subspace is the first layer-one blockchain that can fully resolve the
blockchain trilemma. Subspace is built from first principles to
simultaneously achieve scalability, security and decentralization. At its core,
Subspace introduces a novel storage-based consensus protocol that separates
consensus from execution. This proposer-builder separation allows Subspace to
independently scale transaction throughput and storage requirements while
maintaining a fully decentralized blockchain. 

-[Subspace Subnomicon](https://subnomicon.subspace.network)

### Decoupled Consensus

The Subspace Network decouples consensus from computation by separating
transaction execution into independent domains. Domains are responsible for
executing transactions and smart contract calls. When a user sends a
transaction, this layer processes it and updates the domain app-chain state
accordingly. Decoupling execution from consensus allows for scalability
improvements. It means that execution can be parallelized, optimized, or even
sharded independently of the consensus process.

Domains are run by operators, who pledge their more powerful hardware and stake
to execution of the domain. They are incentivized through execution fees
(similar to gas fees on Ethereum).Operators are free to choose any
infrastructure that meets performance and cost requirements to run their
domains.

Domains can support any conceivable state transition framework and are
execution environment agnostic. As the first execution domain launched with
Subspace Network, the Ethereum Virtual Machine (EVM) domain, Nova, supports
running Ethereum smart contracts and executing Ethereum transactions. Nova
allows Ethereum dApps and DeFi protocols to run on Subspace with significantly
higher throughput, lower costs, and improved scalability. 

-[Subspace Subnomicon](https://subspace.network/docs/subnomicon/)

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

### Terminology

- **Fees**: The payments for transactions on the network.
- **Rewards**: The compensation for the work performed by the participants of the network via the issuance of the newly minted tokens by the protocol.
- **Issuance:** The amount of tokens minted as a Reward per block, total for all recipients.
- **Proposer:** Farmer who won the block solution challenge.
- **Voter**: Farmer who won the vote solution challenge. The current ratio is, on average, 9 votes per block.

For additional terminology, please refer to the [terminology section of the subnomicon](https://subnomicon.subspace.network/docs/terminology/).


### Economic Modeling with cadCAD

cadCAD (complex adaptive dynamics Computer-Aided Design) is a python based modeling framework for research, validation, and Computer Aided Design of complex systems. Given a model of a complex system, cadCAD can simulate the impact that a set of actions might have on it. This helps users make informed, rigorously tested decisions on how best to modify or interact with the system in order to achieve their goals. cadCAD supports different system modeling approaches and can be easily integrated with common empirical data science workflows. Monte Carlo methods, A/B testing and parameter sweeping features are natively supported and optimized for.

For more information on cadCAD:

- https://community.cadcad.org/t/introduction-to-cadcad/15
- https://community.cadcad.org/t/putting-cadcad-in-context/19
- https://github.com/cadCAD-org/demos



## Methodology

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

For more information on parameter selection under uncertainty see:
* Subspace PSuU Methodology document.
* Block Science Publication on PSuU: https://medium.com/block-science/how-to-perform-parameter-selection-under-uncertainty-976931ba7e5d


### Environmental Scenarios

The model is ran through monte carlo simulations that test four types of
scenarios for each behavioral input that is stochastically generated. 

The four scenarios include the following:
1. **Standard Run:** Value is sampled from a normal distribution with low coefficient of variation
2. **Volatile Run:** Value is sampled from a normal distribution with high coefficient of variation
3. **Standard Run with Instantaneous Shocks:** Value is sampled from a normal distribution with low coefficient of variation, with periodic instances of high variation.
4. **Standard Run with Sustained Shocks:** Value is sampled from a normal distribution with low coefficient of variation, with periodic durations of high variation.

The behavioral inputs modulated are the following:
1. **Utilization Ratio**
2. **Operator Stake per Transaction**
3. **Nominator Stake per Transaction**
4. **Transfers from Operators to Farmers per Day**
5. **Transfers from Farmers to Nominators per Day**
6. **Transfers from Farmers to Operators per Day**


### Further Reading on Methodology
- [Subspace PSuU Methodology Document](https://hackmd.io/@blockscience/r1dHBNwC6?type=view)
- [Block Science Publication on PSuU Methodology](https://medium.com/block-science/how-to-perform-parameter-selection-under-uncertainty-976931ba7e5d)


## Usage


