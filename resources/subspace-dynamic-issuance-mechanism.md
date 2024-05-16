# Subspace Dynamic Issuance Mechanism

*BlockScience, November 30, 2023. Updated at 11 January 2024*

--- 
tags: 
#subspace 
#dynamic_issuance

![Screenshot 2024-01-11 at 13.39.55](https://hackmd.io/_uploads/SJpe596ua.png)
*Behavior of the proposed block reward function (black line) and expected profits (blue line) under a stylized scenario. [Source](https://www.desmos.com/calculator/x3h2shsuja)*


## Executive Summary

- We propose a block reward function (*"hyperbolic issuance"*) of the form $s(g(t)) := a + b \tanh(-c(g(t) - d)), s \in \mathbb{R}_+$, where the following interpretations can be made:
    - $g(t) \in [0, 1]$: The Utilization Ratio (or $g(t)=\frac{\text{BlockSize}(t)}{\text{MaxBlockSize}}$)
    - $a \in \mathbb{R}_+$: Offset Parameter. Minimum reward when $d=1$ 
    - $b \in \mathbb{R}_+$: Linear Sensitivity Parameter. Maximum reward when $a=0$ and $c \to \infty$
    - $c \in \mathbb{R}_+$: Hyperbolic Sensitivity Parameter.
    - $d \in [1, \infty]$: Saturation Velocity Parameter.
- $s(g(t))$ can be tuned by assuming a minimum and maximum reward (given by $\underline{s}, \bar{s}$). Assuming $d=1$, we have:
    - $\underline{s}=a=(\bar{C}-\bar{F})^+$
    - $\bar{s}=\underline{s} + b * \tanh{c}=C_0$
- The following issuance parameters should be decided (either statically, dynamically or through governance):
    - $\bar{s}$: Maximum Reward
    - $\underline{s}$: Minimum Reward
    - $b$: Reward Linear Sensitivity
    - $c$: Reward Hyperbolic Sensitivity
- It is possible to embed Dynamic Issuance concepts by assuming $\underline{s}=(\bar{C}-\bar{F})^+=a$ and $\bar{s}=C_0$. By taking all together, this generates the following invariant: $b \tanh{c} = C_0 - (\bar{C} - \bar{F})^+$ and $a=C_0-b \tanh(cd)$
    - Terminology: $C_0$ is the cost denominated in SSC for farmers to operate on a zero utilization rato environment. $\bar{C}$ and $\bar{F}$ are the cost and fee revenue denominated in SSC, respectively, for farmers to operate in a full utilization ratio environment
    - One approach is to decide a priori on the Hyperbolic sensitivity ($c$) and allow the Linear sensitivity ($b$) to float dynamically according to $C_0$, $\bar{C}$ and $\bar{F}$.
- Key Assumptions: 
    - There is a finite issuance lifetime (eg. by assuming maximum issuance rate, the supply will hit its maximum after an limited period).
- Things left undecided
    - How do we determine and set $C_0$?
    - How do we determine and set $\bar{C}$?
    - What should be the Hyperbolic Sensitivity?
- Possible name for the mechanism:
    - Hyperbolic Dynamical Issuance


## Requirements (from [problem statement doc](https://hackmd.io/@blockscience/rJDEKiQBa))

1. Capped Supply (cumulative issuance or circulating supply?)
2. Token supply should be at least 51% owned
  - `Available Token Supply = Vested + Issued - Burnt`
  - `Community Owned Supply = k*Vested + Issued - Burnt`
  - (System-wide vs. mechanism requirement)
3. Interpretable via a 'subsidy parameter' modifying a system characteristic, such as an output gap or storage utilization rate
  - Parameter can be static, dynamic, periodically adjusted...
4. Interpretable "target inflation rate" should be available, e.g. multiplier on block rewards
  - Parameter can be static or dynamic

## Dynamic Issuance Derivation

There is a block generation process $B_0, B_1, \ldots$, with each block having size $|B_t|$ in storage units. Associated with each block is a non-transactions-fee-based "block reward" (note that here and in what follows, 'block reward' will be used in place of the term 'subsidy' relative to earlier work) for producing a block that is distributed to a farmer who 'wins' the block proposal round. There is a maximum block size `MaxBlockSize` denoted here by $|\bar B| >0$, which is assumed to be fixed within the protocol.

**Assumption**: The block reward _is_ the issuance of the SSC token that is minted and distributed.

Define the _relative output gap_ or _utilization rate_ at time $t$ by the fraction

$$g(t) := \frac{|B_t|}{|\bar B|} \in [0,1]$$

At **full** utilization $g(t) = 1$, while $g(t) = 0$ means **no** utilization. The objective is to provide a block reward in addition to any transactions fees (here comprising both storage and compute fees) that is _higher when the utilization rate is lower_, and _lower when the utilization rate is higher_.

A very simple function that provides a block reward $s(\cdot)$ with the required properties has the general form:

$$s(g(t)) := a + b \tanh(-c(g(t) - d))$$


---

![Screenshot 2023-12-04 at 13.51.55](https://hackmd.io/_uploads/HJi6QKsHT.png)
*Visualization for $s(g)$ for a choice of parameters. [Link](https://www.desmos.com/calculator/sqxmuibgur)*

---


### Properties and Restrictions on a solution $s(\cdot))$ 

1. Consider first a zero utilization rate, $g(t) = 0$. In that case the block reward for the block at time $t$ should attain a **maximum** value $\bar s$:
$$s(0) = a + b \tanh(cd) = \bar s$$
2. Next consider a full utilization rate, $g(t) = 1$. Then the block reward for the block at time $t$ should attain a **minimum** value $\underline s$:
$$s(1) = a + b\tanh(c(d-1)) = \underline s$$
3. A simple solution (but by no means the only solution!) is to select $d = 1$ and $a = \underline s$, as then $s(1) = \underline s$, as required, while $s(0) = \bar s = \underline s + b\tanh(c)$. Thus, there are two degrees of freedom in the selection of the functional form of $s(g(t))$:
$$s(g(t)) = \underline s + b\tanh(c(1 - g(t))) \qquad \qquad (*)$$
4. Note that the magnitude of $c$ determines the range of values of the utilization rate for which the block reward is insensitive to utilization: for example, a very high value of $c$ implies that the block reward "maxes out" at $\bar s \simeq \underline s + b$ even for utilization rates significantly different from zero. By contrast, setting a low value of $c$ implies that even if utilization is very near zero, the block reward does not appreciably move from $\underline s + b\tanh(c) \simeq \underline s$. 
5. As shown in #4 above, the parameter $b$ sets the overall scale of the block reward--for non-extreme values of $c$, when the utilization rate is very low the block reward will achieve a maximum value of $\bar s = \underline s + b$.
6. This form implies that the maximum _instantaneous_ rate of issuance is

$$\frac{d s}{d t} = \frac{d s}{d g}\frac{d g}{d t} = -bc\text{sech}{}^2(c(1-g(t)))g'(t)$$

or

$$\left (e^{c(1-g(t))} + e^{-c(1-g(t))} \right )g'(t)$$

7. **Inflation**: The maximum _cumulative_ issuance over a period of time $T$ is just $T \times \bar s$, since the maximum block reward possible for any block is $\bar s$. If the supply at time $t$ is $S_t$, then the inflation rate $\pi_{t+1}$ over the following period (block) is just

$$\pi_{t+1} := \frac{s(g(t))}{S_t} < \frac{\bar s}{S_t}$$

Thus, a desired **_maximum target inflation rate_** can be specified by selecting values for $b$ and $c$ (up to their non-negativity and farmer incentivization conditions, cf. below). Note that under this specification, the maximum inflation rate goes to a minimum value $1/\bar T$ as $S_t \rightarrow \bar S$, with $\bar S$ the capped supply and $\bar T$ the ecosystem horizon (see #8).

8. **Capped Supply:** Suppose that stakeholder requirements specify a maximum supply $\bar S$ over the lifetime of token distribution for block rewards (block reward). For example, the [Subspace Issuance Model Logic document](https://www.notion.so/subspacelabs/Subspace-Issuance-Model-Logic-750054765d5e4083a0811a77b3402255?pvs=4) puts this amount at 43% of the total lifetime token supply of $3e8$ tokens, or around $1.29e8$ tokens. Then given a maximum lifetime (in number of blocks) $\bar T$, the per-block maximum block reward is just $\bar s := \bar S / \bar T$. Given that utilization will never be zero for every block, this immediately implies that actual supply distributed over the lifetime of the ecosystem will be strictly less than $\bar S$. This specification also ensures that a _declining_ issuance over time is achieved precisely when there is an _increasing block utilization_, i.e. that the ecosystem is achieving a measurable success in its use of available block storage to process transactions.


### Block Reward Distribution: Farmer Attributes

The block reward $s(g(t))$ for block $t$ is to be distributed to the farmers that are responsible for proposing block $t$.

**Assumption**: There is one and only one farmer that 'wins' the right to propose a block each period.

The block reward distributed to the farmer should incorporate attributes of both the demand for services and the cost structure of the farmer, which provides an indication of how profitable the farmer finds itself in proposing the block. The rationale is that when the farmer is operating in a negative profitability regime, the block reward should be positive, while if the farmer is operating in a positive profitability regime then the block reward should approach some minimal value (perhaps zero).

In addition, the farmer should not be incentivized to simply keep blocks empty to earn a block reward. The structure of the block reward function should thus provide an incentive for a farmer to prefer to include transactions in a block, earning the associated fees that outweigh the loss in block reward that results from a more 'full' block.

The cost of proposing a block in period $t$ containing a set $M_t$ of transactions  depends upon utilization $g(t)$, since it is assumed that cost depends directly upon the size of the block being composed (this may be relaxed for more complex cost functions, where there is also direct dependence upon the set of transactions included in the block). Denote the cost function by $C(g(t))$, where it is assumed further that $C(\cdot)$ is strictly increasing and strictly convex in its argument.

The selection of the set $M_t$ of transactions to include is up to the farmer. The farmer earns transactions fees $F(M_t)$ based upon the transactions included in the proposed block. It is assumed that, although fees are heterogeneous across transactions, all other things equal fees are increasing in the size of the proposed block. Thus, as with the cost function we assume that $F = F(g(t))$, and that $F(\cdot)$ is strictly increasing and strictly concave in its argument (representing the abstraction that it may be more difficult to increase fees when attempting to add more and more transactions to a block).

### The farmer's problem

In general, given a set of messages $\bar M_t$ available in the mempool to be included in a block at time $t$ , the farmer selects messages for incluision $M_t \subseteq \bar M_t$ each period to maximize their lifetime profits:

$$\pi = \max_{\{M_t\}_{t=0}^\infty} \mathbb{E}_0 [\sum_{t=0}^\infty \beta^t( s(g(t)) + F(g(t)) - C(g(t)))]$$

where $\beta \in (0,1)$ is the _subjective discount factor_ of the farmer, and there is a _capacity function_  $f$ such that

$$|\bar B| g(t) = |B_t| = f(M_t, |\bar B|)$$

The law of motion of transactions is:

$$\bar M_{t+1} = \bar M_t \setminus M_t + N_t$$

where $N_t$ is the set of new transactions arriving in the mempool during the time that transactions $M_t$ were included in the current block $B_t$. This simply means that the number of transactions in the mempool at the beginning of period $t+1$, $\bar M_{t+1}$, is just the residual transactions $\bar M_t \setminus M_t$ that were not selected in period $t$ along with new transactions $N_t$ that have arrived in the meantime.

We have included the general problem of the farmer above for completeness, but we will not investigate the optimal farmer decisions in what follows. Rather, we _assume_ that there is, for this system, an optimal selection of transactions for inclusion $\{M^*_t\}_{t=0}^\infty$ that the farmer has selected, conditional upon the block reward function $s(\cdot)$. In that case, the farmer's profit is given as:

$$\pi[M_0^\star, M_1^\star, \ldots] := \sum_{t=0}^\infty \beta^t\left [ p \left ( s (g(t)) + F(g(t)) \right ) - C(g(t)) \right ]$$

where $p \in (0,1]$ is the probability the farmer 'wins' the block proposal in any period (here we assume this is taken as given by the farmer). 

**The goal of the mechanism is to provide a block reward mechanism geared toward the farmer earning at least zero economic profit each period that they successfully propose a block.** Thus, it should be that

$$s (g(t)) + F(g(t)) - C(g(t)) \geq 0$$

for any actual utilization rate $g(t)$. To achieve this is to 'pin down' some of the free parameters in $s$, _without knowing the full characteristics of every farmer's cost function_ $C(\cdot)$. Thus, the above inequality will be addressed in the polar utilization cases, with the structure of $F(\cdot)$ and $C(\cdot)$ providing assurances that the inequality is (perhaps in expectation only) attained in the general utilization case.

#### Polar case functional form determination

We have at our disposal the polar cases of no and full block utilization. Consider first the polar case of no utilization, i.e. $g(t) =0$. In that case the block reward $s(0) = \bar s$, its maximum and we further suppose that no fees are earned, i.e. $F(0) = 0$. The above constraint is then

$$\bar s \geq C_0$$

where $C_0 := C(0)$ is the _fixed overhead_ a farmer must pay even when block utilization is empty. We assume that $C_0 \geq 0$, and that **there exists a statistic that the protocol can compute that represents its value** (_as we cannot tailor this value to each farmer_).

This constraint may be reduced to an equality in order to provide the lowest maximum block reward necessary, i.e. $\bar s = C_0$.

Next, consider the polar case of full utilization, $g(t) = 1$. Then the block reward is at its minimum value $s(1) := \underline s$, while $F(1) = \bar F$ and $C(1) = \bar C$ represent maximum fees earned and costs paid, respectively (again, this ignores the possibility that a block's fee is maximized while the block is underutilized, or that the cost of proposing a block is highest when it is underutilized).  **It is assumed that the protocol can infer the actual value of $\bar F$ and a statistic for $\bar C$ from other data**. The above constraint then becomes (with an equality given the reasoning above)

$$\underline s = (\bar C - \bar F)^+$$

where the notation $(\cdot)^+$ means 'the non-negative part', i.e. $\underline s = 0$ if $\bar C - \bar F \leq 0$ and $\underline s = \bar C - \bar F > 0$ otherwise.

Since we already know that $\bar s = \underline s + b\tanh(c)$, taken together these extremes reveal that

$$b \tanh(c) = C_0 - (\bar C - \bar F)^+$$

which ensures that actual farmer profit data (given by $\bar F$, $\bar C$ and $C_0$) are included in the block reward function. (If these values should be recognized to change over time, then it would be prudent to provide a governance surface that allows the value of $b$ to be updated according to the newly changed values.)

### Discussion: Economic Restrictions

##### Global incentives for participation as a farmer

Note that for the block reward to function as intended, there is an _economic restriction_ that must be observed: since $\bar s \geq \underline s$ by assumption, it cannot be that

$$C_0 < (\bar C - \bar F)^+$$

In other words, it should not be that case that (positive) losses incurred when a block is fully utilized $(\bar C - \bar F)$ exceed losses when a block is unutilized ($C_0$). Since $C_0 \geq 0$ this is automatically impossible in the intuitively appealing circumstance that

$$(\bar C - \bar F)^+ = 0$$

i.e. if it is the case that the ecosytem rewards full block utilization _in the absence of block reward_ with positive profit to the farmer. But if this is not the case, i.e. if the ecosystem associates a _loss_ to the farmer from fully utilizing a block, then this should be a signal to implement a change in e.g. the transactions (storage and compute) fees awarded for full block utilization. Thus, this condition acts as a _global participation incentive condition_, i.e. that it is profitable to participate in the ecosystem at full utilization.

If this condition is fulfilled (as one would expect), we have the simple result that $\underline s = 0$ and $\bar s = \bar C$, and the feasible block reward parameters $b$ and $c$ are those within the set

$$\{(b,c) \in \mathbb{R}^2_{++} | b\tanh(c) = \bar C \}$$

(The case where, for e.g. $\bar C > 0$, both $b$ and $c$ are less than zero is excluded from the $\bar s \geq \underline s$ restriction.)


Finally, note that there is no _global guarantee_ that any particular farmer (indexed by $i$), with their own (hidden) cost function $C^i(\cdot)$, will receive a block reward from their utilization $g^i$ such that in period $t$

$$s (g^i(t)) + F(g^i(t)) - C^i(g^i(t)) \geq 0$$

To provide such a guarantee would require data on the functions $F$ and $C$ (the former of which might be possible, but the latter of which is assumed to be hidden information). **The best that can be done is to assume that the protocol can be made aware of $\bar F$, $\bar C$ and $C_0$, and provide 'guardrails' on the polar cases of utilization** to ensure that the function $s(\cdot)$ has a 'smooth' transition from $\bar s$ to $\underline s$ when moving from zero to full utilization.

##### Local incentives for transactions inclusion vs. non-inclusion

There is an incentive for a farmer $i$ to include transactions within a block, rather than simply receive the block reward, provided that there exists _at least one_ utilization rate $g^i$ for which

$$F(g^i) - C^i(g^i) > \bar C$$

(Note that $\bar C$ is the _maximum_ block reward $\bar s$, and so it is not indexed by the farmer's identity). It may not be the case that this condition can be satisfied for farmer $i$, in which case the farmer is not economically suited to participation. But if at least one such $g^i$ can be found, then the block reward mechanism derived above provides a _local incentivization condition_ to utilize at least $g^i$, when sufficient transactions in the mempool exist to meet this value (or other values above the first such $g^i$).

As a possible avenue of future work, there exist functional forms for $F$ and $C^i$ such that _all_ values $g \geq g^i$ are themselves profitable utilization rates. If furthermore F(g) - C^i(g) is increasing for those values of $g$, then the farmer is incentivized to provide full utilization $g = 1$ if the mempool supplies enough transactions under the block reward mechanism provided here.)
