# Decoupled Issuance

![Screenshot 2024-01-18 at 17.45.56](https://hackmd.io/_uploads/SkNXC-vY6.png)
[Interactive visualization for the Hybrid Decoupled Issuance](https://www.desmos.com/calculator/h1idbmxlpj). Red and Blue line indicates the rewards for Proposers and Voters respectively, while Red Dashed indicates the Proposers Revenue (Reward + Storage Fees) 


## Summary

On this document, we propose the notion of a Vectorial Issuance Function, which enables to decouple issuance across different classes of recipients, which has the advantage of allowing the expression of per-subpopulation rewards. In particular, this allows for different subsidy forms to be defined for the Voters and the Data Blocks.

## Introduction

On the [Dynamic Issuance Functional Form](/GUzjDVm0TW2CulWAbetBWA) document, a scalar Block Reward function $B(t)$ was proposed on which its value [Stock & Flow Description for the Subspace Network Tokeconomics](/iFjTBsS3Qj6HlB0fLIWF5A) denotes the inflow from the Protocol Issuance stock towards the Farmers ($\hat{f}$) population. This inflow is then split between three Farmer subpopulations: Block Proposers ($\hat{p}$), Block Voters ($\hat{v}$) and Data Blocks ($\hat{d}$). Effectively, this means that the causal relationship is that the protocol does issue rewards, which is then split and disbursed to the fractional recipients.

On this document, we propose to reduce the intermediary steps above by making the protocol issuing directly the fractional rewards. This is made by defining a Vectorial Issuance Function rather than a Scalar one. The new function is a strict superset of the old one and has the advantages of increasing the clarity and the governance surface of the issuance mechanism. We name this capacity of being multi-dimensional with issuance as "Decoupled Issuance".

## Decoupled Issuance

### Defining the Vectorial Issuance Function function

The Vectorial Issuance Function is defined by $\vec{\pi}(t)$, where $\pi_p$, $\pi_v$ and $\pi_p$ are the issuance components for the proposers, voters and data blocks respectively.

$$\vec{\pi}(t) = \pi_p(t) \hat{p} + \pi_v(t) \hat{v} + \pi_d(t) \hat{d}$$

For sake of comparison, the Scalar Issuance Function can be described through the following equation. The main difference is that the reward is issued for the general farmer population ($\hat{f}$) which is then to be split.

$$\vec{\pi}(t) = \pi(t) \hat{f}$$ 

where $\pi(t) = \pi_p(t) + \pi_v(t) + \pi_d(t)$

### Example 1: Fitting the Dynamic Issuance definition on Decoupled Issuance

Given that the Vectorial Issuance Function is a superset of the previous scalar block reward function, we're able to express the current issuance definition as being:

$$\begin{align}
\vec{\pi}(t) &= B(t) \cdot(f_p \hat{p}+ f_v \hat{v} + f_d\hat{d}) \\
\\
B(t) &= a+b \tanh{-c (g(t)-d)}
\end{align}$$

Or alternatively, we could use the Vectorial Issuance Function definition and use the following components:

$$\begin{align}
\pi_p(t) &=f_p B(t) \\
\pi_v(t) &= f_v B(t) \\
\pi_d(t) &= f_d B(t) \\
\end{align}$$

### Example 2: Decoupling Dynamic Issuance from Voters and Data Blocks

In order to highlight how Decouple Issuance can be of benefit, we propose on this sub-section a alternate version for the issuance (vectorial) function, on which the Proposers will be subsidied through the [Dynamic Issuance Functional Form](/GUzjDVm0TW2CulWAbetBWA) and the Voters and Data Blocks will be subsidied through a independent implementations of the [Component-based Halving Subsidies ](/zu1jRV27SBy_HjPp_vKpYg)

$$\begin{align}
\vec{\pi}(t) &= \pi_p(t) \hat{p} + \pi_v(t) \hat{v} + \pi_d(t) \hat{d} \\
\\
\pi_p(t) &= a+b \tanh{-c (g(t)-d)} & \text{(Hyperbolic Dynamic Issuance)} \\
\pi_v(t) &= C_v(t) & \text{(Voter Component-based Subsidy)} \\
\pi_d(t) &= C_d(t) & \text{(Data Block Component-based Subsidy)}  \\
\end{align}$$

Where:

$$
\begin{align}
a&=C_p(t)-b\tanh{(c\cdot d)} \\
b&=\frac{C_p(t) - (C_p(t) - \bar{F}(t))^+}{\tanh{c}}
\end{align}
$$

and both $C_p$, $C_v$ and $C_d$ are defined as per the [Component-based Halving Subsidies](/zu1jRV27SBy_HjPp_vKpYg):

$$
\begin{align}
C_j(t)=\sum_i \alpha_{i,j} (1 \cdot [\tau_{0, i,j} < t \lt \tau_{1, i,j}]+ e^{-\frac{\alpha_{i,j}}{K_{i,j}}(t-\tau_{1, i,j})} \cdot [\tau_{1, i,j} < t])
\end{align}
$$

Given that Voters and Data Blocks have different incentive requirements than Proposers, this approach has the potential for allowing a large degree of customization. It is also possible to mix-and-match this form with the previous one, so that Voters and Data Blocks still receive a fraction of the Dynamic Issuance plus they do receive some independent issued terms. 

### Example 3: Hybrid Decoupled Issuance

On this approach, we add independent terms for the Voters and Data Blocks to the Current Block Reward vectorial formalism. This will give us:

$$\begin{align}
\vec{\pi}(t) &= \pi_p(t) \hat{p} + \pi_v(t) \hat{v} + \pi_d(t) \hat{d} \\
\\
\pi_p(t) &= f_p B(t) \\
\pi_v(t) &= f_v B(t) + C_v(t) \\
\pi_d(t) &= f_d B(t) + C_d(t) \\
\end{align}$$

Where $C_v$ and $C_d$ is defined on the previous section, and $B(t)$ is the usual Hyperbolic Dynamic Issuance + Reference Subsidy function.

$$
\begin{align}
B(t) &= a+b \tanh{-c (g(t)-d)} & \text{(Block Reward through Hyperbolic Dynamic Issuance)} \\
a&=C_0(t)-b\tanh{(c\cdot d)} & \text{(Offset Parameter)}  \\
b&=\frac{C_0(t) - (C_0(t) - \bar{F}(t))^+}{\tanh{c}} & \text{(Linear Sensitivity Parameter)} 
\end{align}
$$

### Example 4: Adding Voter Rewards on top of Dynamic Issuance

On this form, we adopt a similar shape to Example 2, but with the variation that we denominate the extra term for voters as being the "Vote Rewards", which is given by $V(t)$. We also make $V(t)$ being dependent on the ratio between amount of votes per block ($n_{\text{votes}}(t)$) and expected vote count ($\langle n_{\text{votes}}\rangle$) so that the rewards per voter don't change when having extra or less voters on a given block. 


$$\begin{align}
\vec{\pi}(t) &= \pi_p(t) \hat{p} + \pi_v(t) \hat{v} + \pi_d(t) \hat{d} \\
\\
\pi_p(t) &= f_p B(t) & \text{(Proposer Issuance)} \\
\pi_v(t) &= f_v B(t) + V(t) & \text{(Voter Issuance)} \\
\pi_d(t) &= f_d B(t) & \text{(Data Blocks Issuance)} \\
\\
V(t)&=\frac{n_\text{voters}(t)}{\langle n_\text{voters} \rangle} C_v(t) & \text{(Vote Rewards)} \\
\end{align}$$

---

By summing the components, it is possible to extract metrics like how much rewards are going to be issued per block, and what is going to be the Issued Rewards Fraction per category (as opposed to Block Rewards Fraction). This is given by:

$$
\begin{align}
\pi(t) &= B(t) + V(t)  & \text{(Issued Rewards per Block)} \\
\tilde f_p(t) &= \frac{\pi_p(t)}{\pi(t)} = \frac{f_p}{1+k} & \text{(Proposers' Issued Rewards Fraction)}\\
\tilde f_v(t) &= \frac{\pi_v(t)}{\pi(t)} = f_v  & \text{(Voters' Issued Rewards Fraction)} \\
\tilde f_d(t) &= \frac{\pi_d(t)}{\pi(t)} = \frac{f_d}{1+k}  & \text{(Data Blocks' Issued Rewards Fraction)} \\
\\
\tilde f_p(t) &+ \tilde f_v(t) + \tilde f_d(t) = 1 & \text{(Issued Rewards Fraction must sum to 100%)} \\
\end{align}
$$

---

One limitation of using the Expected Vote Count as the denominator on the Vote Rewards is that there's no hard guarantee that the *Actual Cummulative Subsidy towards Voters* will be below the *Expected Cummulative Subsidy towards Voters* at all times.

### Example 5: Equitable Rewards with Bonus for Proposers.

On this example, we assume that all recipients are entitled to the same individual amount of rewards ($\pi_n$), just like the voters on Example 4 in regards to the Vote Rewards and the proposers will receive a bonus per non-proposer recipient (which is defined as $\alpha \pi_n$) so that they're incentivized to include as many recipients as possible. Lastly, the rewards are to be set up such that the sum over all recipients rewards will converge to the Block Reward function ($B(t)$). We can implement those properties through the following formalism, where $\alpha$, $\langle n \rangle$ and $\langle n_p \rangle$ are parameters to be set:

$$\begin{align}
\vec{\pi}(t) &= \pi_p(t) \hat{p} + \pi_v(t) \hat{v} + \pi_d(t) \hat{d} \\
\\
\\
\langle n \rangle &= \langle n_p + n_v + n_d \rangle & \text{Expected Count of Recipients} \\
\pi &= n \pi_n + \alpha \pi_n (n - n_p) & \text{Sum of Issuance across recipients} \\
\langle \pi \rangle &= B(t) & \text{Expected Issuance converges to the Reward function} \\
\pi_n &= \frac{B}{\langle n \rangle (1 + \alpha) - \alpha \langle n_p \rangle} & \text{Per Recipient Reward}\\
\\
\\
\pi_p(t) &= n_p \pi_n + \alpha \pi_n (n - n_p) & \text{Proposer Issuance} \\
\pi_v(t) &= n_v \pi_n  & \text{Voter Issuance} \\
\pi_d(t) &= n_d \pi_n & \text{Data Blocks Issuance} \\
\\
\end{align}$$

A demonstration of the above mechanism can be visualized in the below spreadsheet.

*Fig. Demonstration of Example 5 across different choices of $\alpha$ and varying number of voters. [link](https://docs.google.com/spreadsheets/d/16wk08-pGvU-9Yao-BaO2eYgg6WBT2ggaqQBIsh9KN2w/edit?usp=sharing)*
![Screenshot 2024-02-15 at 17.03.50](https://hackmd.io/_uploads/SJj4RyhoT.png)

