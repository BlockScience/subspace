# Component-based Piece-Wise Exponential Subsidies 

*BlockScience, December 21, 2023. Updated at 11 January 2024*

## Executive Summary

- We propose continuing using the [Hyperbolic Dynamic Issuance as described in the Issuance Mechanism Proposal](/GUzjDVm0TW2CulWAbetBWA), but with the following modifications:
    - The terminology on "costs" is replaced towards "reference subsidies" by setting $C(t)=S_r(t)$, where $S_r$ is the Reference Subsidy at time $t$
- The Reference Subsidy ($S_r$) is to be defined as a summation over piece-wise functions (or subsidy components). Each Subsidy Component has two terms: one which involves assigning a constant Reference Subsidy over a fixed period, and a second on which Reference Subsidy becomes halving.
    - The free parameters for each component are: **1)** The Maximum Possible Cumulative Subsidy ($\Omega_i$) that can be disbursed through this component (distinct from actual); **2)** The Maximum Reference Subsidy ($\alpha_i$) at the beginning of the component life; **3)** The initial period duration ($[\tau_{0, i},\tau_{1, i}]$).
    - More specifically, the reference subsidy is defined as $S_r(t):=\sum s_i$, where $s_i$ are the subsidy components, which are defined as being $s_i=\alpha_i \forall t \in [\tau_{0, i},\tau_{1, i}]$ and $s_i=\alpha_i e^{-\frac{\alpha_i}{K_i}(t-\tau_{1, i})} \forall t > \tau_{1,i}$
    - The halving period for each components depends directly on the choice of parameters being made. All things being equal, larger initial periods tends to imply smaller halving periods. Larger maximum cumulative subsidies imply larger halving periods, and so on.
    - **A key advantage of this approach is enabling additive modifications to the issuance through an additive procedure** (eg. by appending new components that have a fixed budget) rather by modifying or removing pieces. This can be particularly relevant for after-launch governance processes.
- By taking those together, the Issuance Function becomes:
    - $s(g) := a + b \tanh(-c(g - d)), s \in \mathbb{R}_+$ where:
        - $a=C_0-b \tanh (cd)$
        - $b=\frac{S_r(t) - (S_r(t) - \bar{F}(t))^+}{\tanh{c}}$
        - $c=\text{Fixed parameter, to be tuned}$
        - $d=1$
        - $g=\text{Utilization Ratio}(t)$

## Overview

We propose using a component based approach on which the Reference Subsidy is defined by the summation over multiple components. Each component has two terms: the first one defines a initial period on which the reference subsidy remains constant, and the second term consists of a halving term on which the subsidy decays exponentially. 

Specifying each individual component requires defining the maximum subsidy that can be disbursed initially, the duration of the initial period and the maximum cumulative subsidy that can be disbursed through the network lifetime. The halving period is an metric that can be computed against those choices of parameters.

This approach has several advantages, which includes: **1)** They're bounded in maximum cumulative subsidies, which provides a safety factor and can be proven to be less than the total Maximum Supply for Rewards; **2)** Because they're piece-wise, the reward issuance behavior can be governed through component additions rather than modification, which tends to be less complex governance-wise, therefore stimulating the community engagement on the protocol steering. **3)** They express a convenient form to express distinct types of issuance-based disbursals in the token economy if the situation demands it. Each component can be configured to be either a) a pure halving function, b) a fixed period on which subsidies are relatively constant, c) a in-between where the initial period avoids over-centralizing rewards on the earliest farmers.


---
*Reference Subsidy per Block for a single component under a stylized choice of parameters. [Source](https://www.desmos.com/calculator/tgdkgx3gdh)* 
![desmos-graph-2](https://hackmd.io/_uploads/Bk2-UpePT.png#center =400x400)

---
*Reference Subsidy per Block for two under a stylized choice of parameters. Black dots indicates Reference Subsidy while red/green bands are the individual components. [Source](https://www.desmos.com/calculator/rgb6hx59l0)*
![desmos-graph-3](https://hackmd.io/_uploads/ByGl26gPT.png#center =400x400)

---

## Requirements & Considerations

- C1: Farmer data is off-chain. At most we can measure aggregate variables or do assumptions.
- R1: The subsidy goal is to incentivize bootstrapping. It should not replace or substitute the market forces
- D1: Avoiding Monopolies / centralization over recipients
- D2: Incentivizing community engagement 

## Specification

$$S_r(t) = \sum_i s_i(t)$$

$s_i(t)=\alpha_i          if \tau_{0,i}<t<\tau_{1,i}$

$$s_i(t)=\alpha_i*e^{-\frac{\alpha_i}{K_i}(t-\tau_{1, i})}\tau_{1,i}<t$$

$$\Omega_i = K_i + \alpha_i \cdot \Delta \tau_i$$

$$\lambda_i = \frac{K_i \log{2}}{\alpha_i}$$

$$\sum_i \Omega_i < \text{TotalRewardSupply}{}$$

On which the terms are described as being:
- $S_r(t)$ is the Reference Subsidy at time $t$ 
- $s_i$ is the i-th component of the Reference Subsidy which is parametrized by 
    - $\alpha_i$: The maximum subsidy per block to be disbursed during the initial period. 
        - Unit: SSC/block
    - $\Omega_i$: The maximum subsidy that can be disbursed through the component lifetime
        - Unit: SSC
    - $\tau_{0, i}$: The beginning of the constant disbursal period
        - Unit: Blocks
    - $\tau_{1, i}$: The beginning of the exponential disbursal period
        - Unit: Blocks
- Additionally, $s_i$ have the following auxiliary variables:
    - $K_i$: The maximum subsidy that can be disbursed during the exponential period
    - $\lambda_i$: The halving period for the subsidy component
    - $\Delta \tau_i=\tau_{1, i} - \tau{0, i}$: The duration of the initial period in blocks

