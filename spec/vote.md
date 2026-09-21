# Vote

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md) · [identity.md](./identity.md) · [contribution.md](./contribution.md) · [reputation.md](./reputation.md) · [consensus.md](./consensus.md)  
**Related:** [bounty.md](./bounty.md) · [privacy.md](./privacy.md) · [api.md](./api.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [Vote Types](#3-vote-types)
4. [Vote Creation](#4-vote-creation)
5. [Eligibility](#5-eligibility)
6. [Voting Power](#6-voting-power)
7. [Casting a Vote](#7-casting-a-vote)
8. [Delegation](#8-delegation)
9. [Tallying](#9-tallying)
10. [Secret Voting (ZK)](#10-secret-voting-zk)
11. [Veto and Minority Protection](#11-veto-and-minority-protection)
12. [Finalization](#12-finalization)
13. [Disputes and Appeals](#13-disputes-and-appeals)
14. [Validation Rules](#14-validation-rules)
15. [Examples](#15-examples)
16. [Test Vectors](#16-test-vectors)
17. [Open Questions](#17-open-questions)

---

## 1. Overview

**Voting** is how communities in CL make collective decisions. It is used for:

- rule changes;
- validator selection and removal;
- role grants and revocations;
- budget allocation;
- dispute resolution (as fallback);
- forks;
- any other decision the community delegates to a vote.

Voting in CL is **not** token-based. There is no "1 token = 1 vote." Instead:

- voting power comes from **reputation**;
- power is **quadratic** (√reputation), not linear;
- reputation **cannot be bought**;
- delegation is possible, but does not transfer reputation;
- secret voting is possible via zero-knowledge proofs.

**This file defines:**

- The types of votes (Section 3).
- How votes are created (Section 4).
- Who can vote (Section 5).
- How voting power is computed (Section 6).
- How votes are cast (Section 7).
- How delegation works (Section 8).
- How votes are tallied (Section 9).
- How secret voting works (Section 10).
- Veto and minority protection (Section 11).
- Finalization (Section 12).
- Disputes and appeals (Section 13).
- Validation rules (Section 14).

Voting is the political core of CL. The math is simple. The social dynamics are not.

---

## 2. Design Principles

### 2.1. Reputation, not money

Voting power comes from **reputation**, not from token holdings, not from stake, not from payment.

This means:

- you cannot buy votes;
- you cannot rent votes;
- you cannot borrow votes;
- you cannot inherit votes.

Reputation is earned by contribution (see [reputation.md](./reputation.md)).

### 2.2. Quadratic, not linear

Voting power is `√reputation`, not `reputation`.

This means:

- doubling reputation gives 1.41× more power, not 2×;
- accumulating power is expensive;
- small participants have meaningful weight;
- whales cannot dominate.

### 2.3. Contextual

Voting power is computed **per context**. Reputation in one context does not grant voting power in another (unless recognized — see [reputation.md](./reputation.md#8-aggregation-across-contexts)).

### 2.4. Snapshot-based

Voting power is frozen at the moment the vote is created (**snapshot**). Changes to reputation during the vote do not affect the outcome.

This prevents:

- last-minute reputation farming;
- manipulation by transfers;
- gaming during the vote window.

### 2.5. Transparent by default

By default, votes are **public**: anyone can see who voted and how.

Secret voting is possible (Section 10), but it is opt-in and requires ZK proofs.

### 2.6. Delegation without transfer

A voter **MAY** delegate their vote to another identity. Delegation:

- transfers **voting power**, not reputation;
- is temporary;
- is revocable;
- is recorded on-ledger.

Delegation does not allow vote-buying. You can delegate to anyone, but you cannot sell your vote for money (see Section 8.9).

### 2.7. Multiple thresholds

Different decisions require different thresholds:

- simple majority (> 50%);
- qualified majority (2/3);
- supermajority (3/4 or 90%);
- consensus (near-unanimous).

The threshold is set when the vote is created.

### 2.8. Minority protection

Minorities have protections:

- **veto** for constitutional changes (Section 11);
- **appeals** for contested decisions (Section 13);
- **fork rights** for fundamental disagreements (see [consensus.md](./consensus.md#10-forks)).

### 2.9. One vote per identity

An identity **MUST NOT** vote more than once per vote. Multiple votes from the same identity are invalid.

### 2.10. Deterministic tallying

Given the same set of votes and the same snapshot, every node **MUST** compute the same result.

---

## 3. Vote Types

### 3.1. By decision

| Type | Purpose |
|---|---|
| `rule_change` | Change context rules. |
| `validator_add` | Add a validator. |
| `validator_remove` | Remove a validator. |
| `role_grant` | Grant a role. |
| `role_revoke` | Revoke a role. |
| `budget` | Allocate funds. |
| `grant` | Approve a grant. |
| `dispute_appeal` | Appeal a dispute decision. |
| `fork` | Declare a fork. |
| `custom` | Community-defined. |

### 3.2. By options

| Type | Options |
|---|---|
| **Binary** | `yes`, `no`, `abstain` |
| **Multi-option** | Custom list |
| **Ranked** | Ranked choice |
| **Approval** | Multiple selections |
| **Quadratic allocation** | Distribute voice credits |

Most votes are binary. Multi-option is common for elections.

### 3.3. By threshold

| Type | Threshold |
|---|---|
| Simple majority | > 50% |
| Qualified | ≥ 2/3 |
| Supermajority | ≥ 3/4 |
| Consensus | ≥ 90% |
| Unanimous | 100% |

Thresholds are counted over **votes cast**, not over all eligible voters.

Abstentions do not count toward the threshold (unless specified).

### 3.4. By visibility

| Type | Visibility |
|---|---|
| **Public** | Votes and choices visible. |
| **Secret** | Votes visible, choices hidden (ZK). |
| **Anonymous** | Voters hidden (rare). |

Default: public.

### 3.5. By duration

| Type | Duration |
|---|---|
| **Short** | 1–3 days |
| **Standard** | 7 days |
| **Long** | 14–30 days |
| **Conditional** | Until threshold is reached |

Duration is set at creation. Deadlines are absolute timestamps.

### 3.6. By weight

| Type | Weight |
|---|---|
| **Simple** | 1 voter = 1 vote |
| **Reputation-weighted** | Weight = reputation |
| **Quadratic** | Weight = √reputation |
| **Delegated** | Weight includes delegated power |

Default: quadratic.

### 3.7. Custom types

Communities **MAY** define custom vote types. They **MUST** specify:

- the decision;
- the options;
- the threshold;
- the visibility;
- the duration;
- the weight method.

Custom types are recorded in the context's rules.

---

## 4. Vote Creation

### 4.1. Prerequisites

To create a vote, the creator **MUST**:

- be a member of the context;
- have reputation ≥ the context's `vote_create_threshold` (e.g., 100);
- provide a clear proposal.

### 4.2. Vote creation event

```json
{
  "version": 1,
  "type": "vote.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "proposal": "change_weight_code_review",
    "context": "repo:github.com/x/y",
    "description": "Increase code review weight from 2 to 3.",
    "options": ["yes", "no", "abstain"],
    "threshold": "2/3",
    "weighting": "quadratic",
    "deadline": 1730100000,
    "snapshot": "blake3:...",
    "quorum": 0.1,
    "veto_required": false,
    "target": "rules.weights.review"
  },
  "signature": "ed25519:..."
}
```

### 4.3. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `proposal` | string | MUST | Short identifier for the proposal. |
| `context` | string | MUST | The context of the vote. |
| `description` | string | SHOULD | Human-readable description. |
| `options` | array | MUST | Voting options. |
| `threshold` | string | MUST | Required threshold (e.g., "2/3"). |
| `weighting` | string | MUST | `simple`, `linear`, `quadratic`, `delegated`. |
| `deadline` | integer | MUST | Unix timestamp. |
| `snapshot` | string | MUST | Hash of the reputation state at creation. |
| `quorum` | float | MAY | Minimum participation (0.0–1.0). |
| `veto_required` | boolean | MAY | Whether veto applies. |
| `target` | string | MAY | What the vote changes. |

### 4.4. Options

Options are strings. The first option is the default "yes" if not specified.

Common options:

- `["yes", "no", "abstain"]`
- `["approve", "reject"]`
- `["alice", "bob", "carol"]`

Options **MUST NOT** be empty. Duplicate options are invalid.

### 4.5. Threshold

Threshold is specified as a string:

| Value | Meaning |
|---|---|
| `"1/2"` | Simple majority (> 50%) |
| `"1/2+"` | Strictly more than 50% |
| `"2/3"` | At least 2/3 |
| `"3/4"` | At least 3/4 |
| `"90%"` | At least 90% |
| `"unanimous"` | 100% |

The threshold applies to the winning option's share of **votes cast**.

### 4.6. Weighting

| Value | Meaning |
|---|---|
| `simple` | 1 voter = 1 vote |
| `linear` | Weight = reputation |
| `quadratic` | Weight = √reputation |
| `delegated` | Weight includes delegated power |

Default: `quadratic`.

### 4.7. Snapshot

The `snapshot` is a hash of the reputation state at the vote's creation time.

It is used to:

- freeze voting power;
- prevent manipulation;
- allow verification.

The snapshot **MUST** reference a checkpoint or a state root computed from events before `vote.create`.

See [reputation.md](./reputation.md#10-snapshots) for snapshot format.

### 4.8. Quorum

Quorum is the minimum participation required for the vote to be valid.

Specified as a fraction of total eligible voting power (0.0–1.0).

Example: `quorum = 0.1` means at least 10% of eligible voting power must participate.

If quorum is not met by the deadline, the vote fails (regardless of outcome).

### 4.9. Veto

If `veto_required = true`, a minority of sufficient size can veto the outcome.

See Section 11 for details.

### 4.10. Target

The `target` field specifies what the vote affects. Examples:

- `"rules.weights.review"` — a specific rule.
- `"validator:did:cl:main:validator1"` — a specific validator.
- `"grant:12345"` — a specific grant.
- `"fork"` — a fork declaration.

Contexts **MAY** define their own target formats.

### 4.11. Validation

On creation:

- The context **MUST** exist.
- The creator **MUST** meet `vote_create_threshold`.
- The options **MUST** be non-empty.
- The threshold **MUST** be valid.
- The deadline **MUST** be in the future.
- The snapshot **MUST** be a valid state root.

### 4.12. Vote ID

The vote ID is the event ID of the `vote.create` event.

### 4.13. Vote state

A vote is `open` from creation until the deadline.

After the deadline, it is `closed`. After tallying, it is `finalized`.

### 4.14. Vote duplication

Only one vote with the same `proposal` and `context` **MAY** be open at a time.

If a vote is already open for the same proposal, a new `vote.create` is rejected (or replaces the old, per context rules).

### 4.15. Vote cancellation

A vote **MAY** be cancelled before any votes are cast:

```json
{
  "type": "vote.cancel",
  "author": "did:cl:main:alice",
  "payload": {
    "vote_id": "blake3:...",
    "reason": "typo_in_proposal"
  }
}
```

After votes are cast, cancellation requires a new vote.

### 4.16. Vote update

A vote **MUST NOT** be modified after creation. Any change requires a new vote.

---

## 5. Eligibility

### 5.1. Who can vote

To vote, an identity **MUST**:

- be a member of the context;
- have reputation > 0 in the context (at snapshot time);
- be Level 1+ (for most votes);
- not be barred by context rules.

### 5.2. Membership

Membership is context-specific. It **MUST** be defined by:

- explicit join (`community.join`);
- invitation;
- attestation;
- reputation threshold.

### 5.3. Reputation threshold

Contexts **MAY** require a minimum reputation to vote:

```json
"vote_eligibility": {
  "min_reputation": 10,
  "min_level": 1
}
```

If not specified, defaults apply:

- `min_reputation`: 1
- `min_level`: 1

### 5.4. Snapshot eligibility

Eligibility is determined by the **snapshot**, not by current state.

An identity eligible at snapshot time **MAY** vote, even if it loses reputation later.

An identity not eligible at snapshot time **MUST NOT** vote, even if it gains reputation later.

### 5.5. Multiple identities

An identity **MAY** have multiple DIDs, but each DID votes separately.

**Sybil prevention:**

- contexts **MAY** require attestations for voting;
- contexts **MAY** cap the total voting power per linked identity group;
- graph analysis **MAY** detect suspicious patterns.

### 5.6. Voting power at snapshot

Voting power is computed from the snapshot:

```
power(u) = f(reputation(u, context, snapshot_time))
```

Where `f` is the weighting function (Section 6).

### 5.7. No voting power = no vote

An identity with zero voting power **MAY** still cast a vote (it counts as abstain).

This is intentional: it allows expression without affecting the outcome.

### 5.8. Abstention

Abstaining is a valid vote. It:

- counts toward quorum;
- does not count toward the threshold for any option.

---

## 6. Voting Power

### 6.1. Weighting functions

The three weighting functions:

**Simple:**
```
power(u) = 1 if eligible, 0 otherwise
```

**Linear:**
```
power(u) = reputation(u, context, snapshot_time)
```

**Quadratic:**
```
power(u) = sqrt(reputation(u, context, snapshot_time))
```

### 6.2. Quadratic formula

Quadratic voting power is:

```
power(u) = sqrt(R)
```

Where `R` is the identity's reputation in the context at snapshot time.

Examples:

| Reputation | Power (√R) |
|---|---|
| 1 | 1.000 |
| 4 | 2.000 |
| 9 | 3.000 |
| 100 | 10.000 |
| 400 | 20.000 |
| 1000 | 31.623 |
| 10000 | 100.000 |

### 6.3. Rationale

Quadratic weighting:

- reduces whale dominance;
- makes power accumulation sub-linear;
- encourages broad participation;
- aligns with "1 person, 1 vote" more than linear weighting.

### 6.4. Precision

Voting power **MUST** be computed with **6 decimal places**.

Rounding: round half to even.

### 6.5. Total voting power

The total voting power of the context is:

```
total_power = Σ_u power(u)
```

Over all eligible identities.

### 6.6. Share of vote

A voter's share of the vote is:

```
share(u) = power(u) / total_power
```

### 6.7. Delegated power

If a voter has delegated power:

```
power(u) = own_power(u) + Σ_v delegated_power(v → u)
```

Where `v` are identities that delegated to `u`.

Delegated power is also quadratic (see Section 8).

### 6.8. Cap on power

Contexts **MAY** cap the maximum voting power per identity:

```json
"max_voting_power": 100.0
```

This prevents any single identity from dominating.

### 6.9. Cap on delegated power

Contexts **MAY** cap delegated power:

```json
"max_delegated_power": 200.0
```

This prevents delegation chains from concentrating power.

### 6.10. Minimum power for validity

A vote with total power below a minimum **MAY** be invalid:

```json
"min_total_power": 10.0
```

This prevents "votes" with no real participation.

---

## 7. Casting a Vote

### 7.1. Vote cast event

```json
{
  "version": 1,
  "type": "vote.cast",
  "author": "did:cl:main:bob",
  "created_at": 1730050000,
  "parents": ["blake3:..."],
  "payload": {
    "vote_id": "blake3:...",
    "option": "yes",
    "comment": "I support this change."
  },
  "signature": "ed25519:..."
}
```

### 7.2. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `vote_id` | string | MUST | The vote event ID. |
| `option` | string | MUST | One of the vote's options. |
| `comment` | string | MAY | Explanation (public). |
| `weight_proof` | string | MAY | ZK proof for secret voting. |

### 7.3. Rules

- The vote **MUST** be `open`.
- The voter **MUST** be eligible at snapshot time.
- The option **MUST** be one of the vote's options.
- The voter **MUST NOT** have already voted.
- The vote **MUST** be before the deadline.

### 7.4. Deadline

Votes cast after the deadline **MUST** be rejected.

Clock skew: votes within 5 minutes after the deadline are **MAY** accepted (configurable).

### 7.5. Multiple votes

An identity **MUST NOT** vote more than once. If multiple `vote.cast` events from the same identity exist for the same vote:

- only the first (by canonical order) is valid;
- subsequent votes are rejected.

### 7.6. Changing a vote

A voter **MUST NOT** change their vote after casting it.

Exception: contexts **MAY** allow vote changes via a `vote.change` event, which supersedes the earlier vote. If allowed, the latest vote wins.

### 7.7. Vote withdrawal

A voter **MAY** withdraw their vote:

```json
{
  "type": "vote.withdraw",
  "author": "did:cl:main:bob",
  "payload": {
    "vote_id": "blake3:..."
  }
}
```

Effects:

- the vote is removed from the tally;
- the voter's power is no longer counted;
- the withdrawal counts as participation for quorum (configurable).

### 7.8. Comment

Comments are public (unless secret voting). They are stored on-ledger and visible to all.

Comments **MUST NOT** contain personal data or illegal content.

### 7.9. Vote receipt

A voter **MAY** receive a receipt (a signed confirmation that their vote was recorded).

The receipt is not required by the protocol but is useful for verification.

---

## 8. Delegation

### 8.1. Purpose

Delegation allows:

- experts to represent others;
- inactive members to lend their power;
- smaller voices to concentrate for impact.

Delegation does **not** transfer reputation, only voting power.

### 8.2. Delegate event

```json
{
  "version": 1,
  "type": "vote.delegate",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "delegate": "did:cl:main:bob",
    "context": "repo:github.com/x/y",
    "until": 1760000000,
    "scope": ["budget", "rule_change"]
  },
  "signature": "ed25519:..."
}
```

### 8.3. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `delegate` | string (DID) | MUST | The identity receiving delegated power. |
| `context` | string | MUST | The context of the delegation. |
| `until` | integer | MAY | Unix timestamp; delegation expires. |
| `scope` | array | MAY | What types of votes the delegation applies to. |

### 8.4. Rules

- The delegator **MUST** be a member of the context.
- The delegate **MUST** be a member of the context.
- The delegate **MUST NOT** be the delegator.
- The delegate **MUST** have reputation > 0.
- The delegation **MUST NOT** create a cycle.

### 8.5. Cycle prevention

If Alice delegates to Bob and Bob delegates to Alice, this is a cycle.

Cycles **MUST** be rejected. Detection: build a directed graph of delegations; check for cycles.

### 8.6. Delegation chains

Delegation chains are allowed:

- Alice → Bob → Carol.

Power flows through the chain: Alice's power goes to Bob, Bob's power (including Alice's) goes to Carol.

If `max_delegation_depth` is set, chains longer than the limit are rejected.

Default: no limit (with cycle prevention).

### 8.7. Delegation scope

A delegation **MAY** be limited by scope:

```json
"scope": ["budget", "rule_change"]
```

Only votes of the specified types are affected. Other votes use the delegator's own power.

If `scope` is absent, the delegation applies to all votes.

### 8.8. Delegation expiry

A delegation **MAY** expire:

```json
"until": 1760000000
```

After expiry, the delegation is no longer valid. The delegator's power reverts to them.

If `until` is absent, the delegation is permanent until revoked.

### 8.9. Anti-vote-buying

Delegation **MUST NOT** be sold.

Rules:

- a delegate **MUST NOT** pay a delegator for delegation;
- a delegator **MUST NOT** demand payment for delegation;
- any evidence of vote-buying results in reputation penalty and invalidation of the delegation.

Enforcement is social + cryptographic:

- patterns of delegation followed by payments are flagged;
- communities **MAY** vote to invalidate suspect delegations.

### 8.10. Revocation

A delegator **MAY** revoke a delegation at any time:

```json
{
  "type": "vote.undelegate",
  "author": "did:cl:main:alice",
  "payload": {
    "context": "repo:github.com/x/y"
  }
}
```

After revocation, the delegator's power reverts to them.

### 8.11. Delegation and snapshot

Delegation is frozen at snapshot time:

- if a delegation exists at snapshot time, it applies to the vote;
- if delegation is added after snapshot, it does not apply;
- if delegation is revoked after snapshot, it still applies.

### 8.12. Delegated vote

A delegate **MAY** vote with their own power plus delegated power.

The delegate **MUST** vote the same way for all delegators (they cannot split delegated votes).

### 8.13. Self-delegation

Self-delegation is invalid.

### 8.14. Delegation without voting

If a delegate does not vote, the delegated power is not used.

It does not revert to the delegator.

### 8.15. Delegation transparency

All delegations are on-ledger. Anyone can see:

- who delegated to whom;
- when;
- for what scope;
- until when.

This builds trust and allows detection of vote-buying.

### 8.16. Delegation limits

Contexts **MAY** limit:

- maximum delegates per delegator (usually 1);
- maximum delegators per delegate;
- maximum total delegated power per delegate.

### 8.17. Delegation events

| Event | Purpose |
|---|---|
| `vote.delegate` | Create or update a delegation. |
| `vote.undelegate` | Revoke a delegation. |
| `vote.delegate_accept` | Optional: delegate accepts. |
| `vote.delegate_reject` | Optional: delegate rejects. |

Acceptance is optional; most contexts do not require it.

---

## 9. Tallying

### 9.1. When tallying occurs

Tallying occurs after the vote's deadline.

Anyone **MAY** submit the tally:

```json
{
  "type": "vote.tally",
  "author": "did:cl:main:anyone",
  "payload": {
    "vote_id": "blake3:...",
    "result": "passed",
    "tally": {
      "yes": 150.5,
      "no": 50.0,
      "abstain": 10.0
    },
    "total_power": 210.5,
    "participation": 0.7,
    "quorum_met": true,
    "threshold_met": true
  },
  "signature": "ed25519:..."
}
```

### 9.2. Tally computation

Steps:

1. Collect all `vote.cast` events for the vote.
2. Filter to valid votes (eligible, not duplicate, not withdrawn).
3. For each vote, compute the voter's power at snapshot time.
4. Sum power per option.
5. Compute total power.
6. Compute participation (total power of voters / total eligible power).
7. Check quorum.
8. Check threshold.

### 9.3. Voting power computation

For each voter `u`:

```
power(u) = own_power(u) + delegated_power(u)
```

Where:

- `own_power(u) = sqrt(reputation(u, context, snapshot_time))` (for quadratic);
- `delegated_power(u) = Σ_v sqrt(reputation(v, context, snapshot_time))` for delegators `v`.

### 9.4. Total power

```
total_power = Σ_u power(u)
```

Over all voters.

### 9.5. Participation

```
participation = total_power / eligible_power
```

Where `eligible_power` is the total power of all eligible identities (whether they voted or not).

### 9.6. Quorum check

If `participation < quorum`, the vote **FAILS** (regardless of outcome).

If `quorum` is not set, default is `0.0` (no quorum).

### 9.7. Threshold check

For the winning option `w`:

```
share(w) = power(w) / total_power
```

The vote **PASSES** if `share(w) ≥ threshold`.

Thresholds like `"2/3"` mean `share ≥ 2/3`.

`"1/2+"` means `share > 1/2`.

### 9.8. Abstentions

Abstentions count toward participation (for quorum) but not toward the threshold.

So a vote with 60% yes, 20% no, 20% abstain:

- `total_power = 1.0`;
- `share(yes) = 0.6`;
- threshold `"1/2"` is met (0.6 > 0.5).

But a vote with 40% yes, 30% no, 30% abstain:

- `share(yes) = 0.4`;
- threshold `"1/2"` is NOT met.

### 9.9. Tie handling

If two options tie:

- the context's rules decide;
- default: the vote fails.

### 9.10. Result event

When tallying is complete, a `vote.final` event is created:

```json
{
  "type": "vote.final",
  "author": "did:cl:main:anyone",
  "payload": {
    "vote_id": "blake3:...",
    "result": "passed",
    "tally": {...},
    "total_power": 210.5,
    "participation": 0.7
  }
}
```

This event is final once enough validators sign a checkpoint containing it.

### 9.11. Determinism

Tallying **MUST** be deterministic:

- votes sorted by canonical order;
- power computed with 6-decimal precision;
- sum in deterministic order.

### 9.12. Verification

Anyone **MAY** verify the tally by recomputing from events.

If a discrepancy is found:

- a dispute **MAY** be opened;
- arbiters verify;
- if the tally is wrong, it is corrected.

### 9.13. Duplicate tallies

Multiple `vote.tally` events **MAY** exist for the same vote. Only the first valid one counts.

### 9.14. Tally deadline

If no tally is submitted within N days after the deadline (e.g., 7 days), anyone **MAY** submit one.

If no tally is submitted within 30 days, the vote is auto-tallied by the protocol.

### 9.15. Auto-tally

The protocol **SHOULD** auto-tally votes after the deadline if no manual tally is submitted.

Auto-tally uses the same rules as manual tally.

---

## 10. Secret Voting (ZK)

### 10.1. Purpose

Secret voting hides the choice of each voter while keeping the tally verifiable.

This protects:

- voters from coercion;
- voters from retaliation;
- sensitive decisions.

### 10.2. When to use

Secret voting is opt-in. It is used for:

- elections;
- sensitive policy changes;
- disciplinary votes;
- any decision where privacy matters.

### 10.3. Cryptographic primitives

Secret voting uses:

- **Pedersen commitments** for hiding votes;
- **Zero-knowledge proofs** (Bulletproofs or zk-SNARKs) for proving validity;
- **Homomorphic tallying** for computing the result without revealing individual votes.

### 10.4. Vote commitment

A voter commits to their vote:

```
commitment = PedersenCommit(option, randomness)
```

The commitment is published on-ledger. It does not reveal the option.

### 10.5. Zero-knowledge proof

The voter proves:

- the committed option is one of the allowed options;
- the voter is eligible;
- the voter has not voted twice;
- the voter's power is correct.

The proof does not reveal:

- the option;
- the voter's identity (optional);
- the voter's power.

### 10.6. Homomorphic tally

If commitments are homomorphic (Pedersen is), the sum of commitments equals the commitment of the sum:

```
Σ commitments = Commit(Σ options)
```

This allows the tally to be computed without decrypting individual votes.

### 10.7. Decryption

For the result to be revealed, the sum commitment must be decrypted.

This requires:

- a trusted party (or threshold of parties) holding the decryption key;
- a threshold scheme (e.g., 3 of 5 validators);
- a reveal after the deadline.

### 10.8. Secret voting event

```json
{
  "type": "vote.cast_secret",
  "author": "did:cl:main:bob",
  "payload": {
    "vote_id": "blake3:...",
    "commitment": "pedersen:...",
    "proof": "zkp:...",
    "power_proof": "zkp:..."
  }
}
```

### 10.9. Tally event (secret)

```json
{
  "type": "vote.tally_secret",
  "payload": {
    "vote_id": "blake3:...",
    "sum_commitment": "pedersen:...",
    "decrypted_tally": {"yes": 150.5, "no": 50.0, "abstain": 10.0},
    "decryption_proof": "zkp:..."
  }
}
```

### 10.10. Verification

Anyone **MAY** verify:

- each commitment is valid;
- each proof is valid;
- the sum commitment matches the sum of individual commitments;
- the decryption proof is valid;
- the decrypted tally matches the sum commitment.

### 10.11. Trust assumptions

Secret voting trusts:

- the cryptographic primitives (Pedersen, Bulletproofs);
- the decryption parties (unless using a trustless scheme);
- the ZK proof system.

### 10.12. Cost

Secret voting is expensive:

- ZK proofs are computationally heavy;
- homomorphic tallying is slower;
- implementation is more complex.

Contexts **SHOULD** use it only when needed.

### 10.13. Reveal after deadline

After the deadline:

- decryption parties reveal their shares;
- the tally is computed;
- the result is published.

### 10.14. No retroactive de-anonymization

Once votes are decrypted (as a sum), individual votes **MUST NOT** be de-anonymizable.

Unless the voter voluntarily reveals their choice (via a `vote.reveal` event).

### 10.15. Fallback

If ZK proofs are not feasible (e.g., due to bugs), contexts **MAY** fall back to public voting.

### 10.16. Hybrid voting

Some contexts **MAY** use hybrid voting:

- public for routine decisions;
- secret for sensitive decisions.

The choice is per vote.

---

## 11. Veto and Minority Protection

### 11.1. Purpose

Veto protects significant minorities from being overruled on fundamental issues.

### 11.2. When veto applies

Veto applies only if `veto_required = true` in the vote.

Contexts **SHOULD** use veto only for:

- constitutional changes;
- rule changes affecting core rights;
- forks;
- anything else the community considers fundamental.

### 11.3. Veto threshold

A veto is triggered if:

- the minority against an option has ≥ `veto_threshold` share of total power.

Typical veto threshold: `1/3`.

So if 34% vote "no" on a constitutional change, the change fails.

### 11.4. Veto event

The veto is automatic if the threshold is met. A `vote.veto` event is recorded:

```json
{
  "type": "vote.veto",
  "payload": {
    "vote_id": "blake3:...",
    "veto_share": 0.35,
    "veto_threshold": 0.33
  }
}
```

### 11.5. Override

A veto **MAY** be overridden by a second vote with a higher threshold.

For example:

- first vote: 2/3 threshold, veto at 1/3.
- If vetoed, a second vote with 3/4 threshold can override.

The override rules are defined by the context.

### 11.6. Repeated vetoes

If the same proposal is vetoed multiple times, it **MUST NOT** be proposed again for a period (e.g., 6 months).

This prevents endless re-proposals.

### 11.7. Veto transparency

Vetoes are on-ledger. The minority's identity is visible (unless secret voting).

### 11.8. Veto and delegation

Delegated power counts toward veto.

### 11.9. Veto and quorum

Quorum **MUST** be met for a veto to be valid. Low participation invalidates the veto.

---

## 12. Finalization

### 12.1. Vote result

The result of a vote is:

- `passed` — threshold met, quorum met, no veto.
- `failed` — threshold not met, or quorum not met.
- `vetoed` — threshold met, but veto triggered.
- `invalid` — some rule violation.

### 12.2. Finalization event

```json
{
  "type": "vote.final",
  "payload": {
    "vote_id": "blake3:...",
    "result": "passed",
    "tally": {...}
  }
}
```

### 12.3. Applying the result

If `passed`:

- the change is applied to the context's rules (or target);
- the change takes effect immediately (or at a scheduled time);
- the change is recorded in a `rule.change` or equivalent event.

If `failed`:

- the change is not applied;
- the vote is recorded as failed.

If `vetoed`:

- the change is not applied;
- a cooldown period begins.

### 12.4. Finality

The vote is final when:

- the tally is submitted;
- no dispute is open;
- the finalization is included in a finalized checkpoint.

### 12.5. Reverting a vote

A finalized vote **MUST NOT** be reverted.

Exception: proven fraud or protocol violation. In that case:

- a dispute is opened;
- arbiters (or a council) decide;
- if fraud is proven, the vote is invalidated.

### 12.6. Retroactive effect

Votes **MUST NOT** have retroactive effect, unless explicitly stated.

A rule change applies from the vote's finalization time, not from the past.

### 12.7. Notification

On finalization:

- the proposer is notified;
- voters are notified;
- the context's feed shows the result;
- the result is queryable via API.

---

## 13. Disputes and Appeals

### 13.1. When disputes occur

Disputes **MAY** be opened for:

- incorrect tally;
- rule violation in the vote process;
- ineligibility of a voter;
- failure to apply the result.

### 13.2. Opening a dispute

```json
{
  "type": "vote.dispute",
  "author": "did:cl:main:anyone",
  "payload": {
    "vote_id": "blake3:...",
    "reason": "tally_incorrect",
    "evidence": [...]
  }
}
```

### 13.3. Dispute process

Similar to bounty disputes:

1. Dispute opened.
2. 3 arbiters selected (high reputation, no conflict).
3. Arbiters review.
4. Vote: uphold / overturn / new tally.
5. Decision final.

### 13.4. Appeal

A dispute decision **MAY** be appealed to a council (if one exists).

### 13.5. Effect of dispute

During a dispute:

- the vote result is frozen;
- the change is not applied (or paused if already applied).

### 13.6. Fraud

If fraud is proven:

- the vote is invalidated;
- the fraudster loses reputation;
- the fraudster may be banned from voting.

### 13.7. Dispute timeouts

- Dispute must be opened within 14 days of finalization.
- Arbiters must decide within 7 days.

---

## 14. Validation Rules

Nodes **MUST** enforce these rules for vote-related events.

### 14.1. `vote.create` rules

- The context **MUST** exist.
- The creator **MUST** meet `vote_create_threshold`.
- `options` **MUST** be non-empty, with unique strings.
- `threshold` **MUST** be a valid threshold string.
- `weighting` **MUST** be one of the allowed values.
- `deadline` **MUST** be in the future.
- `snapshot` **MUST** be a valid state root.

### 14.2. `vote.cast` rules

- The vote **MUST** be `open`.
- The voter **MUST** be eligible at snapshot time.
- The option **MUST** be one of the vote's options.
- The voter **MUST NOT** have already voted.
- The vote **MUST** be before the deadline.

### 14.3. `vote.delegate` rules

- The delegator **MUST** be a member of the context.
- The delegate **MUST** be a member of the context.
- The delegate **MUST NOT** be the delegator.
- No delegation cycle **MUST** be created.
- `scope` (if present) **MUST** contain valid vote types.
- `until` (if present) **MUST** be in the future.

### 14.4. `vote.undelegate` rules

- The delegation **MUST** exist.
- The undelegator **MUST** be the original delegator.

### 14.5. `vote.tally` rules

- The vote **MUST** be closed (deadline passed).
- No valid tally **MUST** already exist.
- The tally **MUST** match the recomputed tally.
- Quorum and threshold **MUST** be correctly evaluated.

### 14.6. `vote.final` rules

- The tally **MUST** exist.
- No dispute **MUST** be open.
- The finalization **MUST** be signed by an authorized identity.

### 14.7. `vote.dispute` rules

- The vote **MUST** be closed or finalized.
- The dispute **MUST** be opened within the allowed period.
- The disputer **MUST** have standing.

### 14.8. Determinism

- All tallying **MUST** be deterministic.
- All power computations **MUST** use snapshot values.
- All rounding **MUST** be consistent.

### 14.9. Delegation checks

- Cycles **MUST** be detected and rejected.
- Delegated power **MUST** be correctly attributed.
- Self-delegation **MUST** be rejected.

### 14.10. Secret voting checks

- Commitments **MUST** be valid.
- Proofs **MUST** verify.
- Sum commitment **MUST** match.
- Decryption proof **MUST** be valid.

---

## 15. Examples

### 15.1. Simple binary vote

**Creation:**

```json
{
  "type": "vote.create",
  "author": "did:cl:main:alice",
  "payload": {
    "proposal": "add_rule_x",
    "context": "repo:x/y",
    "description": "Add rule X to the context.",
    "options": ["yes", "no", "abstain"],
    "threshold": "1/2+",
    "weighting": "quadratic",
    "deadline": 1730100000,
    "snapshot": "blake3:...",
    "quorum": 0.1
  }
}
```

**Casts:**

```json
{"type": "vote.cast", "author": "did:cl:main:bob", "payload": {"vote_id": "blake3:...", "option": "yes"}}
{"type": "vote.cast", "author": "did:cl:main:carol", "payload": {"vote_id": "blake3:...", "option": "no"}}
{"type": "vote.cast", "author": "did:cl:main:dave", "payload": {"vote_id": "blake3:...", "option": "yes"}}
```

**Tally:**

- Bob: reputation 100 → power 10.
- Carol: reputation 400 → power 20.
- Dave: reputation 25 → power 5.

- Yes: 10 + 5 = 15.
- No: 20.
- Total: 35.
- Participation: 35 / eligible_power.

If eligible_power = 100, participation = 0.35 (quorum 0.1 met).

Share(yes) = 15 / 35 = 0.4286. Threshold `1/2+` not met.

Result: **failed**.

### 15.2. Quadratic vs. linear

Same reputation values:

| Voter | Reputation | Linear | Quadratic |
|---|---|---|---|
| Bob | 100 | 100 | 10.000 |
| Carol | 400 | 400 | 20.000 |
| Dave | 25 | 25 | 5.000 |

**Linear:** Yes (Bob+Dave) = 125; No (Carol) = 400. No wins.

**Quadratic:** Yes = 15; No = 20. No wins but with a much smaller margin.

Quadratic reduces the dominance of high-reputation voters.

### 15.3. Delegation

Alice (rep 100, power 10) delegates to Bob (rep 400, power 20).

Bob's total power for the vote: 20 + 10 = 30.

If Bob votes "yes", it counts as 30.

### 15.4. Delegation chain

Alice (10) → Bob (20) → Carol (30).

Carol's power: 30 + 20 + 10 = 60.

(Assuming no caps.)

### 15.5. Cycle prevention

Alice → Bob → Alice.

This is rejected. The second delegation (Bob → Alice) is invalid.

### 15.6. Veto

Constitutional vote with `veto_required = true`, `veto_threshold = 1/3`.

Result: 70% yes, 30% no.

30% ≥ 1/3? No (30% < 33.3%).

Veto not triggered. Vote passes (if threshold met).

If 35% no, veto triggered. Vote fails.

### 15.7. Quorum failure

Quorum: 0.5 (50%).

Participation: 40%.

Quorum not met. Vote fails, regardless of outcome.

### 15.8. Secret vote

1. Alice commits: `commitment = PedersenCommit("yes", r1)`.
2. Alice submits `vote.cast_secret` with commitment + ZK proof.
3. Same for other voters.
4. Tally: sum commitments = commitment of sum.
5. Decryption parties reveal shares.
6. Sum decrypted: {yes: 150.5, no: 50.0}.
7. Result published.

No individual vote is revealed.

### 15.9. Dispute

Vote finalized as `passed`.

Bob disputes: "my vote was not counted."

Arbiters verify: Bob's `vote.cast` event exists and is valid. It was incorrectly excluded.

Decision: `overturn` — new tally computed with Bob's vote.

### 15.10. Vote on removing a validator

```json
{
  "type": "vote.create",
  "payload": {
    "proposal": "remove_validator_V3",
    "context": "repo:x/y",
    "options": ["yes", "no", "abstain"],
    "threshold": "2/3",
    "weighting": "quadratic",
    "target": "validator:did:cl:main:V3",
    "deadline": 1730100000
  }
}
```

If passed, `validator.remove` is triggered.

---

## 16. Test Vectors

Test vectors for voting live in `spec/test-vectors/votes.json`.

### 16.1. Coverage

- Vote creation with all fields.
- Vote cast with each option.
- Quadratic vs. linear vs. simple weighting.
- Delegation (single, chain, cycle).
- Tally computation (with and without quorum).
- Threshold check.
- Veto detection.
- Secret voting (commitments, proofs, tally).
- Dispute resolution.
- Invalid cases: duplicate votes, post-deadline votes, wrong options, ineligible voters, cycles.

### 16.2. Format

```json
{
  "description": "Quadratic vote with delegation",
  "vote": {...},
  "voters": [
    {"did": "did:cl:main:alice", "reputation": 100, "option": "yes"},
    {"did": "did:cl:main:bob", "reputation": 400, "option": "no", "delegates": [{"from": "did:cl:main:carol", "reputation": 25}]}
  ],
  "expected_tally": {"yes": 10.0, "no": 25.0},
  "expected_result": "failed"
}
```

### 16.3. Determinism

All tally results **MUST** be identical across implementations.

### 16.4. Cross-implementation

Test vectors **MUST** pass on at least two implementations before v1.0.

### 16.5. ZK test vectors

For secret voting:

- commitment generation;
- ZK proof verification;
- homomorphic tally;
- decryption proof.

These require a specific ZK library. Implementations **MUST** agree on the variant.

---

## 17. Open Questions

- Should voting power be **quadratic** by default, or context-specific?
- How to prevent **Sybil voting** without requiring full identity verification?
- Should **delegation** be time-limited or indefinite by default?
- How to detect **vote-buying** when delegation is allowed?
- Should there be a **cap on voting power** per identity?
- How to handle **reputation changes** mid-vote (snapshot is current solution)?
- Should **secret voting** be the default for all votes?
- How to handle **vote privacy** without heavy ZK overhead?
- Should **veto** be automatic or require a separate vote?
- How to prevent **endless veto cycles**?
- Should there be a **minimum participation** for all votes?
- How to handle **delegation cascades** efficiently at scale?
- Should **ranked-choice voting** be supported natively?
- How to handle **vote weight** for organizations (multiple DIDs)?
- Should there be a **vote fee** to prevent spam?

These will be resolved through RFCs and community discussion.

---

## Summary

**Voting is:**

- Reputation-based, not token-based.
- Quadratic by default (√reputation).
- Snapshot-frozen.
- Contextual.
- Delegable (without transfer).
- Optionally secret (ZK).
- Veto-protected for fundamental changes.

**Vote types:**

- Rule changes, validator changes, roles, budgets, grants, forks.
- Binary, multi-option, ranked, approval.
- Simple, qualified, supermajority, consensus.

**Eligibility:**

- Members of the context.
- Reputation ≥ threshold.
- Level 1+ (for most votes).

**Power:**

- `simple`: 1.
- `linear`: reputation.
- `quadratic`: √reputation.
- `delegated`: own + delegated.

**Casting:**

- One vote per identity.
- Before deadline.
- Options only.
- Public or secret.

**Delegation:**

- Transfers power, not reputation.
- Temporary, revocable.
- Cannot be bought.

**Tallying:**

- Deterministic.
- Snapshot-based.
- Quorum + threshold.
- Veto protection.

**Secret voting:**

- Pedersen commitments.
- ZK proofs.
- Homomorphic tally.
- Threshold decryption.

**Finalization:**

- `passed`, `failed`, `vetoed`, `invalid`.
- Applied via `rule.change` or target event.
- Disputes possible.

**Key insight:**

Voting in CL is **not** about counting tokens. It is about counting **earned trust**. Quadratic weighting ensures that no one — no matter how much reputation — can dominate. Delegation allows expertise to represent others. ZK allows privacy without sacrificing verifiability.

The math is simple. The politics is not. CL provides the tools. Communities use them.

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [identity.md](./identity.md) — identity model.
- [contribution.md](./contribution.md) — contribution records.
- [reputation.md](./reputation.md) — reputation (basis for voting power).
- [consensus.md](./consensus.md) — validators, finalization.
- [bounty.md](./bounty.md) — bounty disputes (parallel to vote disputes).
- [privacy.md](./privacy.md) — ZK proofs.
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026 
**Version:** 0.1 (draft)

---
