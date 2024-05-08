# The Subspace Network Economic Digital Twin 

A cadCAD Design Digital Twin for Subspace Network Economic Dynamics.

![](resources/ssc-stock-flow.png)
*A stock and flow description for SSC on the tokenomics of Subspace. This model uses this as the departure point for the dynamics being simulated.*

## Table of Contents
- Introduction

    - Subspace
Subspace is the first layer-one blockchain that can fully resolve the
blockchain trilemma. Subspace is built from first principles to
simultaneously achieve scalability, security and decentralization. At its core,
Subspace introduces a novel storage-based consensus protocol that separates
consensus from execution. This proposer-builder separation allows Subspace to
independently scale transaction throughput and storage requirements while
maintaining a fully decentralized blockchain. -Subspace Subnomicon

    - Decoupled Consensus
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
higher throughput, lower costs, and improved scalability. -Subspace Subnomicon

    - Aligning Incentives for Optimal Scalability

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

    - Relevant Terminology

        - Subspace Network
Typically means a combination of Subspace consensus chain, domain chains and Distributed Storage Network as a whole system.

        - Blockchain History
An ordered collection of blocks of the blockchain, specifically in Subspace, means SCALE-encoded blocks of the blockchain.

        - Blockchain State
The result of executing transactions on a blockchain (like state of account balances, smart contracts, etc.)

        - Dilithium
The Subspace Network Proof-of-Archival-Storage consensus mechanism which defines Archiving, Plotting, Farming, Proving and Verification.

        - ...

- Background
    - Subspace Resources
    - cadCAD Resources
- Installation
    - Option 1: Using `venv` virtual environment
    - Option 2: Using python poetry
- Usage
    - Running Tests
    - Running a Simulation
    - Generating a PSuU Dataset
- Advanced Usage
    - Modifying Default State
    - Modifying Default Parameter
    - Modifying Controllable Parameter Sweeps
    - Modifying Environmental Scenario Sweeps
    - Defining Custom Experiments
- Model Implementation
    - File Structure
    - Model Structure
    - State Update Logic
    - Subspace Mechanism Components
    - Functional Parameters
- Research Analysis
    - Sanity Check Run
    - PSuU Analysis
    - PSuU Single Run Analysis

## Notes on modelling

This Digital Twin is a Stock & Flow representation for the SSC token dynamics as they
flow through Subspace's distinct mechanisms. Balances on the system are split
across economic sectors of interest: Farmers, Operators, Nominators and Holders,
each one with distinct admissible actions.

The parameters, mechanisms and their constituint logic were based mainly on 
Subnomicon and Token Economics design documents that were provided. Several
assumptions were required to be done, and they're indicated with `XXX` tags
through this repo.

## How to run it

- Option 1 (CLI): Just pass `python -m subspace_model`
This will generate an pickled file at `data/simulations/` using the default single run
system parameters & initial state.
    - To perform a multiple run, pass `python -m subspace_model -e`
- Option 2 (cadCAD-tools easy run method): Import the objects at `subspace_model/__init__.py`
and use them as arguments to the `cadCAD.tools.execution.easy_run` method. Refer to `subspace_model/__main__.py` to an example.

## File structure

```
├── notebooks
│   ├── fund_inclusion.ipynb
│   ├── issuance_sweep.ipynb
│   ├── reward_split_sweep.ipynb
│   ├── sanity_check.ipynb
│   └── standard_stochastic.ipynb
├── README.md
├── requirements.txt
├── resources
│   ├── shares-stock-flow.png
│   └── ssc-stock-flow.png
└── subspace_model
    ├── __init__.py
    ├── __main__.py
│   ├── experiment.py
│   ├── logic.py
│   ├── params.py
│   ├── structure.py 
│   └── types.py
    ├── const.py
    ├── metrics.py
    ├── trajectory_metrics.py 
```

Digital twin python modules.
    
| Python Module | Purpose |
|:--------|:--------|
|  [experiment.py](subspace_model/experiment.py)  |  Code for running experiments, parameter sweeps, and scenario planning.  |
|  [logic.py](subspace_model/logic.py)  |  All logic for substeps of blocks. Informs how state is mutated.  |
|  [params.py](subspace_model/params.py)  |  System parameters, initial state, and standard parameters.  |
|  [structure.py](subspace_model/structure.py)  |  The model structure as a netlist that wires state update blocks.  |
|  [types.py](subspace_model/types.py)  |  Type definitions for the model state and parameters.  |
|  [const.py](subspace_model/const.py)  |  System constants  |
|  [metrics.py](subspace_model/metrics.py)  |  System metrics  |
|  [trajectory_metrics.py](subspace_model/trajectory_metrics.py)  |  Metrics that require trajectory dataset.  |


## What is cadCAD
cadCAD (complex adaptive dynamics Computer-Aided Design) is a python based modeling framework for research, validation, and Computer Aided Design of complex systems. Given a model of a complex system, cadCAD can simulate the impact that a set of actions might have on it. This helps users make informed, rigorously tested decisions on how best to modify or interact with the system in order to achieve their goals. cadCAD supports different system modeling approaches and can be easily integrated with common empirical data science workflows. Monte Carlo methods, A/B testing and parameter sweeping features are natively supported and optimized for.

For more information on cadCAD:

* https://community.cadcad.org/t/introduction-to-cadcad/15
* https://community.cadcad.org/t/putting-cadcad-in-context/19
* https://github.com/cadCAD-org/demos


## Installing cadCAD for running this repo

### 1. Pre-installation Virtual Environments with [`venv`](https://docs.python.org/3/library/venv.html) (Optional):
It's a good package managing practice to create an easy to use virtual environment to install cadCAD. You can use the built in `venv` package.

***Create** a virtual environment:*
```bash
$ python3 -m venv ~/cadcad
```

***Activate** an existing virtual environment:*
```bash
$ source ~/cadcad/bin/activate
(cadcad) $
```

***To Deactivate** virtual environment:*
```bash
(cadcad) $ deactivate
$
```

### 2. Installation: 
Requires [>= Python 3.6](https://www.python.org/downloads/) 

**Install all packages with requirement.txt**
```bash
$ pip3 install -r requirements.txt
