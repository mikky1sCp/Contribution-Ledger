# Consensus

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md) · [identity.md](./identity.md) · [ledger.md](./ledger.md) · [reputation.md](./reputation.md)  
**Related:** [sync.md](./sync.md) · [vote.md](./vote.md) · [privacy.md](./privacy.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [Why Not PoW or PoS](#3-why-not-pow-or-pos)
4. [Validator Model](#4-validator-model)
5. [Validator Selection](#5-validator-selection)
6. [Finalization](#6-finalization)
7. [Finalization Process](#7-finalization-process)
8. [Validator Rotation](#8-validator-rotation)
9. [Validator Removal](#9-validator-removal)
10. [Forks](#10-forks)
11. [Federation](#11-federation)
12. [Cross-Ledger Consensus](#12-cross-ledger-consensus)
13. [Security Model](#13-security-model)
14. [Validation Rules](#14-validation-rules)
15. [Examples](#15-examples)
16. [Test Vectors](#16-test-vectors)
17. [Open Questions](#17-open-questions)

---

## 1. Overview

**Consensus** is how CL decides which events are final. Without consensus, two nodes could accept different sets of events and diverge.

CL uses **federated consensus**: a set of validators, chosen by the community, sign events to finalize them. There is no mining, no staking, no token.

**This file defines:**

- Why CL rejects PoW and PoS (Section 3).
- The validator model (Section 4).
- How validators are selected (Section 5).
- What finalization means (Section 6).
- The finalization process (Section 7).
- How validators rotate (Section 8).
- How validators are removed (Section 9).
- How forks are handled (Section 10).
- How separate ledgers federate (Section 11).
- Cross-ledger consensus (Section 12).
- The security model (Section 13).
- What validators enforce (Section 14).

Consensus is the most politically sensitive part of CL. It determines who has power and how power changes. Mistakes here are existential.

---

## 2. Design Principles

### 2.1. No money in consensus

Validators are **not** paid in a token. They are not selected by stake. They do not earn from emission.

This is a fundamental difference from PoW and PoS. It eliminates:

- the race for hash power;
- plutocracy (rich get richer);
- the incentive to attack for profit.

### 2.2. Reputation, not capital

Validators are chosen based on **reputation** and **community trust**, not on how much money they have.

Reputation cannot be bought (see [reputation.md](./reputation.md)). Therefore, validator seats cannot be bought.

### 2.3. Federated, not global

CL does **not** have a single global validator set. Each community has its own validators.

This means:

- communities are sovereign;
- there is no single point of failure;
- different communities can have different rules.

### 2.4. Explicit finality

An event is either:

- **pending** — received but not final;
- **finalized** — signed by enough validators;
- **rejected** — invalid.

Pending events **MAY** be reverted. Finalized events **MUST NOT** be reverted (except by fork, Section 10).

### 2.5. Validators are accountable

Validators **MUST**:

- run reliable infrastructure;
- sign only valid events;
- participate in rotation;
- be subject to removal by the community.

Validators **MUST NOT**:

- sign conflicting events;
- censor valid events;
- collude to alter history.

Violations result in removal and reputation penalty.

### 2.6. Fork is a right

If validators misbehave, the community **MAY** fork the ledger. Forking is not a catastrophe — it is a safety valve.

### 2.7. Federation over unification

Different communities **MAY** run independent ledgers and interoperate. There is no requirement for a single global consensus.

### 2.8. Determinism

Given the same set of events and the same validator set, all nodes **MUST** compute the same finality.

---

## 3. Why Not PoW or PoS

### 3.1. PoW (Proof of Work)

**How it works:** miners compete to solve a hash puzzle; the winner proposes the next block; the chain with the most work wins.

**Problems for CL:**

- **Energy waste.** Mining consumes enormous electricity for no useful output.
- **Requires a token.** Miners must be paid, which requires emission.
- **Creates a mining industry.** ASICs, pools, and hardware races.
- **Plutocratic over time.** Larger miners dominate.
- **Wrong incentive.** Miners are incentivized by token price, not by usefulness.
- **Not useful for reputation.** Reputation is not a commodity to be mined.

**Conclusion:** PoW is incompatible with CL's principles.

### 3.2. PoS (Proof of Stake)

**How it works:** validators are chosen based on how many tokens they stake; more stake = more influence.

**Problems for CL:**

- **Requires a token.** There is no token in CL.
- **Plutocracy.** The rich get more power.
- **Nothing-at-stake.** Validators can vote on multiple forks without cost (mitigated by slashing, but still an issue).
- **Token price manipulation.** Attacks on the token affect consensus.
- **Wrong incentive.** Validators are incentivized by token value, not by community trust.
- **Not compatible with "reputation cannot be bought".** PoS is exactly the opposite.

**Conclusion:** PoS is incompatible with CL's principles.

### 3.3. What CL uses instead

**Federated consensus** with **reputational validators**:

- Validators are chosen by the community, based on reputation.
- No token, no stake, no mining.
- Finalization requires a threshold of validator signatures.
- Validators rotate.
- Communities can fork.

This is closer to how:

- IETF standards are approved (rough consensus, no token);
- Wikipedia operates (community trust, no token);
- Certificate Transparency works (multiple independent logs);
- Distributed databases in enterprises work (known validators).

### 3.4. Comparison

| Property | PoW | PoS | CL |
|---|---|---|---|
| Token required | Yes | Yes | No |
| Energy use | High | Low | Low |
| Validator selection | Hash power | Stake | Reputation |
| Plutocracy | Over time | Yes | No |
| Finality | Probabilistic | Probabilistic or explicit | Explicit |
| Fork risk | High | Medium | Low (with federation) |
| Environmental impact | High | Low | Low |
| Incentive | Token price | Token price | Community trust |

### 3.5. Trade-offs

Federated consensus has trade-offs:

- **Trust assumption.** Users trust the validator set, not math alone.
- **Smaller scale.** Harder to scale to thousands of validators.
- **Governance complexity.** Who decides who is a validator?

These trade-offs are acceptable for CL's goals. CL is not trying to be a global currency. It is trying to be a coordination layer for communities.

---

## 4. Validator Model

### 4.1. What is a validator

A **validator** is a node that:

- verifies events;
- signs finalization;
- participates in rotation;
- stores the ledger (at least the finalized portion);
- is available and reliable.

Validators are **not**:

- miners (no hashing);
- stakers (no money at risk);
- block producers (no blocks);
- authorities (they cannot change rules unilaterally).

### 4.2. Validator identity

A validator is identified by a DID (see [identity.md](./identity.md)).

Typically, a validator is:

- an individual with high reputation;
- an organization (e.g., a foundation, cooperative);
- a technical team running infrastructure.

A validator **MUST** be a Level 2+ identity (verified).

### 4.3. Validator set

Each **context** (community) has its own **validator set**.

- Small communities: 3–5 validators.
- Medium: 7–15.
- Large: 15–50.

The set size is a community decision. Larger sets are more secure but slower.

### 4.4. Validator rights

Validators **MAY**:

- sign events for finalization;
- propose checkpoints;
- participate in dispute resolution (as auditors);
- vote on rule changes (as members of the community).

Validators **MUST NOT**:

- unilaterally change rules;
- censor valid events;
- sign conflicting events;
- use their position for personal gain outside the rules.

### 4.5. Validator obligations

Validators **MUST**:

- run a node with sufficient uptime (e.g., 99%);
- process and verify incoming events;
- sign finalization within a reasonable time;
- participate in rotation;
- respond to disputes when selected;
- publish their identity and contact.

Failure to meet obligations **MAY** result in removal.

### 4.6. Validator rewards

Validators **MAY** be compensated by:

- community dues (from [economics.md](../docs/economics.md));
- grants from funds;
- payment from organizations;
- reputation and influence.

There is **no protocol-level reward**. Validators are not paid by the protocol. They are paid by the community or external parties.

This is intentional:

- prevents a validator economy driven by emission;
- keeps validators accountable to the community;
- allows communities to decide how to fund validators.

### 4.7. Validator penalties

Validators **MAY** be penalized (by reputation loss, removal, or community action) for:

- downtime (missed finalizations);
- signing invalid events;
- signing conflicting events (equivocation);
- censorship;
- collusion.

Penalties are defined by the community's rules.

### 4.8. Validator count

The validator count is a trade-off:

- **More validators:** more decentralized, slower.
- **Fewer validators:** faster, less decentralized.

Typical thresholds:

| Community size | Validators | Finalization threshold |
|---|---|---|
| Small (< 100) | 3 | 2/3 |
| Medium (100–1000) | 5–7 | 2/3 |
| Large (1000+) | 7–15 | 2/3 |
| Very large | 15–50 | 2/3 |

### 4.9. Validator visibility

Validators **MUST** be publicly listed in the ledger:

- their DID;
- their contact;
- their uptime history;
- their participation in past finalizations.

This allows the community to evaluate and replace them.

### 4.10. No anonymous validators

Validators **MUST** be Level 2+ (verified) identities.

Anonymous validators are not allowed, because:

- the community needs to hold them accountable;
- censorship and collusion are harder to detect without identity;
- validator trust is social, not mathematical.

---

## 5. Validator Selection

### 5.1. How validators are chosen

Validators are chosen by the community. The exact process is defined in the community's rules.

Common processes:

1. **Community vote** — members vote on candidates.
2. **Council appointment** — a council selects validators.
3. **Reputation threshold** — anyone above a reputation threshold can become a validator (with community approval).
4. **Rotation** — validators are selected randomly from a pool of eligible candidates.

### 5.2. Eligibility

To be eligible as a validator, an identity **MUST**:

- be Level 2+;
- have reputation above a threshold (e.g., 500 in the context);
- have no active penalties (e.g., recent equivocation);
- meet technical requirements (uptime, hardware);
- be approved by the community (per rules).

### 5.3. Nomination

Candidates **MAY** nominate themselves via a `validator.nominate` event:

```json
{
  "type": "validator.nominate",
  "author": "did:cl:main:candidate",
  "payload": {
    "context": "repo:x/y",
    "contact": "https://...",
    "infrastructure": {
      "location": "EU",
      "uptime_30d": 0.99,
      "hardware": "cloud-vm"
    }
  }
}
```

### 5.4. Approval

Approval depends on the community's rules. Options:

**Option A: Vote.**
A vote is opened; members vote; approved with threshold (e.g., 2/3).

**Option B: Council.**
The council reviews the candidate and approves/rejects.

**Option C: Reputation threshold.**
Anyone above a threshold is automatically eligible; the community ratifies via a simple vote.

### 5.5. Adding a validator

Once approved, the validator is added via a `validator.add` event:

```json
{
  "type": "validator.add",
  "author": "did:cl:main:community-admin",
  "payload": {
    "context": "repo:x/y",
    "validator": "did:cl:main:candidate",
    "effective_at": 1730100000
  }
}
```

The event **MUST** be signed by an authorized identity (admin, council, or approved by vote).

### 5.6. Activation delay

A newly added validator **MUST NOT** participate in finalization until:

- an activation delay has passed (e.g., 7 days);
- the validator has synced the full ledger.

This prevents attackers from being added and immediately signing malicious events.

### 5.7. Initial validator set

At genesis, the initial validator set is defined in the genesis event or the first `validator.add` events.

For a new community:

- typically 3–5 founding validators;
- each is a trusted member;
- they bootstrap the ledger.

### 5.8. Validator set changes

Adding or removing a validator **MUST** be:

- recorded on-ledger;
- signed by an authorized identity;
- subject to the activation delay.

The current validator set is derived from the ledger.

### 5.9. Random selection (for audit and disputes)

For dispute resolution (see [contribution.md](./contribution.md#11-disputes)), auditors are selected randomly from the eligible pool.

Randomness **MUST** be deterministic:

- based on a verifiable random function (VRF) seeded by a recent checkpoint hash;
- or based on a deterministic hash of the dispute ID and the eligible pool.

**Example:**

```
seed = BLAKE3(dispute_id || latest_checkpoint_root)
auditors = sort_by(BLAKE3(seed || candidate_did))[:3]
```

This ensures all nodes pick the same auditors.

### 5.10. No validator cartel

Communities **SHOULD** discourage validator cartels:

- limit the number of validators from the same organization;
- require diversity (geography, affiliation);
- rotate regularly;
- allow easy removal.

### 5.11. Public list

The current validator set **MUST** be publicly queryable:

- via API (see [api.md](./api.md));
- via a `validator.list` query;
- in checkpoints.

---

## 6. Finalization

### 6.1. What finalization means

An event is **finalized** when it has been signed by enough validators.

Finalization is the protocol's guarantee that the event will not be reverted.

### 6.2. Finalization threshold

The threshold is typically **2/3** of the validator set:

```
threshold = ceil(2 * N / 3)
```

Where `N` is the number of validators.

Examples:

| N | Threshold |
|---|---|
| 3 | 2 |
| 5 | 4 |
| 7 | 5 |
| 10 | 7 |
| 15 | 10 |
| 21 | 14 |

### 6.3. Why 2/3

2/3 (or ⌈2N/3⌉) is a common Byzantine fault tolerance threshold:

- tolerates up to ⌊N/3⌋ faulty validators;
- ensures no two conflicting finalizations;
- is the threshold used in PBFT, Tendermint, and other BFT protocols.

### 6.4. Alternative thresholds

For some contexts, stricter thresholds **MAY** be used:

- **3/4** for high-security contexts;
- **1/2 + 1** for fast-finality contexts (with higher fork risk).

The threshold is defined in the context's rules.

### 6.5. Finalization scope

Finalization can be:

- **Per event** — each event is individually signed.
- **Per batch** — a batch of events is signed together.
- **Per checkpoint** — only checkpoints are signed; events are final when included in a signed checkpoint.

CL uses **per checkpoint** finalization for scalability:

- validators sign checkpoints (every 10 000 events or every 24 hours);
- events between checkpoints are pending until the next checkpoint.

This is efficient but introduces a finality delay.

### 6.6. Finality delay

Events between checkpoints are **pending** for up to:

- the checkpoint interval (e.g., 24 hours);
- or until a checkpoint is created (e.g., on demand).

Communities **MAY** create checkpoints more frequently (e.g., every hour) if faster finality is needed.

### 6.7. Immediate finalization

For critical events (e.g., rule changes, validator changes), validators **MAY** finalize immediately (outside the checkpoint cycle).

This is a community decision.

### 6.8. Reverting finalized events

Finalized events **MUST NOT** be reverted.

Exception: **fork** (Section 10). A community **MAY** fork the ledger, abandoning certain events. But this is a new ledger, not a modification of the old one.

### 6.9. Pending events

Pending events:

- are visible to nodes;
- contribute to **provisional** state;
- are not subject to slashing or penalties;
- can be reverted if they conflict with finalized events.

Clients **SHOULD** indicate whether a value is final or provisional.

### 6.10. Finalization of checkpoints

A checkpoint is finalized when:

- it is signed by the threshold of validators;
- the signatures are valid;
- the checkpoint's roots match the recomputed values.

Once finalized:

- the checkpoint is permanent;
- events included in it are final;
- the checkpoint is used for bootstrap.

### 6.11. Checkpoint signature collection

Checkpoint creation process:

1. Any node proposes a checkpoint (`checkpoint.propose`).
2. Validators verify the checkpoint (roots match).
3. Validators sign the checkpoint (`checkpoint.sign`).
4. When threshold is met, the checkpoint is final (`checkpoint.final`).

Alternative: checkpoint signatures are collected off-chain, and only the final signed checkpoint is published.

Both are valid. The choice is a community decision.

### 6.12. Checkpoint intervals

Recommended intervals:

| Community size | Interval |
|---|---|
| Small | 1 hour |
| Medium | 6 hours |
| Large | 24 hours |

Shorter intervals = faster finality = more overhead.

### 6.13. Missing validators

If some validators are offline:

- finalization continues if the threshold is still met;
- if the threshold is not met, finalization pauses;
- after a timeout, offline validators **MAY** be removed (Section 9).

### 6.14. Quorum failure

If finalization cannot proceed (quorum failure), the community has options:

- **Wait** for validators to return.
- **Remove** offline validators.
- **Fork** (Section 10) with a new validator set.

---

## 7. Finalization Process

### 7.1. Proposing a checkpoint

Any node **MAY** propose a checkpoint. The proposal includes:

- the event root;
- the state root;
- the height and depth;
- the context roots;
- the rules versions.

```json
{
  "type": "checkpoint.propose",
  "author": "did:cl:main:anyone",
  "payload": {
    "height": 100000,
    "depth": 50000,
    "event_root": "blake3:...",
    "state_root": "blake3:...",
    "context_roots": {...},
    "rules_versions": {...}
  }
}
```

### 7.2. Validator verification

Each validator:

1. Verifies the proposal's roots match their own computation.
2. Verifies the checkpoint includes all finalized events.
3. Signs the checkpoint if valid.

```json
{
  "type": "checkpoint.sign",
  "author": "did:cl:main:validator1",
  "payload": {
    "checkpoint_id": "blake3:...",
    "signature": "ed25519:..."
  }
}
```

### 7.3. Threshold

When ⌈2N/3⌉ signatures are collected:

- the checkpoint is final;
- a `checkpoint.final` event is created;
- the checkpoint is broadcast to the network.

```json
{
  "type": "checkpoint.final",
  "author": "did:cl:main:aggregator",
  "payload": {
    "checkpoint_id": "blake3:...",
    "signatures": [
      {"signer": "did:cl:main:validator1", "signature": "..."},
      ...
    ]
  }
}
```

### 7.4. Broadcasting

The finalized checkpoint is broadcast via gossip (see [sync.md](./sync.md)).

Nodes that receive it:

- verify the signatures;
- update their finality state;
- mark all events in the checkpoint as final.

### 7.5. Conflict detection

If a node receives two finalized checkpoints at the same height with different roots:

- it **MUST** alert (fork detected);
- it **MUST NOT** accept either until resolution (see Section 10);
- it **SHOULD** notify other nodes.

### 7.6. Aggregation

The checkpoint aggregation (collecting signatures) **MAY** be done:

- by a designated aggregator;
- by any node (permissionless);
- by validators themselves.

The aggregator is not a trusted role — the signatures are verified by recipients.

### 7.7. Timeouts

If a checkpoint is proposed but not finalized within a timeout (e.g., 24 hours):

- validators **SHOULD** investigate;
- the community **MAY** intervene.

### 7.8. Multiple concurrent proposals

Multiple checkpoints **MAY** be proposed in parallel. Validators sign the first valid one they see. This is fine — only one will meet the threshold.

If two meet the threshold at the same height (rare but possible), it is a fork (Section 10).

### 7.9. Incremental checkpointing

For large ledgers, checkpoints **MAY** be incremental:

- each checkpoint builds on the previous;
- only the delta is included;
- the state root is updated via delta application.

This is faster than recomputing from genesis.

### 7.10. Checkpoint storage

Finalized checkpoints **MUST** be stored in the ledger (as events) and **MAY** be:

- stored in a dedicated table;
- published to external storage (IPFS, Arweave);
- served via API for bootstrap.

---

## 8. Validator Rotation

### 8.1. Why rotate

- **Prevent entrenchment.** Long-serving validators may become complacent or corrupt.
- **Distribute power.** Rotation prevents any small group from dominating.
- **Bring in fresh validators.** New identities can earn a seat.
- **Test the system.** Regular changes ensure the ledger can handle rotation.

### 8.2. Rotation mechanisms

Three mechanisms:

1. **Scheduled rotation** — a fixed fraction rotates every N months.
2. **Election** — validators are elected for fixed terms.
3. **Continuous** — validators join and leave continuously based on rules.

CL supports all three. The community chooses.

### 8.3. Scheduled rotation

Example:

- every 6 months, 1/3 of validators are replaced;
- replacements are chosen by vote or random selection from eligible pool;
- outgoing validators may re-nominate (subject to term limits).

### 8.4. Election

Example:

- validators serve 12-month terms;
- elections are held every 12 months;
- all seats are up for election;
- top N candidates by vote (or reputation) become validators.

### 8.5. Continuous rotation

Example:

- any eligible identity may become a validator at any time;
- the validator set is capped at N;
- when a new validator joins and the set is full, the lowest-reputation validator is removed.

### 8.6. Term limits

Communities **MAY** set term limits:

- maximum consecutive terms;
- mandatory break after N terms;
- maximum total terms.

Term limits prevent entrenchment.

### 8.7. Rotation process

1. Rotation is triggered (time, vote, or condition).
2. Eligible candidates are identified.
3. New validators are selected (per the mechanism).
4. `validator.add` events are created.
5. Outgoing validators receive `validator.remove` events.
6. Activation delay for new validators.
7. Old validators finish their duties (sign any pending checkpoints).

### 8.8. Overlap

To avoid gaps, new validators are added **before** old ones are removed:

- both sets are active during the overlap period;
- finalization requires threshold from **all** active validators (including both sets).

This ensures continuity.

### 8.9. Rotation and checkpoints

A checkpoint signed by the pre-rotation set is valid. A checkpoint signed by the post-rotation set is valid.

A checkpoint signed by a mix is valid if the threshold is met across all active validators.

### 8.10. Forced rotation

If a validator:

- is offline for more than a threshold (e.g., 30 days);
- fails to sign N consecutive checkpoints;
- is proven to have equivocated;
- is removed by community vote;

then the validator is forcibly removed, and a replacement is added.

### 8.11. Random selection for rotation

For fairness, rotation **MAY** use random selection:

- eligible candidates are pooled;
- a deterministic random function picks replacements;
- randomness is seeded by a recent checkpoint hash.

This prevents organized capture of the validator set.

### 8.12. Rotation transparency

All rotation events **MUST** be recorded on-ledger:

- who was added;
- who was removed;
- why;
- when.

This makes rotation auditable.

---

## 9. Validator Removal

### 9.1. Reasons for removal

- **Voluntary** — validator chooses to leave.
- **Inactivity** — validator is offline for too long.
- **Equivocation** — validator signed conflicting checkpoints.
- **Censorship** — validator systematically refuses valid events.
- **Collusion** — validator colludes with others to alter state.
- **Community vote** — community decides to remove.
- **Term limit** — validator reached maximum term.

### 9.2. Voluntary removal

A validator **MAY** resign via a `validator.resign` event:

```json
{
  "type": "validator.resign",
  "author": "did:cl:main:validator1",
  "payload": {
    "context": "repo:x/y",
    "reason": "stepping down"
  }
}
```

The validator is removed after the current checkpoint is finalized.

### 9.3. Inactivity removal

A validator is **inactive** if it has not signed any checkpoint in the last N (e.g., 7) checkpoint intervals.

Inactive validators **MAY** be removed via a `validator.remove` event, signed by an authorized identity (admin, council).

### 9.4. Equivocation removal

**Equivocation** is signing two conflicting checkpoints at the same height.

Detection:

- any node receiving two signatures from the same validator at the same height **MUST** broadcast an `equivocation.proof` event;
- the proof includes both signed checkpoints.

Once proven, the validator:

- is immediately removed;
- loses reputation (large penalty);
- is barred from re-nomination for a period (e.g., 1 year).

### 9.5. Censorship removal

If a validator systematically refuses to sign valid events, the community **MAY** remove it via vote.

Evidence of censorship:

- multiple reports from users;
- comparison with other validators' signing patterns;
- refusal to sign valid checkpoints.

### 9.6. Collusion removal

If a group of validators colludes to:

- alter state;
- censor users;
- sign conflicting checkpoints;
- bypass rules;

then the community **MAY** remove them via vote, and if necessary, fork (Section 10).

### 9.7. Community vote removal

A vote **MAY** be opened to remove a validator:

```json
{
  "type": "vote.create",
  "payload": {
    "proposal": "remove_validator",
    "context": "repo:x/y",
    "options": ["yes", "no", "abstain"],
    "target": "did:cl:main:validator1"
  }
}
```

If the threshold is met, the validator is removed.

### 9.8. Removal process

1. Reason for removal is established.
2. A `validator.remove` event is created.
3. The event **MUST** be signed by an authorized identity.
4. The removed validator **MUST** finish signing any pending checkpoints.
5. After removal, the validator **MUST NOT** sign new checkpoints.
6. A replacement **MAY** be added.

### 9.9. Loss of validator status

After removal, the identity:

- loses the "validator" role in the context;
- retains its reputation (minus any penalty);
- may re-nominate after a period (if rules allow).

### 9.10. Permanent ban

In severe cases (e.g., proven collusion), the validator **MAY** be permanently banned:

- cannot re-nominate;
- reputation reduced;
- marked in the ledger.

A permanent ban **MUST** require a high threshold (e.g., 3/4 of members).

---

## 10. Forks

### 10.1. What is a fork

A **fork** is a divergence in the ledger:

- two different sets of events;
- two different states;
- two different histories.

Forks happen when:

- validators disagree;
- the community splits;
- a malicious group attempts to alter history.

### 10.2. Types of forks

| Type | Cause | Resolution |
|---|---|---|
| **Accidental fork** | Network partition, simultaneous checkpoints | Merge if possible |
| **Contentious fork** | Disagreement on rules | Community vote, or split |
| **Malicious fork** | Attack by validators | Reject minority fork |
| **Voluntary fork** | Community decides to split | Both forks continue independently |

### 10.3. Accidental forks

If two checkpoints are finalized at the same height (rare), nodes **MUST**:

1. Detect the conflict.
2. Pause finalization.
3. Attempt to reconcile (e.g., by producing a new checkpoint that includes both).

If reconciliation is not possible, see contentious fork.

### 10.4. Contentious forks

If the community disagrees on a rule change:

- a vote is held;
- if the vote is close or contested, a fork **MAY** occur;
- each side continues with its own rules;
- both ledgers are valid for their respective communities.

This is **not** a failure — it is a feature. Communities are sovereign.

### 10.5. Malicious forks

If a small group of validators attempts to fork maliciously:

- the majority continues with the original ledger;
- the malicious fork is ignored;
- the malicious validators are removed (Section 9).

### 10.6. Voluntary fork

A community **MAY** decide to fork voluntarily:

- to change fundamental rules;
- to escape capture;
- to experiment with new features.

Procedure:

1. Announce the intent to fork.
2. Specify the fork point (a specific checkpoint).
3. Publish the new rules.
4. Continue the ledger from the fork point with new rules.
5. Members choose which fork to follow.

### 10.7. Fork declaration

A fork is declared via a `fork.declare` event:

```json
{
  "type": "fork.declare",
  "author": "did:cl:main:anyone",
  "payload": {
    "fork_point": "blake3:...",       // checkpoint ID
    "reason": "rule_disagreement",
    "new_rules": {...},
    "new_validators": [...]
  }
}
```

### 10.8. Fork and identity

Identities exist in both forks after the fork point.

- The same DID may act in both forks (unusual but possible).
- Or the identity may choose one fork.

Reputation is **fork-specific** after the fork.

### 10.9. Fork and data

Data before the fork point is shared between forks.

Data after the fork point diverges.

Nodes **MAY** follow both forks or only one.

### 10.10. Fork resolution

If a fork is accidental or malicious, resolution is:

- majority rules (the fork with more signatures wins);
- or the community votes.

If a fork is voluntary, there is no "resolution" — both continue.

### 10.11. Right to fork

Any community **MAY** fork at any time. This is a fundamental right.

Forking is not blocked by the protocol. It is a natural mechanism for disagreement.

### 10.12. Fork economics

Forking has costs:

- duplicated infrastructure;
- split community;
- loss of network effects.

The protocol does not subsidize or prevent forks. They are a community choice.

---

## 11. Federation

### 11.1. What is federation

**Federation** is the interoperability of multiple ledgers. Each ledger has its own validators and rules, but they can:

- exchange attestations;
- recognize each other's contributions;
- create shared spaces;
- remain independent.

### 11.2. Federation vs. single ledger

A single global ledger would have:

- one validator set;
- one rule set;
- one community.

Federation:

- multiple validator sets;
- multiple rule sets;
- multiple communities;
- interoperability between them.

Federation is more flexible but requires more trust management.

### 11.3. Federation models

| Model | Description |
|---|---|
| **Isolated** | Ledgers do not interact. |
| **Attestation-only** | Ledgers exchange attestations but do not share reputation. |
| **Reputation recognition** | Ledgers recognize each other's reputation with weights and caps. |
| **Shared contexts** | Some contexts span multiple ledgers. |
| **Merged** | Ledgers merge into one. |

CL supports all models.

### 11.4. Isolated ledgers

Two ledgers do not interact. Each has its own rules and reputation.

This is the default. It requires no cross-ledger coordination.

### 11.5. Attestation-only

Ledgers exchange attestations:

- an identity in ledger A is attested by an organization in ledger B;
- the attestation is visible in ledger A.

Attestations do not transfer reputation. They only confirm claims.

### 11.6. Reputation recognition

Ledger A recognizes reputation from ledger B:

- `A` includes in its rules a recognition of `B`;
- weight and cap are applied (see [reputation.md](./reputation.md#8-aggregation-across-contexts)).

This is explicit, not automatic.

### 11.7. Shared contexts

Two ledgers agree to share a context:

- contributions in the shared context are visible in both;
- reputation in the shared context is shared;
- validators from both ledgers participate in finalization.

This is the most complex federation model.

### 11.8. Merged ledgers

Two ledgers merge into one:

- both histories are preserved;
- one validator set is chosen;
- one rule set is chosen.

Merging is a rare event, typically after a fork reverses.

### 11.9. Cross-ledger references

Events in one ledger **MAY** reference events in another:

```json
{
  "type": "contribution.create",
  "payload": {
    "context": "cross:ledgerA/ledgerB",
    "external_refs": [
      {"ledger": "ledgerA", "event_id": "blake3:..."}
    ]
  }
}
```

The reference is a hint; verification requires access to the other ledger.

### 11.10. Cross-ledger verification

To verify a cross-ledger reference:

1. The node must have access to the other ledger.
2. The referenced event **MUST** exist and be finalized in the other ledger.
3. The reference **MUST** be included in the local event's payload.

If the other ledger is not accessible, the reference is treated as unverified (not invalid).

### 11.11. Federation agreements

Federation **MUST** be explicit. Two ledgers **MUST** have an agreement (recorded in each ledger's rules) to recognize each other.

Unilateral recognition is possible (one ledger recognizes another without reciprocation), but it is asymmetric.

### 11.12. Federation disputes

If two ledgers disagree on a cross-ledger event:

- each ledger resolves per its own rules;
- the disagreement is visible in the rules;
- members choose which ledger's interpretation they trust.

### 11.13. Federation and identity

An identity **MAY** exist in multiple ledgers:

- same DID (if the ledgers support it);
- different DIDs (linked via attestations).

Cross-ledger identity linking is optional.

### 11.14. Federation and reputation

Reputation is context-specific. A context may be:

- local to one ledger;
- shared across ledgers.

Shared contexts require agreement on:
- rules;
- validators;
- reputation formula;
- thresholds.

---

## 12. Cross-Ledger Consensus

### 12.1. The problem

When two ledgers share a context, how is consensus reached?

Options:

1. **Single ledger owns the context.** Other ledgers treat it as read-only.
2. **Joint validator set.** Validators from both ledgers sign.
3. **Two-phase commit.** Each ledger finalizes locally, then cross-signs.
4. **Optimistic.** Each ledger finalizes locally; conflicts are resolved later.

### 12.2. Single-ledger ownership

The simplest model:

- the context lives in one ledger;
- other ledgers reference it read-only;
- no cross-ledger consensus needed.

### 12.3. Joint validator set

For shared contexts:

- the validator set is the union of validators from both ledgers;
- finalization requires threshold from the union;
- a checkpoint is valid only if signed by both sides.

This is secure but slow.

### 12.4. Two-phase commit

Each ledger:

1. Proposes a checkpoint locally.
2. Shares it with the other ledger.
3. Waits for the other ledger's acknowledgment.
4. Finalizes only after both sides agree.

This ensures consistency but can deadlock if one side is unavailable.

### 12.5. Optimistic

Each ledger finalizes locally. Conflicts are detected and resolved later.

This is fast but requires conflict resolution.

### 12.6. Recommended model

For most cases, **single-ledger ownership** is best:

- simple;
- fast;
- no cross-ledger consensus complexity.

Shared contexts are used only when necessary.

### 12.7. Cross-ledger checkpoint format

If cross-ledger consensus is used, the checkpoint includes signatures from both ledgers:

```json
{
  "type": "checkpoint",
  "payload": {
    "height": 100000,
    "event_root": "blake3:...",
    "state_root": "blake3:...",
    "ledger_signatures": {
      "ledgerA": [...],
      "ledgerB": [...]
    }
  }
}
```

Both sides' thresholds **MUST** be met.

### 12.8. Cross-ledger disputes

If ledgers disagree on a cross-ledger checkpoint:

- the checkpoint is invalid on both sides;
- a new checkpoint is proposed;
- if disagreement persists, the shared context is split.

### 12.9. Cross-ledger security

The security of cross-ledger consensus is the **minimum** of both ledgers' security.

If one ledger has faulty validators, the shared context is at risk.

This is why shared contexts require high trust between ledgers.

---

## 13. Security Model

### 13.1. Assumptions

CL's consensus assumes:

- **Honest majority.** At least ⌈2N/3⌉ validators are honest.
- **Synchrony (partial).** Messages arrive within a bounded time (most of the time).
- **Cryptographic security.** Ed25519 and BLAKE3 are secure.
- **No long-range attacks.** Validators' private keys are not compromised.
- **Public verifiability.** All events and signatures are public.

### 13.2. What CL does not assume

- **Economic rationality.** Validators are not assumed to be rational profit-maximizers (there is no profit).
- **Permissionlessness.** Validators are known identities.
- **Anonymity.** Validators are public.

### 13.3. Threats

| Threat | Defense |
|---|---|
| Byzantine validators | 2/3 threshold |
| Censorship | Multiple validators, fork |
| Collusion | Rotation, removal, fork |
| Equivocation | Detection and slashing |
| Sybil attack | Attestation, reputation |
| DoS | Rate limits, network design |
| Long-range attack | Finality checkpoints |
| Rule change attack | Vote threshold |

### 13.4. Byzantine fault tolerance

CL tolerates up to ⌊N/3⌋ Byzantine validators.

With 7 validators, up to 2 can be faulty.

If more than ⌊N/3⌋ are faulty:

- safety may be compromised (conflicting checkpoints);
- liveness may fail (no finalization).

The community must intervene (fork, remove validators).

### 13.5. Liveness

If at least ⌈2N/3⌉ validators are online, finalization proceeds.

If fewer are online:

- finalization pauses;
- the community may remove offline validators;
- or fork.

### 13.6. Safety

If fewer than ⌈2N/3⌉ validators sign a checkpoint, it is not finalized.

This prevents conflicting finalization.

### 13.7. Griefing

A malicious validator can:

- slow finalization by not signing;
- force repeated checkpoint proposals.

Mitigations:

- timeout-based removal;
- rotation;
- reputation penalty.

### 13.8. Collusion

If ⌈2N/3⌉ validators collude, they can:

- finalize invalid events;
- censor users;
- alter state.

Mitigations:

- community vote to remove colluders;
- fork to a new validator set;
- slashing (reputation).

Collusion of a supermajority is the worst-case scenario. The only defense is the community's right to fork.

### 13.9. Long-range attacks

If a validator's private key is compromised, an attacker could sign conflicting checkpoints.

Mitigations:

- key rotation (see [identity.md](./identity.md#9-key-rotation));
- finality checkpoints (once finalized, an event is permanent);
- community notification.

### 13.10. Sybil attacks

An attacker creates many identities to influence votes.

Mitigations:

- attestations (Level 2+);
- reputation thresholds;
- quadratic voting (see [vote.md](./vote.md));
- graph analysis.

### 13.11. Censorship resistance

A single validator cannot censor events — others will sign.

If a majority censors, the community can:

- fork;
- remove validators;
- run its own ledger.

### 13.12. Quantum threats

If quantum computers break Ed25519 or BLAKE3:

- the protocol will need to migrate;
- the migration is an RFC;
- in the meantime, the community decides.

This is a future concern, not a current one.

---

## 14. Validation Rules

Validators **MUST** enforce these rules.

### 14.1. Validator set

- The current validator set is derived from the ledger.
- A validator **MUST** be a Level 2+ identity.
- A validator **MUST** be approved per the community's rules.
- A validator **MUST** observe the activation delay.

### 14.2. Finalization

- A checkpoint **MUST** be signed by ⌈2N/3⌉ validators.
- Signatures **MUST** be valid.
- Signers **MUST** be in the active validator set at the checkpoint's time.
- The checkpoint's roots **MUST** match the recomputed values.

### 14.3. Rotation

- Rotation events **MUST** be authorized.
- New validators **MUST** observe activation delay.
- Removed validators **MUST NOT** sign new checkpoints.

### 14.4. Equivocation

- Two conflicting checkpoints at the same height **MUST** be flagged.
- The validator(s) that signed both **MUST** be reported.
- The report **MUST** include both signed checkpoints.

### 14.5. Forks

- A fork **MUST** be declared explicitly.
- The fork point **MUST** be a valid checkpoint.
- Members **MAY** choose which fork to follow.

### 14.6. Federation

- Recognition **MUST** be explicit in rules.
- Cross-ledger references **MUST** be verifiable (if the other ledger is available).
- Shared contexts **MUST** have agreements in both ledgers.

### 14.7. Finalization and sync

- Finalized checkpoints **MUST** be propagated to all nodes.
- Nodes **MUST** update their finality state upon receiving a valid checkpoint.
- Nodes **MUST** reject invalid checkpoints.

---

## 15. Examples

### 15.1. Validator set change

Community `repo:x/y` has 7 validators. One resigns, one is added.

**Before:**

- Validators: V1, V2, V3, V4, V5, V6, V7.
- Threshold: ⌈2×7/3⌉ = 5.

**Events:**

1. `validator.resign` by V7.
2. `validator.add` for V8.
3. `validator.remove` for V7 (after overlap).

**After:**

- Validators: V1, V2, V3, V4, V5, V6, V8.
- Threshold: ⌈2×7/3⌉ = 5.

### 15.2. Checkpoint finalization

1. Node A proposes checkpoint at height 100000.
2. Validators V1–V7 verify the checkpoint.
3. V1, V2, V3, V4, V5 sign it (5 signatures).
4. Threshold met (5 of 7).
5. Checkpoint is final.
6. Broadcast to network.

### 15.3. Equivocation

Validator V3 signs two checkpoints at height 100000 with different roots.

Node B receives both.

Node B broadcasts `equivocation.proof` with both signed checkpoints.

Community removes V3. V3's reputation is slashed.

### 15.4. Fork

Community `repo:x/y` disagrees on a rule change.

- 60% want change A.
- 40% want change B.

They agree to fork:

- fork point: checkpoint at height 50000.
- Side A continues with change A and its validators.
- Side B continues with change B and its validators.

Both ledgers are valid for their communities.

### 15.5. Federation

Ledger A (open-source project) and Ledger B (research lab) federate.

Ledger A's context `repo:x/y` recognizes:
- Ledger B's context `lab:research` with weight 0.5, cap 500.

A contributor with reputation 800 in Ledger B has:
- reputation recognized in Ledger A: 0.5 × min(800, 500) = 250.

### 15.6. Cross-ledger shared context

Ledger A and Ledger B share context `cross:climate`.

- Validators from both ledgers sign checkpoints.
- Contributions in the shared context count for both ledgers.
- Reputation is shared.

### 15.7. Validator inactivity

Validator V4 does not sign any checkpoint for 30 days.

Community opens a vote. Vote passes.

`validator.remove` for V4 is created.

V4 is removed. V8 is added as replacement.

---

## 16. Test Vectors

Test vectors for consensus live in `spec/test-vectors/consensus.json`.

### 16.1. Coverage

- Validator set derivation from events.
- Finalization threshold computation.
- Checkpoint signature verification.
- Equivocation detection.
- Rotation events.
- Fork declaration.
- Federation recognition.
- Cross-ledger references.
- Invalid cases: insufficient signatures, unknown validators, conflicting checkpoints.

### 16.2. Format

```json
{
  "description": "Finalization with 7 validators, 5 signatures",
  "validators": ["V1", ..., "V7"],
  "checkpoint": {...},
  "signatures": ["sig1", ..., "sig5"],
  "expected": "finalized"
}
```

### 16.3. Determinism

All computations **MUST** be deterministic:

- validator set derivation;
- threshold computation;
- signature verification;
- fork detection.

### 16.4. Cross-implementation

Test vectors **MUST** pass on at least two implementations before v1.0.

---

## 17. Open Questions

- Should finalization be **per checkpoint** or **per event**?
- What is the optimal **checkpoint interval**?
- How to handle **validator set changes mid-checkpoint**?
- Should there be a **minimum validator set size**?
- How to handle **rotating validators** without disrupting finality?
- Should **federation** have a standard protocol, or is it ad hoc?
- How to handle **cross-ledger forks**?
- Should **shared contexts** be a protocol feature or an application-level convention?
- How to prevent **validator cartels**?
- Should there be **slashing** for validator misbehavior?
- How to handle **quantum threats**?
- Should there be a **maximum term** for validators?
- How to handle **disputes over finality**?
- Should **light clients** trust checkpoints by default?
- How to handle **long-range attacks** without slashing?

These will be resolved through RFCs and community discussion.

---

## Summary

**Consensus is:**

- Federated (per community).
- Reputation-based (not token-based).
- Explicit (finalization via signatures).
- Rotatable (validators change).
- Forkable (communities can split).

**Validator model:**

- Level 2+ identities.
- Chosen by community.
- No token, no stake, no mining.
- Accountable (removable).

**Finalization:**

- Threshold: ⌈2N/3⌉.
- Per checkpoint.
- Signed by validators.
- Broadcast to network.

**Rotation:**

- Scheduled, elected, or continuous.
- Term limits optional.
- Overlap during transitions.

**Removal:**

- Voluntary, inactivity, equivocation, censorship, collusion, vote.
- Permanent bans for severe cases.

**Forks:**

- Accidental, contentious, malicious, voluntary.
- Right to fork is fundamental.
- Both forks can continue.

**Federation:**

- Isolated, attestation-only, reputation recognition, shared contexts, merged.
- Explicit agreements.

**Security:**

- Byzantine fault tolerance up to ⌊N/3⌋.
- Fork as last resort.
- Community as ultimate authority.

**Key insight:**

CL's consensus is **political**, not mathematical. The math (signatures, thresholds) is simple. The politics (who validates, who decides, who forks) is where the real complexity lives.

The protocol provides tools. Communities use them.

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [identity.md](./identity.md) — identity model.
- [ledger.md](./ledger.md) — DAG, checkpoints.
- [reputation.md](./reputation.md) — reputation (basis for validator selection).
- [sync.md](./sync.md) — P2P synchronization.
- [vote.md](./vote.md) — governance votes.
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
