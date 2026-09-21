# Reputation

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md) · [identity.md](./identity.md) · [contribution.md](./contribution.md)  
**Related:** [vote.md](./vote.md) · [consensus.md](./consensus.md) · [privacy.md](./privacy.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [Reputation Formula](#3-reputation-formula)
4. [Context and Scope](#4-context-and-scope)
5. [Quality Coefficient](#5-quality-coefficient)
6. [Decay Function](#6-decay-function)
7. [Revocation Coefficient](#7-revocation-coefficient)
8. [Aggregation Across Contexts](#8-aggregation-across-contexts)
9. [Levels and Thresholds](#9-levels-and-thresholds)
10. [Snapshots](#10-snapshots)
11. [Caching](#11-caching)
12. [Determinism Requirements](#12-determinism-requirements)
13. [Numerical Precision](#13-numerical-precision)
14. [Validation Rules](#14-validation-rules)
15. [Examples](#15-examples)
16. [Test Vectors](#16-test-vectors)
17. [Open Questions](#17-open-questions)

---

## 1. Overview

**Reputation** is the derived measure of an identity's contribution within a context. It is computed from confirmed, non-revoked contributions, weighted by quality and decay.

Reputation is:

- **Derived**, not stored. It is computed from the ledger events on demand.
- **Contextual**. Reputation in one context does not automatically transfer to another.
- **Dynamic**. It changes as contributions are added, confirmed, revoked, or decay.
- **Deterministic**. Given the same events and the same time, every implementation computes the same value.
- **Non-transferable**. It cannot be sold, bought, or gifted.

Reputation is the basis for:

- vote weight (see [vote.md](./vote.md));
- access to roles;
- priority in bounties and grants;
- confirmation authority;
- validator eligibility.

**This file defines:**

- The formula (Section 3).
- Context scoping (Section 4).
- Quality (Section 5).
- Decay (Section 6).
- Revocation (Section 7).
- Aggregation across contexts (Section 8).
- Levels (Section 9).
- Snapshots (Section 10).
- Caching (Section 11).
- Determinism requirements (Section 12).
- Numerical precision (Section 13).
- Validation rules (Section 14).

This is the most mathematically sensitive part of the specification. Errors here break consensus.

---

## 2. Design Principles

### 2.1. Determinism above all

Every node **MUST** compute the same reputation for the same input. Any divergence is a critical bug.

### 2.2. Contextual

Reputation is computed **per context**. There is no global reputation.

A context may recognize another context's reputation (Section 8), but this is explicit, not automatic.

### 2.3. Derived from events

Reputation is not stored as a value. It is derived from the ledger by:

1. Collecting all contributions for the subject in the context.
2. Filtering to confirmed, non-revoked contributions.
3. Applying weights, quality, decay.
4. Summing.

### 2.4. Time-dependent

Reputation changes with time due to decay. The formula includes `t` (evaluation time).

### 2.5. Snapshot-friendly

Reputation can be frozen at a point in time (`snapshot`) for votes and audits.

### 2.6. Numerically bounded

Reputation is a non-negative real number. It is bounded above by the sum of all possible contributions (practically, it is finite).

### 2.7. No negative reputation

Reputation **MUST NOT** be negative. Revocation reduces it to zero, not below.

### 2.8. Recomputable

Any node can recompute reputation from scratch. Caching is an optimization, not a source of truth.

---

## 3. Reputation Formula

### 3.1. Base formula

For an identity `u` in context `c` at time `t`:

```
R(u, c, t) = Σ over all contributions i in context c by u:
    w_i × q_i × d(t - t_i) × s_i
```

Where:

- `w_i` — weight of contribution `i` (from weight class).
- `q_i` — quality coefficient of contribution `i` (0.0 to 1.0).
- `d(Δt)` — decay function for age `Δt = t - t_i`.
- `s_i` — revocation coefficient (1 if active, 0 if revoked).
- `t_i` — timestamp of contribution `i`.

### 3.2. Components

| Component | Range | Source |
|---|---|---|
| `w_i` | > 0 | Weight class in context rules |
| `q_i` | [0.0, 1.0] | Average of confirmation qualities |
| `d(Δt)` | (0, 1] | Decay function (Section 6) |
| `s_i` | {0, 1} | Revocation status |

### 3.3. Expanded formula

```
R(u, c, t) = Σ_i [ w_i × (Σ_j q_ij / n_i) × max(floor, 0.5 ^ ((t - t_i) / half_life)) × s_i ]
```

Where:

- `q_ij` — quality from confirmation `j` of contribution `i`.
- `n_i` — number of confirmations of contribution `i`.
- `floor` — decay floor (Section 6.4).
- `half_life` — decay half-life (Section 6.3).

### 3.4. Simplified form

For the common case (quality 1.0, no decay):

```
R(u, c, t) = Σ_i w_i × s_i
```

This is the sum of weights of confirmed, non-revoked contributions.

### 3.5. What is not in the formula

Reputation does **not** include:

- number of contributions (only their weights);
- duration of membership;
- number of confirmations (only quality);
- social connections;
- financial investment;
- token holdings.

Reputation is purely a function of confirmed contribution value over time.

### 3.6. Order of operations

To compute reputation:

1. Collect all `contribution.create` events for subject `u` in context `c`.
2. Filter to those with enough confirmations (confirmed state).
3. For each, collect all `contribution.confirm` events.
4. Compute quality `q_i` = average of confirmation qualities.
5. Determine revocation status `s_i`.
6. Look up weight `w_i` from context rules at `t_i`.
7. Compute decay `d(t - t_i)`.
8. Multiply and sum.

Steps **MUST** be applied in this order for determinism.

---

## 4. Context and Scope

### 4.1. Definition of context

A **context** is a named scope within which contributions are evaluated. It is created by a `community.create` event (see [contribution.md](./contribution.md#6-context-rules)).

Examples:

- `repo:github.com/x/y`
- `org:mycompany`
- `community:mycommunity`
- `coop:mycoop`

### 4.2. Reputation is per context

`R(u, c, t)` is defined only for a specific context `c`.

There is no `R(u, t)` at the protocol level.

### 4.3. Cross-context recognition

A context may recognize reputation from another context. This is expressed in the context's rules:

```json
{
  "context": "repo:github.com/x/y",
  "recognizes": [
    {
      "context": "repo:github.com/a/b",
      "weight": 0.5,
      "max_contribution": 1000
    }
  ]
}
```

Meaning: this context recognizes up to 1000 CU from `repo:github.com/a/b`, weighted at 0.5.

See Section 8 for the aggregation formula.

### 4.4. Context hierarchy

Contexts may have parents and children:

- `repo:github.com/x/y` — parent.
- `repo:github.com/x/y/frontend` — child.

By default:

- A child inherits the parent's rules unless overridden.
- Reputation in the parent **MAY** include child contributions (if configured).
- Reputation in the child does **not** automatically include parent contributions.

### 4.5. Context isolation

By default, contexts are **isolated**. Contributions in context A do not affect reputation in context B.

This is intentional:

- prevents cross-context Sybil amplification;
- allows communities to define their own standards;
- respects the sovereignty of each community.

### 4.6. Global reputation

There is **no global reputation** at the protocol level.

A context or a client **MAY** compute a "global" score by aggregating across contexts, but this is application-level, not protocol-level.

### 4.7. Context resolution

To compute reputation in context `c`:

1. Verify `c` exists in the ledger (via `community.create`).
2. Retrieve the context's rules.
3. Apply the rules to contributions in `c`.

If `c` does not exist, reputation is undefined (0 by convention).

---

## 5. Quality Coefficient

### 5.1. Definition

The quality coefficient `q_i` reflects the assessed quality of contribution `i`. It is a number in `[0.0, 1.0]`.

### 5.2. Source

Quality is set by confirmers. Each `contribution.confirm` event may include a `quality` field:

```json
{
  "type": "contribution.confirm",
  "payload": {
    "contribution_id": "blake3:...",
    "quality": 0.9
  }
}
```

If `quality` is absent, it defaults to `1.0`.

### 5.3. Aggregation

If multiple confirmations exist, `q_i` is the **arithmetic mean**:

```
q_i = (Σ_j q_ij) / n_i
```

Where `n_i` is the number of confirmations.

### 5.4. Why average, not sum?

- Sum would reward many low-quality confirmations.
- Average rewards consistent assessment.
- Outliers (one 0.1 among 0.9s) have limited effect.

### 5.5. Weighted average

Contexts **MAY** use a reputation-weighted average instead:

```
q_i = (Σ_j q_ij × R(confirmer_j, c, t_j)) / (Σ_j R(confirmer_j, c, t_j))
```

This gives more weight to confirmations from high-reputation identities.

If used, the context **MUST** specify this in its rules. The default is arithmetic mean.

### 5.6. Precision

Quality **MUST** be rounded to **6 decimal places** before use in the formula.

Example: `0.900000`, not `0.9` (though these are numerically equal, the canonical form matters for determinism).

### 5.7. Range enforcement

- Values below `0.0` **MUST** be rejected.
- Values above `1.0` **MUST** be rejected.
- Values outside `[0.0, 1.0]` in events are invalid.

### 5.8. Quality in test vectors

Test vectors use fixed quality values to ensure deterministic results.

### 5.9. Quality assessment

The protocol does not define how quality is assessed. Each context defines its own standards:

- formal rubrics;
- peer judgment;
- automated checks;
- hybrid.

The protocol only defines the coefficient.

### 5.10. Quality and revocation

If a contribution is revoked, quality is irrelevant (`s_i = 0`, so `CU = 0`).

### 5.11. Minimum quality threshold

Contexts **MAY** define a minimum quality threshold:

```json
{
  "min_quality": 0.5
}
```

Contributions with `q_i < min_quality` earn 0 CU.

Default: `0.0` (no threshold).

---

## 6. Decay Function

### 6.1. Purpose

Decay reduces the value of old contributions over time. It:

- prevents frozen power;
- encourages ongoing contribution;
- reflects that recent work is often more relevant.

### 6.2. Function

The decay function is exponential:

```
d(Δt) = 0.5 ^ (Δt / half_life)
```

Where:

- `Δt` = `t - t_i` (seconds since contribution).
- `half_life` = time for value to halve (seconds).

### 6.3. Half-life

The half-life is defined by the context:

```json
{
  "decay": {
    "enabled": true,
    "half_life_days": 730,
    "floor": 0.1
  }
}
```

| Parameter | Default | Meaning |
|---|---|---|
| `enabled` | false | Whether decay applies |
| `half_life_days` | 730 (2 years) | Time to halve |
| `floor` | 0.1 | Minimum remaining fraction |

### 6.4. Floor

Decay **MUST NOT** reduce below the floor:

```
d(Δt) = max(floor, 0.5 ^ (Δt / half_life))
```

If `floor = 0.1`, a contribution never falls below 10% of its original value.

If `floor = 0`, decay continues indefinitely.

If `floor = 1`, decay is effectively disabled (always 1).

### 6.5. Exempt classes

Some weight classes **MAY** be exempt from decay:

```json
{
  "decay": {
    "exempt_classes": ["foundation", "milestone"]
  }
}
```

Exempt contributions have `d = 1` always.

### 6.6. Disabled decay

If `enabled = false`:

```
d(Δt) = 1
```

All contributions keep full value indefinitely.

### 6.7. Examples

With `half_life = 2 years`:

| Age | d(Δt) |
|---|---|
| 0 days | 1.000 |
| 6 months | 0.840 |
| 1 year | 0.707 |
| 2 years | 0.500 |
| 4 years | 0.250 |
| 8 years | 0.125 |
| 20 years | 0.100 (floor) |

With `half_life = 1 year`:

| Age | d(Δt) |
|---|---|
| 0 days | 1.000 |
| 6 months | 0.707 |
| 1 year | 0.500 |
| 2 years | 0.250 |
| 4 years | 0.100 (floor) |

### 6.8. Rationale for exponential

- **Smooth.** No sudden drops.
- **Memoryless.** The half-life is the same at any age.
- **Familiar.** Same math as radioactive decay, widely understood.
- **Deterministic.** Easy to compute and verify.

### 6.9. Alternatives

Other decay functions exist:

- **Linear:** `d(Δt) = max(0, 1 - Δt / T)`. Simple, but has a hard cutoff.
- **Power-law:** `d(Δt) = (1 + Δt / T)^(-α)`. Heavier tail, more weight on old contributions.
- **Step:** `d = 1` for `Δt < T`, then drops. Discontinuous, discouraged.

CL uses exponential. Other functions **MAY** be added via RFC.

### 6.10. Precision

Decay **MUST** be computed with **double precision** and rounded to **6 decimal places**.

Example: `0.707107`, not `0.70710678`.

### 6.11. Time source

`t` (evaluation time) is:

- the **current time** for live reputation queries;
- the **snapshot time** for historical queries (votes, audits).

The evaluation time **MUST** be explicitly specified for every calculation.

### 6.12. Negative Δt

If `t < t_i` (future contribution), `Δt` would be negative.

This **MUST NOT** happen. If it does:

- the contribution is invalid (timestamp > current time);
- or the evaluation time is before the contribution's timestamp (reject the query).

### 6.13. Zero half-life

If `half_life = 0`, decay is undefined.

Validators **MUST** reject context rules with `half_life = 0` when decay is enabled.

### 6.14. Very large Δt

For very large `Δt`:

```
0.5 ^ (Δt / half_life) → 0
```

But with a floor, it stops at `floor`.

For numerical stability:

- cap `Δt / half_life` at a large value (e.g., 1000);
- compute `0.5 ^ min(Δt / half_life, 1000)`.

This prevents overflow and ensures determinism.

---

## 7. Revocation Coefficient

### 7.1. Definition

The revocation coefficient `s_i` is:

- `1` if the contribution is active (not revoked);
- `0` if the contribution is revoked.

### 7.2. Revocation chain

A contribution may be revoked and un-revoked multiple times. The final state is:

- the most recent `contribution.revoke` or `contribution.unrevoke` event;
- taking precedence by DAG order.

### 7.3. Computing s_i

To determine `s_i`:

1. Start with `s_i = 1` (active by default).
2. Iterate all `contribution.revoke` and `contribution.unrevoke` events for this contribution in DAG order.
3. Update `s_i` based on the most recent event.

If the most recent is `revoke`: `s_i = 0`.  
If the most recent is `unrevoke`: `s_i = 1`.  
If there is no revocation event: `s_i = 1`.

### 7.4. Effects

When `s_i = 0`:

- `CU_i = 0` regardless of weight, quality, or decay.
- Reputation is reduced accordingly.

### 7.5. Historical evaluation

For a historical query at time `t`:

- only consider revocations/un-revocations with `created_at ≤ t`.

This ensures historical reputation matches what was true at the time.

### 7.6. No negative CU

Revoked contributions contribute `0`, not negative values. Reputation **MUST NOT** go below zero due to revocation.

### 7.7. Mass revocation

If a community revokes all contributions from an identity (e.g., due to fraud), all `s_i` for that identity are set to `0`.

### 7.8. Un-revocation

If a revocation is overturned, `s_i` returns to `1` and the CU is restored (subject to decay).

---

## 8. Aggregation Across Contexts

### 8.1. Default behavior

By default, contexts are **isolated**. Reputation in one context does not include contributions from another.

### 8.2. Explicit recognition

A context may explicitly recognize other contexts:

```json
{
  "context": "repo:github.com/x/y",
  "recognizes": [
    {
      "context": "repo:github.com/a/b",
      "weight": 0.5,
      "max_contribution": 1000
    },
    {
      "context": "org:mycompany",
      "weight": 0.3,
      "max_contribution": 500
    }
  ]
}
```

### 8.3. Aggregation formula

If context `c` recognizes contexts `c_1, c_2, ..., c_k`:

```
R_total(u, c, t) = R_local(u, c, t) + Σ_j [ weight_j × min(R(u, c_j, t), max_contribution_j) ]
```

Where:

- `R_local(u, c, t)` — reputation from contributions in `c`.
- `weight_j` — recognition weight (0.0 to 1.0).
- `max_contribution_j` — cap on contribution from `c_j`.

### 8.4. Recognition weight

The weight `weight_j` is a number in `[0.0, 1.0]`:

- `1.0` — full recognition.
- `0.5` — half-weight.
- `0.0` — no recognition (equivalent to not listing).

Weights **MUST** be in `[0.0, 1.0]`. Higher values are invalid.

### 8.5. Cap

The cap `max_contribution_j` limits how much reputation from `c_j` counts.

This prevents:

- cross-context Sybil amplification;
- one context dominating another;
- reputation laundering.

### 8.6. Example

Alice has:

- `R_local` in `repo:x/y` = 200.
- `R` in `repo:a/b` = 1500.
- `R` in `org:mycompany` = 800.

Context `repo:x/y` recognizes:

- `repo:a/b` with weight 0.5, cap 1000.
- `org:mycompany` with weight 0.3, cap 500.

`R_total = 200 + 0.5 × min(1500, 1000) + 0.3 × min(800, 500)`  
`R_total = 200 + 0.5 × 1000 + 0.3 × 500`  
`R_total = 200 + 500 + 150 = 850`

### 8.7. Cycles

Contexts **MUST NOT** form recognition cycles.

If `c_1` recognizes `c_2` and `c_2` recognizes `c_1`, the aggregation is undefined.

Validators **MUST** reject context rules that create cycles.

To detect cycles:

- build a directed graph of recognition edges;
- check for cycles using DFS or topological sort;
- reject if a cycle is found.

### 8.8. Transitive recognition

Recognition is **not transitive** by default.

If `c_1` recognizes `c_2`, and `c_2` recognizes `c_3`, `c_1` does **not** automatically recognize `c_3`.

To enable transitive recognition:

```json
{
  "recognition": {
    "transitive": true,
    "max_depth": 2
  }
}
```

If `transitive = true`, recognition propagates up to `max_depth`.

### 8.9. Manual aggregation

Clients **MAY** compute custom aggregations for display, e.g., "total reputation across all contexts".

Such aggregations are **informative**, not protocol-level. They **MUST NOT** be used for governance.

### 8.10. No global reputation

There is no protocol-level global reputation. Any "global" score is a client-side convention.

---

## 9. Levels and Thresholds

### 9.1. Definition

Contexts define **levels** — thresholds of reputation that unlock rights.

```json
{
  "levels": {
    "newbie": 0,
    "member": 10,
    "trusted": 100,
    "veteran": 500,
    "council": 2000
  }
}
```

### 9.2. Rights per level

Each level grants rights:

| Level | Threshold | Typical rights |
|---|---|---|
| Newbie | 0 | Read, small contributions |
| Member | 10 | Contribute, comment |
| Trusted | 100 | Confirm, moderate |
| Veteran | 500 | Vote, create projects |
| Council | 2000 | Governance, audit, grants |

The exact rights are defined by the context.

### 9.3. Level lookup

To determine an identity's level in context `c`:

1. Compute `R(u, c, t)`.
2. Find the highest level whose threshold is ≤ `R`.

### 9.4. Threshold changes

Thresholds **MAY** change via `rule.change` events.

Changes are **not retroactive** for historical queries (which use the thresholds in effect at the query time).

### 9.5. Multiple thresholds

A context may define multiple thresholds for different purposes:

```json
{
  "thresholds": {
    "confirm_small": 10,
    "confirm_large": 100,
    "vote": 500,
    "validate": 2000,
    "audit": 1000
  }
}
```

Each threshold is checked independently.

### 9.6. Reputation precision for thresholds

For threshold comparison:

- `R` **MUST** be computed with 6 decimal places.
- Comparison uses `R ≥ threshold`.
- Ties (exactly at threshold) count as **passing**.

Example: `R = 100.000000`, threshold = 100 → passes.

### 9.7. Negative thresholds

Thresholds **MUST NOT** be negative. Minimum is `0`.

### 9.8. Level decay

Levels are computed from current reputation, which decays. An identity may drop from a level if its reputation falls below the threshold.

Communities **MAY** add "sticky levels" — once achieved, a level is retained for a period even if reputation drops.

### 9.9. Level display

Clients **SHOULD** display the identity's current level in the context.

The level is a convention, not a stored value.

---

## 10. Snapshots

### 10.1. Purpose

A **snapshot** is a frozen reputation value at a specific time. Used for:

- votes (prevent gaming during the vote);
- audits (reconstruct historical state);
- disputes (was the threshold met at the time?).

### 10.2. Structure

```json
{
  "context": "repo:github.com/x/y",
  "time": 1730000000,
  "state_root": "blake3:...",
  "reputations": {
    "did:cl:main:alice": 150.5,
    "did:cl:main:bob": 320.75,
    ...
  },
  "rules_version": "blake3:..."
}
```

### 10.3. Snapshot creation

A snapshot **MUST** be deterministic: given the ledger up to time `t`, every node computes the same values.

### 10.4. Snapshot time

The snapshot time is the **maximum event timestamp** included in the snapshot. Events with `created_at > snapshot_time` are excluded.

### 10.5. Snapshot root

The `state_root` is a BLAKE3 hash over the canonical CBOR of the `reputations` map.

This allows light clients to verify a snapshot without recomputing.

### 10.6. Rules version

The snapshot includes a `rules_version` — the hash of the context rules at snapshot time.

This ensures historical queries use the correct rules.

### 10.7. Snapshot for votes

Votes use a snapshot created at the vote's `vote.create` event:

```json
{
  "type": "vote.create",
  "payload": {
    "snapshot": "blake3:..."
  }
}
```

The snapshot hash references a `checkpoint` event or is computed on demand.

### 10.8. Verification

To verify a snapshot:

1. Compute the reputations from the ledger up to snapshot time.
2. Compute the `state_root`.
3. Compare with the published snapshot.

If they differ, the snapshot is invalid.

### 10.9. Snapshot storage

Snapshots **MAY** be:

- stored as ledger events (`checkpoint`);
- computed on demand;
- cached by nodes.

### 10.10. Snapshot as checkpoint

A `checkpoint` event (see [ledger.md](./ledger.md)) **MAY** include reputation snapshots for all contexts.

This allows nodes to bootstrap quickly.

### 10.11. Snapshot size

Snapshots of large contexts may be large. Mitigations:

- store only `state_root` on-ledger;
- store full snapshot off-chain;
- use Merkle proofs for individual entries.

### 10.12. Snapshot expiry

Snapshots do not expire. They are historical facts.

However, nodes **MAY** garbage-collect old snapshots if they can be recomputed.

---

## 11. Caching

### 11.1. Purpose

Computing reputation from scratch is `O(n)` where `n` is the number of contributions. For large contexts, this is slow.

Caching speeds up queries without changing results.

### 11.2. Cache invariants

- The cache **MUST** be consistent with the ledger.
- Cache invalidation **MUST** occur when relevant events are added.
- Cache **MUST NOT** affect the result of reputation computation.

**The cache is not a source of truth.** Any value in the cache **MUST** be recomputable from events.

### 11.3. Cache invalidation triggers

A cache entry for `(u, c)` **MUST** be invalidated when:

- a new `contribution.create` for `u` in `c`;
- a new `contribution.confirm` for such a contribution;
- a new `contribution.revoke` or `contribution.unrevoke`;
- a `rule.change` in `c` (affects weights, decay, thresholds);
- a `community.create` that affects `c` (for cross-context recognition);
- time advances (decay).

Time-based invalidation is the hardest. Options:

- **Time-bucketed cache.** Recompute every N minutes/hours.
- **Incremental decay.** Store `R` and `last_update_time`; on query, apply decay delta.
- **On-demand.** No time-based cache; compute fresh on each query.

### 11.4. Incremental decay

A common technique:

- Store `R_base` (undecayed sum) and `last_update`.
- On query at time `t`:
  ```
  R(t) = Σ_i w_i × q_i × s_i × 0.5 ^ ((t - t_i) / half_life) × 1
  ```
  Cannot be incrementally decayed exactly (different contributions have different ages).

**Alternative:** store contributions grouped by age bucket (e.g., by week).

```
R(t) = Σ_bucket [ R_bucket × decay(t - t_bucket) ]
```

This is approximate (within one bucket) but exact enough for most uses. For exact results, recompute.

**Precision note:** if buckets are used, the context **MUST** document the approximation. Consensus-critical uses (votes, audits) **MUST** use exact computation.

### 11.5. Per-contribution cache

Each contribution's `CU_i` can be cached independently:

```
CU_i = w_i × q_i × d(t - t_i) × s_i
```

On query:

```
R(u, c, t) = Σ_i CU_i(t)
```

This requires recomputing `d(t - t_i)` for each contribution on each query. For large `n`, this is slow.

### 11.6. Merkle-ized cache

A more advanced approach:

- Build a Merkle tree over contributions, with `t_i` in the leaves.
- Cache the root.
- For a query at time `t`, walk the tree and apply decay per leaf.

This is efficient if the tree is pre-built. For small contexts, overkill.

### 11.7. Snapshot-based cache

Nodes **MAY** cache snapshots at regular intervals (e.g., daily). Queries between snapshots use the most recent snapshot plus incremental updates.

This gives:

- `O(1)` query time for snapshots;
- `O(k)` for updates since the snapshot, where `k` is small.

### 11.8. Cache coherence

If multiple nodes cache reputation, they **MUST** produce the same results.

Any difference indicates a bug in caching logic or a divergence in the underlying rules.

### 11.9. No cache poisoning

A node **MUST NOT** trust a cached value without verifying it can be reproduced from events.

If a cached value is inconsistent with the ledger, it **MUST** be discarded.

### 11.10. Distributed cache

Nodes **MAY** share cache values via the network. If so:

- each value **MUST** include a proof or hash of the underlying events;
- recipients **MUST** verify the proof before trusting the value.

### 11.11. Recommended implementation

For a first implementation:

- No caching. Compute on demand.
- Optimize later when performance requires it.

Correctness first.

---

## 12. Determinism Requirements

### 12.1. The core rule

**Given the same events and the same evaluation time, every implementation MUST produce the same reputation value.**

No exceptions. Any divergence is a critical bug.

### 12.2. Sources of non-determinism to avoid

- **Floating-point errors.** Use fixed precision (Section 13).
- **Order of summation.** Sum in a deterministic order (e.g., by event ID).
- **Time source.** Use the specified evaluation time, not the local clock.
- **Iteration order of maps.** Iterate in canonical order (sorted keys).
- **Platform differences.** Different CPUs may compute floats differently.
- **Library differences.** Different math libraries may give slightly different results for `0.5 ^ x`.

### 12.3. Summation order

To ensure deterministic summation:

- Collect contributions.
- Sort by event ID (lexicographic).
- Sum in that order.

Floating-point addition is not associative. Sorting ensures consistent order across implementations.

**Alternative:** use fixed-point arithmetic (Section 13.3).

### 12.4. Exponentiation

`0.5 ^ x` where `x = Δt / half_life`:

- **MUST** be computed using a deterministic algorithm.
- **SHOULD** use the standard library's `pow` function.
- **MAY** use a lookup table for common values.

Implementations **MUST** agree on the algorithm. This is the most likely source of divergence.

**Recommendation:** use `exp(x × ln(0.5))` with double precision, then round to 6 decimals.

### 12.5. Rounding

All intermediate values **MUST** be rounded consistently:

- Before summing: each `CU_i` rounded to 6 decimals.
- After summing: result rounded to 6 decimals.
- Consistency in rounding mode: **round half to even** (banker's rounding).

### 12.6. Comparison

Threshold comparisons **MUST** use the rounded value:

```
if round(R, 6) >= threshold: pass
```

Not the unrounded value.

### 12.7. Deterministic test vectors

Test vectors **MUST** cover:

- Simple sums (no decay, no quality).
- Decay with various ages.
- Quality averaging.
- Revocation.
- Cross-context aggregation.
- Large numbers of contributions (performance and precision).
- Edge cases: zero contributions, floor decay, minimum quality.

### 12.8. Cross-implementation testing

Two implementations **MUST** agree on all test vectors. If they do not, the specification is ambiguous and needs clarification.

### 12.9. Non-deterministic features

The following are **not allowed** in reputation computation:

- Random number generation.
- Hash-based ordering (unless seeded deterministically).
- Time-based ordering (except the specified evaluation time).
- Concurrency (results must be serializable).

### 12.10. Versioning of the formula

If the formula changes (e.g., new decay function), it **MUST** be:

- a MAJOR version bump;
- documented in an RFC;
- accompanied by migration notes.

Historical reputation computed with the old formula **MUST** remain retrievable.

---

## 13. Numerical Precision

### 13.1. Range

Reputation values are:

- **Non-negative.** Minimum: 0.
- **Bounded.** Theoretically unbounded, but practically limited by the number of contributions and their weights.
- **Real.** Fractional values are allowed.

### 13.2. Internal representation

Implementations **MAY** use:

- IEEE 754 double precision (64-bit float);
- IEEE 754 single precision (32-bit float) — **not recommended**;
- Fixed-point integers (see below);
- Arbitrary precision (e.g., `decimal` in Python).

**Recommendation:** use double precision for computation, round to 6 decimals for storage and comparison.

### 13.3. Fixed-point arithmetic

To avoid floating-point issues entirely, use fixed-point:

- Store reputation as an integer scaled by `10^6`.
- Example: `150.5` → `150500000`.
- All operations done in integer arithmetic.
- Exponentiation and division use integer approximations.

This guarantees determinism across platforms.

**Trade-off:** more complex to implement, but eliminates an entire class of bugs.

**Recommendation:** fixed-point for consensus-critical paths (votes, thresholds); floating-point for display.

### 13.4. Rounding rule

All rounding uses **round half to even** (banker's rounding):

- `0.5` → `0`
- `1.5` → `2`
- `2.5` → `2`
- `3.5` → `4`

This avoids statistical bias and is standard in IEEE 754.

### 13.5. Precision of components

| Component | Precision | Notes |
|---|---|---|
| `w_i` | 6 decimals | Typically integer, but fractional allowed |
| `q_i` | 6 decimals | Range [0, 1] |
| `d(Δt)` | 6 decimals | Range (floor, 1] |
| `s_i` | exact | 0 or 1 |
| `CU_i` | 6 decimals | Product |
| `R` | 6 decimals | Sum |

### 13.6. Intermediate precision

To avoid accumulating rounding errors:

- Compute `CU_i` in higher precision (e.g., double).
- Round `CU_i` to 6 decimals.
- Sum rounded `CU_i` in higher precision.
- Round the sum to 6 decimals.

### 13.7. Overflow

For very large reputations (e.g., billions of CU), double precision is still sufficient (up to ~10^15 with 6-decimal precision).

If fixed-point is used, ensure the integer type can hold `max_R × 10^6`. Use 64-bit integers (max ~9.2 × 10^18).

### 13.8. Underflow

For very small values (e.g., `d(Δt)` near floor):

- Values below `10^-6` are rounded to 0.
- This is intentional — sub-micro precision is meaningless.

### 13.9. NaN and Infinity

These **MUST NOT** appear in reputation values.

If computation produces them (e.g., division by zero), it is a bug. Validators **MUST** reject such events.

### 13.10. Comparison tolerance

For comparison of two reputations computed by different implementations:

- Exact equality is required after rounding to 6 decimals.
- If they differ, at least one implementation is wrong.

No tolerance is allowed for consensus-critical values.

### 13.11. Display precision

Clients **MAY** display reputation with fewer decimals (e.g., 2 or 0).

Display precision is cosmetic. It **MUST NOT** affect governance or thresholds.

### 13.12. Canonical form

The canonical form of a reputation value in test vectors and snapshots:

- 6 decimal places;
- trailing zeros preserved;
- no leading zeros (except `0.xxxxxx`);
- decimal separator: `.` (dot).

Example: `150.500000`, not `150.5`, not `150,5`.

---

## 14. Validation Rules

Validators **MUST** enforce these rules when processing reputation-related events.

### 14.1. Contribution events

- All rules from [contribution.md](./contribution.md#13-validation-rules) apply.
- The `weight_class` **MUST** be defined in the context at `created_at`.

### 14.2. Context rules

- The context **MUST** exist before contributions.
- Rules **MUST** be consistent (no cycles in recognition).
- `half_life` **MUST** be > 0 if decay is enabled.
- `floor` **MUST** be in `[0, 1]`.
- Recognition weights **MUST** be in `[0, 1]`.
- Thresholds **MUST** be non-negative.

### 14.3. Snapshot verification

- A snapshot **MUST** be verifiable from the ledger.
- If a snapshot is referenced (e.g., in a vote), it **MUST** match the recomputed value.

### 14.4. Threshold checks

- Thresholds **MUST** be checked against the rounded reputation value.
- Ties pass (reputation exactly at threshold is sufficient).

### 14.5. Quality values

- Quality **MUST** be in `[0.0, 1.0]`.
- Values outside this range are invalid.
- Quality **MUST** be present if specified in the context rules.

### 14.6. Revocation

- Revocation events **MUST** reference valid contributions.
- Revocation **MUST** be authorized (by subject, issuer, auditor, or vote).
- Un-revocation **MUST** be authorized by the same or higher authority.

### 14.7. Cross-context

- Recognition edges **MUST NOT** form cycles.
- If transitive, `max_depth` **MUST** be a positive integer.
- Recognized contexts **MUST** exist.

### 14.8. Cache

- Cache values **MUST** be reproducible from events.
- If not, the cache **MUST** be invalidated.

### 14.9. Determinism

- All computations **MUST** be deterministic.
- Any non-determinism is a bug.

---

## 15. Examples

### 15.1. Simple reputation

Alice has 3 contributions in `repo:x/y`:

| Contribution | Weight | Quality | Age | Decay | s |
|---|---|---|---|---|---|
| C1 | 5 | 1.0 | 0 | 1.0 | 1 |
| C2 | 3 | 0.8 | 1 year | 0.707107 | 1 |
| C3 | 10 | 0.5 | 2 years | 0.5 | 1 |

`CU_1 = 5 × 1.0 × 1.0 × 1 = 5.000000`  
`CU_2 = 3 × 0.8 × 0.707107 × 1 = 1.697057`  
`CU_3 = 10 × 0.5 × 0.5 × 1 = 2.500000`

`R = 5.000000 + 1.697057 + 2.500000 = 9.197057`

### 15.2. Reputation with revocation

Same as above, but C3 is revoked:

`CU_3 = 10 × 0.5 × 0.5 × 0 = 0.000000`

`R = 5.000000 + 1.697057 + 0.000000 = 6.697057`

### 15.3. Cross-context aggregation

Context `repo:x/y` has:

- `R_local(Alice)` = 100.
- Recognizes `repo:a/b` weight 0.5, cap 200.
- `R(Alice, repo:a/b)` = 300.

`R_total = 100 + 0.5 × min(300, 200) = 100 + 0.5 × 200 = 200`

### 15.4. Threshold check

Context threshold for "trusted": 100.

Alice has `R = 100.000000`. She **passes** (exactly at threshold).

Bob has `R = 99.999999`. He **fails** (below threshold).

### 15.5. Decay over time

Contribution of weight 10, quality 1.0, created at `t_0`.

| Age | Decay (half-life 2y) | CU |
|---|---|---|
| 0 | 1.000000 | 10.000000 |
| 1 year | 0.707107 | 7.071070 |
| 2 years | 0.500000 | 5.000000 |
| 4 years | 0.250000 | 2.500000 |
| 10 years | 0.100000 (floor) | 1.000000 |
| 20 years | 0.100000 (floor) | 1.000000 |

### 15.6. Snapshot

At time `t = 1730000000`, the state of context `repo:x/y` includes Alice's reputation = 150.5.

The snapshot:

```json
{
  "context": "repo:x/y",
  "time": 1730000000,
  "state_root": "blake3:...",
  "reputations": {
    "did:cl:main:alice": 150.500000,
    ...
  }
}
```

### 15.7. Level determination

Context thresholds:

| Level | Threshold |
|---|---|
| Newbie | 0 |
| Member | 10 |
| Trusted | 100 |
| Veteran | 500 |
| Council | 2000 |

Alice has `R = 450`. Her level: **Trusted** (highest threshold ≤ 450).

Bob has `R = 550`. His level: **Veteran**.

Carol has `R = 5000`. Her level: **Council**.

### 15.8. Aggregation with cap

Context `c` recognizes:

- `c_1`: weight 0.5, cap 100.
- `c_2`: weight 0.3, cap 1000.
- `c_3`: weight 1.0, cap 500.

Alice's reputation:

- `R_local` = 200.
- `R(c_1)` = 500.
- `R(c_2)` = 200.
- `R(c_3)` = 3000.

`R_total = 200 + 0.5×min(500,100) + 0.3×min(200,1000) + 1.0×min(3000,500)`  
`R_total = 200 + 0.5×100 + 0.3×200 + 1.0×500`  
`R_total = 200 + 50 + 60 + 500 = 810`

---

## 16. Test Vectors

Test vectors for reputation live in `spec/test-vectors/reputation.json`.

### 16.1. Coverage

- Empty reputation (no contributions) = 0.
- Single contribution, no decay.
- Multiple contributions, summation order.
- Decay at various ages (0, half-life, 2× half-life, at floor).
- Quality averaging.
- Revocation.
- Un-revocation.
- Cross-context aggregation.
- Cycle detection.
- Threshold comparisons.
- Precision edge cases (round half to even).
- Large numbers (1000+ contributions).

### 16.2. Format

```json
{
  "description": "Single contribution, no decay",
  "context_rules": {
    "weights": {"commit": 5},
    "decay": {"enabled": false}
  },
  "contributions": [
    {
      "id": "blake3:...",
      "subject": "did:cl:test:alice",
      "weight_class": "commit",
      "timestamp": 1730000000,
      "confirmations": [
        {"quality": 1.0}
      ],
      "revoked": false
    }
  ],
  "evaluation_time": 1730000000,
  "expected_reputation": "5.000000"
}
```

### 16.3. Determinism check

For each test vector:

1. Compute reputation using the specified inputs.
2. Compare with `expected_reputation`.
3. If different, the implementation is non-compliant.

### 16.4. Cross-implementation

Test vectors **MUST** pass on at least two independent implementations before protocol version 1.0.

### 16.5. Boundary tests

Test vectors **MUST** include:

- Reputation exactly at a threshold.
- Reputation one unit above and below a threshold.
- Decay exactly at half-life.
- Decay exactly at floor.
- Quality exactly 0.0, 0.5, 1.0.
- Recognition exactly at cap.

These test the precision rules.

---

## 17. Open Questions

- Should reputation be **integer** (fixed-point) at the protocol level to avoid float issues?
- How to handle **negative quality** (penalties)?
- Should there be a **maximum reputation** cap?
- How to handle **cross-context reputation laundering** (contributing in a low-standard context to inflate reputation in a high-standard one)?
- Should decay be **per-context** or **global**?
- How to handle **reputation in sub-contexts**?
- Should **exempt classes** be a fixed list or context-defined?
- How to handle **reputation for organizations** (multiple identities under one org)?
- Should there be a **minimum age** for reputation to count (to prevent flash farming)?
- How to handle **reputation transfers** when an identity rotates keys?
- Should there be a **reputation decay for inactive identities** (beyond contribution decay)?
- How to handle **retroactive rule changes** (if a context changes weights, does old reputation change)?
- Should there be a **reputation floor for newcomers** (minimum starting reputation)?
- How to handle **reputation across federated ledgers**?

These will be resolved through RFCs and community discussion.

---

## Summary

**Reputation formula:**

```
R(u, c, t) = Σ_i [ w_i × q_i × d(t - t_i) × s_i ]
```

**Components:**

- `w_i` — weight (from context rules).
- `q_i` — quality (average of confirmations).
- `d(Δt)` — decay (exponential with floor).
- `s_i` — revocation (0 or 1).

**Key properties:**

- Contextual (no global reputation).
- Derived (not stored).
- Deterministic (same input → same output).
- Time-dependent (decay).
- Snapshot-friendly (frozen at time `t`).

**Aggregation:**

- By default, contexts are isolated.
- Explicit recognition with weight and cap.
- No cycles.

**Precision:**

- 6 decimal places.
- Round half to even.
- Consider fixed-point for consensus-critical paths.

**Caching:**

- Optimization only.
- Must be consistent with ledger.
- Invalidated on relevant events.

**Validation:**

- Structural, semantic, deterministic.
- Threshold checks on rounded values.
- Ties pass.

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [identity.md](./identity.md) — identity model.
- [contribution.md](./contribution.md) — contribution records.
- [vote.md](./vote.md) — voting (uses snapshots).
- [ledger.md](./ledger.md) — checkpoints and snapshots.
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---