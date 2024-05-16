# Economic Design Report: Subspace Issuance Function
*BlockScience, November 25, 2023. Updated at 27 Februar, 2024*

--- 
## Intro
**Summary**
This document summarizes the economic mechanism design work towards a proposal for the Issuance Function, a core economic mechanism present in the Subspace protocol.

**Project Goal**
BlockScience's main goal related to the Subspace Issuance Function is to:

*Produce a recommendation for the **functional form** of a mechanism that satisfies the requirements and desirables related to token issuance in the Subspace protocol*



## Summary of proposals and supporting documents

* **Problem statement: [Issuance Function design elements](https://hackmd.io/@blockscience/rJDEKiQBa)** (Nov 25th)
This initial formulation of the problem statement summarized function properties (requirements and desirables) and proposed three basic functional forms that may be fesible, given available state information (data from the protocol).

* **Proposal: [Subspace Dynamic Issuance Function](https://hackmd.io/GUzjDVm0TW2CulWAbetBWA?view)** (Dec 7th)
This proposal describes a functional form that is dynamic with respect to block utilization while considering constraints set in the original problem statement.

    > We propose a block reward function (*"hyperbolic issuance"*) of the form $s(g(t)) := a + b \tanh(-c(g(t) - d))$

    This proposal raised further questions related to farmer costs and how to ensure sufficient incentive (reward) at all levels of block utilization.

    This also sparked an economic design thread around the definition of Credit Supply, from which a [taxonomy of Credit Supply definitions](https://hackmd.io/@blockscience/SJrmGneDT) was developed to support the decision-making process.

* **Proposal: [Component-based piecewise exponential subsidies](https://hackmd.io/zu1jRV27SBy_HjPp_vKpYg?view)** (Dec 23rd)
This proposal was a modification of the original dynamic issuance function where terminology related to "costs" was replaced towards "reference subsidies". A key advantage noted for this proposal was that it enabled modifications to the issuance by adding or removing piecewise components.

    > The Reference Subsidy ($S_r$) is to be defined as a summation over piece-wise functions (or subsidy components). Each Subsidy Component has two terms: one which involves assigning a constant Reference Subsidy over a fixed period, and a second on which Reference Subsidy becomes halving.
> $$S_r(t) = \sum_i s_i(t)$$
> $$s_i(t) = \alpha_i \text{if }{}  \tau_{0, i}<t<\tau_{1, i}$$
> $$s_i(t) = \alpha_i e^{-\frac{\alpha_i}{K_i}(t-\tau_{1, i})} \text{if }{}\tau_{1, i}<t$$
> 
> $$\Omega_i = K_i + \alpha_i \cdot \Delta \tau_i$$
> $$\lambda_i = \frac{K_i \log{2}}{\alpha_i}$$
> 
> $$\sum_i \Omega_i < \text{   TotalRewardSupply}{}$$

    Following this proposal, an additional question was raised to clarify how the current functional form incentivizes/rewards voters (an original design requirement).

* **Final proposal: [Decoupled Issuance](https://hackmd.io/@blockscience/SkEPigvFa)** (Jan 18th)
This document proposes the notion of a Vectorial Issuance Function, which enables to decouple issuance across different classes of recipients. The 3 different representations are intended to clarify protocol rewards from the perspective of block proposers, voters, and data blocks in order to verify that the required & desired incentives are indeed captured by the mechanism.

    >The issuance (vectorial) function, on which the Proposers will be subsidied through the [Dynamic Issuance Functional Form](/GUzjDVm0TW2CulWAbetBWA) and the Voters and Data Blocks will be subsidied through a independent implementations of the [Component-based Halving Subsidies ](/zu1jRV27SBy_HjPp_vKpYg)
    >
    >
    >
    >$$\vec{\pi}(t) = \pi_p(t) \hat{p} + \pi_v(t) \hat{v} + \pi_d(t) \hat{d}$$
    >
    >$$\pi_p(t) = f_p B(t)  \text{(Proposer Issuance)}{}$$
    >$$\pi_v(t) = f_v B(t) + V(t) \text{(Voter Issuance)}{}$$
    >$$\pi_d(t) = f_d B(t) \text{(Data Blocks Issuance)}{}$$
    >
    >$$V(t)=\frac{n_\text{voters}{}(t)}{\langle n_\text{voters}{} \rangle} C_v(t) \text{(Vote Rewards)}{}$$
    >$$B(t) = a+b \tanh{-c (g(t)-d)} \text{(Block Reward through Hyperbolic Dynamic Issuance)}{}$$
    >
    >Where:
    >$$a=C_p(t)-b\tanh{(c\cdot d)} \text{(Offset Parameter)}{}$$
    >$$b=\frac{C_p(t) - (C_p(t) - \bar{F}(t))^+}{\tanh{c}} \text{(Linear Sensitivity Parameter)}{}$$
    >
    >and:
    >* $B(t)$ is defined as the [Hyperbolic Dynamic Issuance Mechanism](https://hackmd.io/GUzjDVm0TW2CulWAbetBWA?view)
    >* both $C_p(t)$ and $C_v(t)$ are defined as per the [Component-based Halving Subsidies](/zu1jRV27SBy_HjPp_vKpYg):
    >$$C_j(t)=\sum_i \alpha_{i,j} (1 \cdot [\tau_{0, i,j} < t \lt \tau_{1, i,j}]+ e^{-\frac{\alpha_{i,j}}{K_{i,j}}(t-\tau_{1, i,j})} \cdot [\tau_{1, i,j} < t])$$

    Update: added **[Example 4: Adding Voter Rewards on top of Dynamic Issuance](https://hackmd.io/@blockscience/SkEPigvFa#Example-4-Adding-Voter-Rewards-on-top-of-Dynamic-Issuance)** (Feb 1st)
    In this example adds an extra term for voters as being the "Vote Rewards" to show that the rewards per voter don't change when having extra or less voters on a given block.

    Update: added **[Example 5: Equitable rewards with bonus for proposers](https://hackmd.io/w7mKLY7kRZ2Tm7FAaL3ibQ?both#Example-5-Equitable-Rewards-with-Bonus-for-Proposers)** (Feb 15th)
This example verifies that the current proposed functional form can also ensure that proposers will receive a bonus per non-proposer recipient (which is defined as $\alpha \pi_n$) so that they're incentivized to include as many recipients as possible.



## Next Step: Parameter Selection
Work towards the next step of parameter selection of this mechanism (and additional system parameters) is captured in the [Subspace System Parameter Selection Report](https://hackmd.io/UUqsTyzaQd2l2yANtLV3Pg?view).

Note that this document is still living - mechanism changes are possible as we learn more about the mechanism through simulations and experiments.
