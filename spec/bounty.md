# Bounty

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md) · [identity.md](./identity.md) · [contribution.md](./contribution.md) · [reputation.md](./reputation.md)  
**Related:** [vote.md](./vote.md) · [compute.md](./compute.md) · [api.md](./api.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [Bounty Lifecycle](#3-bounty-lifecycle)
4. [Bounty Creation](#4-bounty-creation)
5. [Escrow](#5-escrow)
6. [Claiming a Bounty](#6-claiming-a-bounty)
7. [Submission](#7-submission)
8. [Verification](#8-verification)
9. [Completion and Payment](#9-completion-and-payment)
10. [Cancellation](#10-cancellation)
11. [Disputes and Arbitration](#11-disputes-and-arbitration)
12. [Reputation and CU](#12-reputation-and-cu)
13. [Payment Rails](#13-payment-rails)
14. [Multi-Milestone Bounties](#14-multi-milestone-bounties)
15. [Bounty Types](#15-bounty-types)
16. [Anti-Abuse](#16-anti-abuse)
17. [Validation Rules](#17-validation-rules)
18. [Examples](#18-examples)
19. [Test Vectors](#19-test-vectors)
20. [Open Questions](#20-open-questions)

---

## 1. Overview

A **bounty** is a paid task posted by an issuer. It is the primary mechanism for direct payment in Contribution Ledger:

- an organization, fund, or individual posts a task;
- funds are locked in escrow;
- a participant claims the task;
- the participant completes it and submits evidence;
- verifiers confirm the work;
- escrow releases payment;
- a contribution record is created;
- CU and reputation are awarded.

Bounties connect three layers of CL:

- **Identity** — who posts, who works, who verifies.
- **Contribution** — the work is recorded as a contribution.
- **Economics** — real money moves from client to worker.

**This file defines:**

- The bounty lifecycle (Section 3).
- How bounties are created (Section 4).
- How escrow works (Section 5).
- How bounties are claimed (Section 6).
- How work is submitted (Section 7).
- How work is verified (Section 8).
- How payment is released (Section 9).
- How bounties are cancelled (Section 10).
- How disputes are arbitrated (Section 11).
- How CU and reputation are awarded (Section 12).
- Payment rails (Section 13).
- Multi-milestone bounties (Section 14).
- Bounty types (Section 15).
- Anti-abuse measures (Section 16).
- Validation rules (Section 17).

Bounties are the closest thing CL has to a market. Everything else (grants, cooperatives, compute) builds on the same primitives.

---

## 2. Design Principles

### 2.1. Escrow-first

**No work begins without funded escrow.**

This protects both sides:

- the worker knows the money exists;
- the issuer knows the money will only be released on completion.

Bounties without funded escrow **MUST NOT** be claimable.

### 2.2. Explicit requirements

A bounty **MUST** specify:

- what needs to be done;
- what counts as completion;
- what evidence is required;
- the deadline (optional but recommended).

Vague bounties lead to disputes. The protocol does not prevent vague bounties, but verifiers and arbiters will judge them strictly.

### 2.3. Verifiable completion

Completion is determined by:

- **verifiers** (peers with reputation in the context);
- **evidence** (hashes, links, automated checks);
- **requirements** (explicit criteria).

Not by the issuer alone, not by the worker alone.

### 2.4. Arbitration as fallback

If verification fails (dispute), arbitration resolves it:

- 3 randomly chosen auditors;
- vote-based decision;
- escrow released per the decision.

Arbitration is a last resort, not the default.

### 2.5. Money outside the protocol

The protocol records **that** payment was made and by what rail, but does not move money itself.

Payment rails:

- fiat (Stripe, Wise, bank transfer);
- stablecoins (USDC, USDT, DAI);
- crypto (BTC, ETH — optional);
- in-kind (services, access, resources).

### 2.6. CU is not the reward

Bounties pay **real money**. CU is awarded in addition, as a record of contribution.

A bounty does not pay in CU. CU cannot be bought or sold. Confusing the two breaks the system.

### 2.7. Reputation gates participation

Not everyone can claim any bounty. Eligibility depends on:

- reputation threshold in the context;
- identity level (Level 1+ for most, Level 2+ for high-value);
- past performance (no pattern of failed bounties);
- no active disputes.

### 2.8. Bounded resources

Bounties **MUST** be bounded:

- maximum escrow amount;
- maximum deadline;
- maximum number of concurrent bounties per issuer;
- maximum claim rate per worker.

This prevents abuse and resource exhaustion.

### 2.9. Transparency

Every step is on-ledger:

- creation;
- funding;
- claim;
- submission;
- verification;
- completion;
- disputes.

Anyone can audit any bounty.

---

## 3. Bounty Lifecycle

### 3.1. States

A bounty passes through the following states:

```
draft → open → claimed → submitted → verified → completed
         │                 │           │
         │                 │           └──→ disputed → resolved
         │                 └──→ disputed → resolved
         └──→ cancelled
```

| State | Description |
|---|---|
| `draft` | Created locally, not yet funded. |
| `open` | Funded, visible, claimable. |
| `claimed` | Claimed by a worker. |
| `submitted` | Worker submitted work. |
| `verified` | Verifiers approved the work. |
| `completed` | Payment released, CU awarded. |
| `disputed` | Dispute opened. |
| `resolved` | Dispute resolved (payment released or cancelled). |
| `cancelled` | Bounty cancelled before claim. |
| `expired` | Deadline passed without completion. |

### 3.2. Transitions

**draft → open:**
- Escrow funded.
- Requirements validated.

**open → claimed:**
- A worker claims the bounty.
- Claim meets eligibility.

**claimed → submitted:**
- Worker submits work with evidence.
- Before or at deadline.

**submitted → verified:**
- Verification threshold met.
- Payment released.

**submitted → disputed:**
- Either party opens a dispute.

**claimed → disputed:**
- Dispute before submission (rare; e.g., worker disappears).

**disputed → resolved:**
- Arbitration decision.
- Payment released per decision.

**open → cancelled:**
- Issuer cancels before claim.
- Escrow refunded.

**claimed → expired:**
- Deadline passed, no submission.
- Escrow refunded (or partial).
- Worker penalized in reputation (if repeated).

**any → cancelled (by issuer):**
- Only in `draft` or `open` states.
- Once claimed, cancellation requires worker consent or arbitration.

### 3.3. Terminal states

- `completed` — success.
- `cancelled` — issuer withdrew.
- `resolved` — dispute settled.
- `expired` — deadline passed.

No transitions out of terminal states.

### 3.4. Timeline

Typical bounty timeline:

| Step | Duration |
|---|---|
| Draft → open (funding) | Minutes to hours |
| Open → claimed | Hours to days |
| Claimed → submitted | Hours to weeks (per deadline) |
| Submitted → verified | Hours to days |
| Verified → completed | Minutes (payment) |

Disputes add 3–14 days.

---

## 4. Bounty Creation

### 4.1. Prerequisites

To create a bounty, the issuer **MUST**:

- be a Level 2+ identity (verified);
- have reputation ≥ threshold in the context (if the context requires it);
- have no active penalties;
- have the funds to escrow.

### 4.2. Creation event

```json
{
  "version": 1,
  "type": "bounty.create",
  "author": "did:cl:org:startupX",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "task": "Write API documentation for v2",
    "context": "repo:github.com/x/y",
    "reward": {
      "amount": 500,
      "currency": "USD",
      "method": "escrow"
    },
    "escrow_id": "did:cl:escrow:main:123",
    "deadline": 1730100000,
    "requirements": [
      "3 peer reviews",
      "grammar check passed",
      "code examples tested"
    ],
    "eligibility": {
      "min_reputation": 100,
      "min_level": 1,
      "max_concurrent": 3
    },
    "verification": {
      "threshold": 3,
      "min_reputation": 100,
      "roles": ["reviewer", "maintainer"]
    },
    "weight_class": "bounty_doc",
    "evidence_required": true,
    "auto_approve_after": 604800
  },
  "signature": "ed25519:..."
}
```

### 4.3. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `task` | string | MUST | Human-readable description of the work. |
| `context` | string | MUST | The context (community/project). |
| `reward` | object | MUST | Amount, currency, method. |
| `escrow_id` | string | MUST | DID of the escrow (Section 5). |
| `deadline` | integer | MAY | Unix timestamp. |
| `requirements` | array | MAY | Explicit completion criteria. |
| `eligibility` | object | MAY | Who can claim. |
| `verification` | object | MUST | How work is verified. |
| `weight_class` | string | MUST | CU weight class (from context rules). |
| `evidence_required` | boolean | MAY | Whether evidence is mandatory. Default: true. |
| `auto_approve_after` | integer | MAY | Seconds; if no verification, auto-approve. |

### 4.4. Reward

```json
{
  "amount": 500,
  "currency": "USD",
  "method": "escrow"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `amount` | number | MUST | Positive number. |
| `currency` | string | MUST | Currency code (ISO 4217) or token symbol. |
| `method` | string | MUST | `escrow`, `direct`, `milestone`. |

**Validation:**

- `amount` **MUST** be > 0.
- `amount` **MUST NOT** exceed the context's maximum (if set).
- `currency` **MUST** be supported by the escrow.

### 4.5. Requirements

Requirements are free-form strings. They define completion criteria.

Example:

```json
"requirements": [
  "Documentation covers all public API endpoints",
  "Each endpoint has at least one example",
  "Examples are runnable and tested",
  "Grammar and spelling checked"
]
```

Verifiers **MUST** assess whether each requirement is met.

### 4.6. Eligibility

```json
{
  "min_reputation": 100,
  "min_level": 1,
  "max_concurrent": 3,
  "allowed_dids": ["did:cl:main:alice", "did:cl:main:bob"]
}
```

| Field | Description |
|---|---|
| `min_reputation` | Minimum reputation in the context. |
| `min_level` | Minimum identity level (1, 2, or 3). |
| `max_concurrent` | Max concurrent claims per worker. |
| `allowed_dids` | If set, only these DIDs can claim. |

If `eligibility` is absent, defaults apply:

- `min_reputation`: 0.
- `min_level`: 1.
- `max_concurrent`: unlimited.

### 4.7. Verification rules

```json
{
  "threshold": 3,
  "min_reputation": 100,
  "roles": ["reviewer", "maintainer"],
  "allow_issuer_confirm": false
}
```

| Field | Description |
|---|---|
| `threshold` | Number of confirmations required. |
| `min_reputation` | Minimum reputation of a confirmer. |
| `roles` | Roles allowed to confirm (if set). |
| `allow_issuer_confirm` | Whether the issuer counts as a confirmer. |

Defaults:

- `threshold`: 1.
- `min_reputation`: 10.
- `roles`: any.
- `allow_issuer_confirm`: true.

### 4.8. Validation

On creation:

- The context **MUST** exist.
- `weight_class` **MUST** be defined in the context.
- `escrow_id` **MUST** be a valid escrow DID.
- `reward.method` **MUST** be supported.
- `deadline` **MUST** be in the future (if set).
- The issuer **MUST** have the right to create bounties.

### 4.9. Draft state

A bounty is created in `draft` state. It is not visible to workers until escrow is funded.

### 4.10. Activation

Once escrow is funded (Section 5), the bounty transitions to `open`.

A `bounty.fund` event is created:

```json
{
  "type": "bounty.fund",
  "author": "did:cl:escrow:main:123",
  "payload": {
    "bounty_id": "blake3:...",
    "amount": 500,
    "currency": "USD",
    "rail": "stripe",
    "external_ref": "pi_..."
  }
}
```

### 4.11. Visibility

An `open` bounty is visible in:

- the context's bounty list;
- the issuer's bounty list;
- search (by keywords).

Clients **SHOULD** display:

- task description;
- reward;
- deadline;
- requirements;
- eligibility;
- current state.

---

## 5. Escrow

### 5.1. Purpose

Escrow guarantees that:

- the funds exist before work begins;
- the funds are released only on verified completion;
- the funds are refunded if the bounty is cancelled.

### 5.2. Escrow as a DID

Escrow is an identity with a DID:

```
did:cl:escrow:<network>:<id>
```

It is **not** controlled by a single party. Instead, it is controlled by **multisig rules**:

- issuer;
- arbiter (selected by the context);
- protocol rules (automatic release on completion).

### 5.3. Escrow funding

When a bounty is created, the issuer **MUST** fund the escrow before the bounty becomes `open`.

**Fiat example (Stripe):**

1. Issuer creates a payment intent via Stripe API.
2. Funds are held in Stripe's escrow (or a connected account).
3. A `bounty.fund` event is created with the Stripe reference.

**Stablecoin example:**

1. Issuer sends USDC to a multisig wallet controlled by the escrow.
2. A `bounty.fund` event is created with the transaction hash.

### 5.4. Escrow release

On verified completion:

1. A `bounty.complete` event is created.
2. The escrow releases funds to the worker.
3. A `payment.record` event is created with the transaction reference.

Release is automatic if verification threshold is met.

### 5.5. Escrow refund

On cancellation (before claim) or expiration:

1. A `bounty.cancel` or `bounty.expire` event is created.
2. Escrow refunds the issuer.
3. A `payment.record` event is created.

Refund is automatic.

### 5.6. Escrow dispute

If a dispute is opened:

1. Escrow freezes the funds.
2. Arbitration decides.
3. Funds are released per the decision.

### 5.7. Escrow as protocol vs. external

The protocol **does not move money**. It records:

- that funds were escrowed;
- that funds were released;
- by what rail;
- with what external reference.

The actual money movement happens in external systems (Stripe, bank, blockchain).

This is intentional:

- avoids regulatory burden on the protocol;
- allows multiple rails;
- allows communities to choose.

### 5.8. Escrow reference

Every escrow-related event includes:

- `escrow_id`;
- `rail` (stripe, wise, usdc, btc, etc.);
- `external_ref` (Stripe payment ID, transaction hash);
- `status` (pending, held, released, refunded, disputed).

### 5.9. Escrow failure

If the escrow funding fails (payment declined):

- the bounty remains in `draft`;
- the issuer is notified;
- the bounty is not visible to workers.

### 5.10. Escrow timeout

If the escrow is funded but the bounty is not claimed within a timeout (e.g., 90 days):

- the bounty is automatically cancelled;
- the escrow is refunded.

The timeout is set by the context or the issuer.

### 5.11. Escrow and multisig

For large bounties (e.g., > $10 000), a multisig escrow is recommended:

- issuer key;
- arbiter key;
- protocol key (or context admin key).

Release requires 2 of 3.

This prevents:

- issuer refusing to release (arbiter + protocol can override);
- worker stealing funds (issuer + protocol required).

### 5.12. Escrow fees

Escrow **MAY** charge a fee (e.g., 0.5–2%) to cover:

- payment processing;
- arbitration costs;
- protocol development.

Fees are set by the escrow provider (community, foundation, or third party).

CL **SHOULD** keep fees low (< 2%) to be competitive with platforms.

### 5.13. Escrow transparency

Escrow balances **MAY** be publicly visible:

- total escrowed per context;
- per bounty;
- historical releases.

This builds trust.

---

## 6. Claiming a Bounty

### 6.1. Eligibility check

Before claiming, a worker **MUST**:

- meet the eligibility criteria;
- have no active disputes;
- not exceed `max_concurrent`;
- have the required reputation and level.

### 6.2. Claim event

```json
{
  "version": 1,
  "type": "bounty.claim",
  "author": "did:cl:main:alice",
  "created_at": 1730000100,
  "parents": ["blake3:..."],
  "payload": {
    "bounty_id": "blake3:...",
    "estimated_completion": 1730050000,
    "plan": "I will write the docs, add examples, and test them."
  },
  "signature": "ed25519:..."
}
```

### 6.3. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `bounty_id` | string | MUST | The bounty event ID. |
| `estimated_completion` | integer | MAY | Unix timestamp. |
| `plan` | string | MAY | Brief plan (optional). |

### 6.4. Claim rules

- The bounty **MUST** be in `open` state.
- The worker **MUST** meet eligibility.
- The worker **MUST** have no active claim on the same bounty.
- Multiple workers **MAY** claim the same bounty (context-dependent).

### 6.5. Single-claim vs. multi-claim

Contexts **MAY** define:

- **Single-claim:** only one worker can claim. Others are rejected.
- **Multi-claim:** multiple workers can claim; the first to submit verified work gets paid.
- **Competitive:** multiple workers, all paid if verified (e.g., for redundancy).

Default: single-claim.

### 6.6. Claim lock

Once claimed, the bounty is locked for the claimer:

- the issuer cannot cancel without arbitration;
- the claimer cannot claim other bounties beyond `max_concurrent`;
- the claimer has until the deadline to submit.

### 6.7. Deadline extension

If the deadline passes without submission:

- the bounty enters `expired` state;
- the escrow refunds the issuer;
- the claimer's reputation is penalized (small, if first offense; larger for repeated).

A claimer **MAY** request an extension:

```json
{
  "type": "bounty.extend_request",
  "payload": {
    "bounty_id": "blake3:...",
    "new_deadline": 1730200000,
    "reason": "Unexpected scope"
  }
}
```

The issuer **MAY** approve or reject.

### 6.8. Abandonment

If the claimer abandons the bounty (no submission, no communication), the issuer **MAY**:

- wait for the deadline;
- or request early cancellation via arbitration.

If the claimer abandons repeatedly, their ability to claim future bounties is reduced.

### 6.9. Claim withdrawal

A claimer **MAY** withdraw from a bounty before submitting:

```json
{
  "type": "bounty.withdraw",
  "payload": {
    "bounty_id": "blake3:...",
    "reason": "Cannot complete in time"
  }
}
```

The bounty returns to `open` state.

Repeated withdrawals reduce reputation.

### 6.10. Claim transparency

All claims are on-ledger. Anyone can see:

- who claimed;
- when;
- the worker's reputation;
- the worker's past bounties.

---

## 7. Submission

### 7.1. Submission event

```json
{
  "version": 1,
  "type": "bounty.submit",
  "author": "did:cl:main:alice",
  "created_at": 1730050000,
  "parents": ["blake3:..."],
  "payload": {
    "bounty_id": "blake3:...",
    "summary": "Documentation written for all endpoints.",
    "evidence": [
      {"type": "link", "value": "https://github.com/x/y/pull/42"},
      {"type": "hash", "algo": "sha256", "value": "abc..."}
    ],
    "self_assessment": {
      "requirements_met": [true, true, true, true]
    }
  },
  "signature": "ed25519:..."
}
```

### 7.2. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `bounty_id` | string | MUST | The bounty event ID. |
| `summary` | string | MUST | What was done. |
| `evidence` | array | MAY | Evidence supporting completion. |
| `self_assessment` | object | MAY | How the worker thinks they met requirements. |

### 7.3. Evidence

Evidence **MUST** follow the format defined in [contribution.md](./contribution.md#7-evidence).

Common evidence types for bounties:

- pull requests;
- commits;
- deployed artifacts;
- screenshots;
- videos;
- test results;
- audit reports.

### 7.4. Submission rules

- The bounty **MUST** be in `claimed` state.
- The submitter **MUST** be the claimer.
- The submission **MUST** be before the deadline (if set).
- Evidence **MUST** be included if `evidence_required = true`.

### 7.5. Submission deadline

If the deadline passes:

- late submissions are rejected;
- the bounty enters `expired` state.

Exceptions:

- if the deadline was extended by the issuer;
- if arbitration grants an extension.

### 7.6. Multiple submissions

A claimer **MAY** submit multiple times (e.g., to fix issues after partial review).

Rules:

- Each submission is a separate `bounty.submit` event.
- The **latest** submission is used for verification.
- Earlier submissions are kept in the ledger (for audit).

### 7.7. Revision requests

Verifiers **MAY** request revisions:

```json
{
  "type": "bounty.revise_request",
  "author": "did:cl:main:reviewer1",
  "payload": {
    "bounty_id": "blake3:...",
    "issues": [
      "Missing example for /users endpoint",
      "Grammar issue in section 3"
    ]
  }
}
```

The claimer **MAY** fix and re-submit.

### 7.8. Submission as a contribution

A successful submission is recorded as a contribution:

- a `contribution.create` event is created;
- the contribution references the bounty;
- when verified, the contribution earns CU and reputation.

See Section 12.

---

## 8. Verification

### 8.1. Verification event

```json
{
  "version": 1,
  "type": "bounty.verify",
  "author": "did:cl:main:reviewer1",
  "created_at": 1730050100,
  "parents": ["blake3:..."],
  "payload": {
    "bounty_id": "blake3:...",
    "result": "approve",
    "quality": 0.9,
    "comment": "Documentation is thorough and well-tested."
  },
  "signature": "ed25519:..."
}
```

### 8.2. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `bounty_id` | string | MUST | The bounty event ID. |
| `result` | string | MUST | `approve`, `reject`, or `revise`. |
| `quality` | float | MAY | Quality coefficient (0.0–1.0). |
| `comment` | string | MAY | Explanation. |

### 8.3. Verification results

| Result | Effect |
|---|---|
| `approve` | Counts toward completion threshold. |
| `reject` | Counts toward rejection. |
| `revise` | Requests revision; not counted as approve or reject. |

### 8.4. Verification threshold

The bounty is completed when:

- at least `threshold` verifiers have `approve` results;
- the average quality is above the context's minimum (if set).

Defaults:

- `threshold`: 3.
- minimum quality: 0.5.

### 8.5. Who can verify

Verifiers **MUST**:

- have reputation ≥ `verification.min_reputation`;
- have the required roles (if `verification.roles` is set);
- not be the claimer;
- not be the issuer (unless `allow_issuer_confirm = true`).

If the issuer is allowed to confirm, their `approve` counts as **one** confirmation (not the whole threshold).

### 8.6. Verification window

Verifiers **MUST** submit their verification within a window (e.g., 7 days).

If the window passes without enough verifications:

- the bounty is auto-approved if `auto_approve_after` is set;
- otherwise, it goes to arbitration.

### 8.7. Auto-approval

If `auto_approve_after` is set (e.g., 604800 seconds = 7 days), and no rejection or revision request occurs:

- the bounty is auto-approved;
- the escrow releases funds;
- CU is awarded.

This protects workers from silent issuers.

### 8.8. Rejection

If enough verifiers reject:

- the bounty is not completed;
- the claimer **MAY** open a dispute;
- or the bounty returns to `claimed` (if there is time).

### 8.9. Revision loop

If verifiers request revisions:

- the claimer fixes the issues;
- re-submits;
- new verification round.

Repeated revision loops are allowed but consume time. If the deadline passes, the bounty expires.

### 8.10. Verification by the issuer

If `allow_issuer_confirm = true`, the issuer's `approve` counts as one confirmation.

The issuer **MAY** also submit a `reject` — but this alone does not reject the bounty; it requires the threshold of rejections.

### 8.11. Automated verification

Some contexts **MAY** use automated verifiers:

- CI systems (tests pass, build succeeds);
- linters (style checks);
- format checkers.

Automated verifiers **MUST** be identities with the appropriate role.

### 8.12. Verification transparency

All verifications are on-ledger. Anyone can see:

- who verified;
- when;
- the result;
- the quality.

This creates accountability.

### 8.13. Verification penalties

Verifiers who:

- approve work that clearly does not meet requirements;
- reject work that clearly meets requirements;
- abandon verification after accepting the role;

**MAY** be penalized in reputation.

Repeated abuse may result in removal from verifier roles.

---

## 9. Completion and Payment

### 9.1. Completion event

When the verification threshold is met:

```json
{
  "type": "bounty.complete",
  "author": "did:cl:main:anyone",
  "payload": {
    "bounty_id": "blake3:...",
    "verified_by": ["did:cl:main:reviewer1", "did:cl:main:reviewer2", "did:cl:main:reviewer3"],
    "average_quality": 0.9
  },
  "signature": "ed25519:..."
}
```

Anyone **MAY** submit this event (typically the escrow or a verifier).

### 9.2. Escrow release

The escrow releases funds to the worker:

```json
{
  "type": "payment.record",
  "author": "did:cl:escrow:main:123",
  "payload": {
    "bounty_id": "blake3:...",
    "recipient": "did:cl:main:alice",
    "amount": 500,
    "currency": "USD",
    "method": "stripe",
    "external_ref": "tr_...",
    "status": "settled"
  }
}
```

### 9.3. Payment fee

If the escrow charges a fee, it is deducted:

- `reward.amount` is the total;
- `fee` is the escrow fee;
- `net_amount` is what the worker receives.

Example:

- Reward: $500
- Fee: 1% = $5
- Net: $495

The fee is recorded in the `payment.record`.

### 9.4. Contribution creation

On completion, a `contribution.create` event is created (if not already):

```json
{
  "type": "contribution.create",
  "author": "did:cl:main:alice",
  "payload": {
    "subject": "did:cl:main:alice",
    "issuer": "did:cl:org:startupX",
    "action": "bounty_completion",
    "context": "repo:github.com/x/y",
    "weight_class": "bounty_doc",
    "evidence": [...],
    "timestamp": 1730050000,
    "metadata": {
      "bounty_id": "blake3:..."
    }
  }
}
```

### 9.5. CU award

The contribution earns CU per the context's rules:

```
CU = weight × quality × decay
```

Where:

- `weight` is from `weight_class`;
- `quality` is the average quality from verifications;
- `decay` is 1.0 (new contribution).

### 9.6. Reputation update

The worker's reputation in the context increases by the CU amount.

The issuer **MAY** also gain reputation for posting a completed bounty (small weight).

Verifiers gain small CU for their verification work.

### 9.7. Notification

On completion:

- the worker is notified (via their client);
- the issuer is notified;
- verifiers are notified;
- the context's feed shows the completion.

### 9.8. Public record

The completed bounty is publicly visible:

- task;
- reward;
- worker;
- verifiers;
- quality;
- payment reference.

This builds reputation and trust.

### 9.9. Failure to pay

If the escrow does not release funds within a timeout (e.g., 24 hours):

- the worker **MAY** open a dispute;
- the escrow provider is penalized in reputation (if applicable);
- the community **MAY** intervene.

### 9.10. Partial payments

For multi-milestone bounties (Section 14), payments are released per milestone.

### 9.11. Payment rails

See Section 13 for details on fiat, stablecoin, and crypto rails.

---

## 10. Cancellation

### 10.1. Cancellation by issuer (before claim)

The issuer **MAY** cancel an `open` bounty:

```json
{
  "type": "bounty.cancel",
  "author": "did:cl:org:startupX",
  "payload": {
    "bounty_id": "blake3:...",
    "reason": "Task no longer needed"
  }
}
```

Effects:

- escrow refunds the issuer;
- the bounty is marked `cancelled`;
- no CU is awarded.

### 10.2. Cancellation after claim

Once claimed, the issuer **MUST NOT** cancel unilaterally.

Options:

- **Mutual cancellation:** both parties agree.
- **Arbitration:** the issuer requests cancellation; arbiters decide.
- **Expiration:** the deadline passes.

### 10.3. Mutual cancellation

```json
{
  "type": "bounty.cancel_mutual",
  "author": "did:cl:main:alice",
  "payload": {
    "bounty_id": "blake3:...",
    "agreement": {
      "issuer_signature": "ed25519:...",
      "worker_signature": "ed25519:..."
    }
  }
}
```

Both parties sign. Escrow refunds the issuer (or splits per agreement).

### 10.4. Cancellation by arbitration

If the issuer wants to cancel after claim, and the worker disagrees:

1. The issuer opens a dispute.
2. Arbiters decide:
   - cancel: refund issuer;
   - complete: pay worker;
   - partial: split.

### 10.5. Expiration

If the deadline passes without submission:

- the bounty expires;
- escrow refunds the issuer;
- the worker's reputation is penalized (small).

If the worker had partially completed work, they **MAY** negotiate with the issuer or open a dispute.

### 10.6. Cancellation fees

If the issuer cancels after claim:

- a small fee **MAY** be paid to the worker (for time spent);
- the fee is defined in the bounty or by arbitration.

### 10.7. Cancellation of disputed bounties

If a dispute is open, cancellation is not allowed. The dispute **MUST** be resolved first.

---

## 11. Disputes and Arbitration

### 11.1. When disputes occur

Disputes arise when:

- the worker believes the work is complete, but verification fails;
- the issuer believes the work is not complete, but the worker disagrees;
- the deadline passes with partial work;
- the escrow does not release funds.

### 11.2. Opening a dispute

```json
{
  "version": 1,
  "type": "bounty.dispute",
  "author": "did:cl:main:alice",
  "created_at": 1730050200,
  "parents": ["blake3:..."],
  "payload": {
    "bounty_id": "blake3:...",
    "reason": "work_rejected_unfairly",
    "description": "All requirements are met, but the issuer rejected without reason.",
    "evidence": [
      {"type": "link", "value": "https://github.com/x/y/pull/42"},
      {"type": "hash", "algo": "sha256", "value": "abc..."}
    ]
  },
  "signature": "ed25519:..."
}
```

### 11.3. Who can open a dispute

- The worker.
- The issuer.
- Any verifier.
- Any identity with reputation ≥ threshold in the context.

### 11.4. Dispute reasons

| Reason | Description |
|---|---|
| `work_rejected_unfairly` | Worker believes work meets requirements. |
| `work_incomplete` | Issuer believes work does not meet requirements. |
| `deadline_missed` | Deadline passed; worker wants partial payment. |
| `escrow_not_released` | Escrow did not pay after verification. |
| `escrow_not_refunded` | Escrow did not refund after cancellation. |
| `other` | Other (requires description). |

### 11.5. Freezing

When a dispute is opened:

- escrow funds are frozen;
- the bounty enters `disputed` state;
- no further verifications are accepted.

### 11.6. Auditor selection

3 auditors are selected randomly:

```
seed = BLAKE3(dispute_id || latest_checkpoint_root)
auditors = sort_by(BLAKE3(seed || candidate_did))[:3]
```

Candidates are identities with:

- reputation ≥ context's `auditor_threshold` (e.g., 1000);
- no conflict of interest (not issuer, not worker, not verifier);
- no active disputes.

### 11.7. Auditor duties

Each auditor:

1. Reviews the evidence.
2. Checks the requirements.
3. Votes:
   - `favor_worker` — release full payment;
   - `favor_issuer` — refund full amount;
   - `split` — split per agreement;
   - `unclear` — cannot decide.

### 11.8. Decision rules

- Majority wins (2 of 3).
- If `unclear` wins (2 of 3 unclear), the dispute is escalated to a higher council (if one exists).
- If no council exists, the dispute is `resolved` with a default: split 50/50.

### 11.9. Split percentages

If the decision is `split`, the percentage is:

- proposed by the arbiters;
- majority agreement.

Example: 70/30 in favor of the worker.

### 11.10. Auditor compensation

Auditors receive:

- a small fee from the escrow (e.g., 1% of the disputed amount);
- CU for their work.

If an auditor does not vote within the deadline (e.g., 7 days), they lose reputation.

### 11.11. Resolution event

```json
{
  "type": "bounty.resolve",
  "author": "did:cl:main:arbiter1",
  "payload": {
    "bounty_id": "blake3:...",
    "decision": "favor_worker",
    "split": {"worker": 1.0, "issuer": 0.0},
    "auditors": ["did:cl:main:arbiter1", "did:cl:main:arbiter2", "did:cl:main:arbiter3"],
    "votes": ["favor_worker", "favor_worker", "split"]
  },
  "signature": "ed25519:..."
}
```

### 11.12. Escrow release after resolution

Escrow releases funds per the decision:

- `favor_worker`: full payment to worker.
- `favor_issuer`: full refund to issuer.
- `split`: partial per percentage.

### 11.13. Appeals

An appeal **MAY** be filed within a period (e.g., 14 days):

```json
{
  "type": "bounty.appeal",
  "payload": {
    "resolution_id": "blake3:...",
    "reason": "new_evidence",
    "evidence": [...]
  }
}
```

Appeals are reviewed by a higher council (if exists) or by a larger auditor panel (5 auditors).

### 11.14. Frivolous disputes

Repeatedly filing frivolous disputes results in:

- reputation penalty;
- loss of dispute rights;
- possible ban from claiming bounties.

### 11.15. Dispute transparency

All disputes are on-ledger. Anyone can see:

- the reason;
- the evidence;
- the auditors;
- the decision;
- the split.

This creates accountability and trust.

### 11.16. Dispute timeouts

- Auditors must vote within 7 days.
- If auditors do not vote, replacements are selected.
- If no decision after 30 days, the dispute defaults to split 50/50.

---

## 12. Reputation and CU

### 12.1. Worker CU

On completion, the worker earns CU:

```
CU = weight_class_value × average_quality × decay
```

Where:

- `weight_class_value` is defined in the context's rules for the bounty's `weight_class`;
- `average_quality` is the average quality from verifications;
- `decay` is 1.0 for new contributions.

### 12.2. Worker reputation

The worker's reputation in the context increases by the CU amount.

### 12.3. Issuer reputation

The issuer earns a small CU amount for posting a completed bounty:

```
CU_issuer = bounty_issuer_weight × completion_factor
```

Where:

- `bounty_issuer_weight` is defined in the context's rules (e.g., 1);
- `completion_factor` is 1.0 if completed, 0.5 if disputed, 0 if cancelled.

This incentivizes issuers to post successful bounties.

### 12.4. Verifier reputation

Verifiers earn small CU:

```
CU_verifier = verification_weight × (1 - |quality - actual|)
```

Where:

- `verification_weight` is defined in the context's rules (e.g., 0.5);
- `actual` is the final outcome (1.0 if approved, 0.0 if rejected).

Verifiers who match the outcome earn more.

### 12.5. Arbiter reputation

Arbiters earn CU for resolving disputes:

```
CU_arbiter = arbitration_weight × agreement_factor
```

Where:

- `arbitration_weight` is defined in the context's rules (e.g., 5);
- `agreement_factor` is 1.0 if the arbiter voted with the majority, 0.5 otherwise.

### 12.6. Failed bounties

If a bounty fails (expired, cancelled after claim):

- the worker earns **0 CU**;
- the worker's reputation is slightly penalized (e.g., −1% of the bounty weight);
- the issuer earns **0 CU**.

### 12.7. Disputed bounties

If a bounty is disputed:

- the worker earns CU per the resolution (partial CU for split);
- the issuer earns CU per the resolution;
- arbiters earn CU for their work.

### 12.8. Decay

CU from bounties decays per the context's rules (see [reputation.md](./reputation.md#6-decay-function)).

### 12.9. Snapshot for disputes

If a dispute involves reputation thresholds, the reputation at the time of the dispute **MUST** be used (not current reputation).

This prevents gaming via reputation changes during a dispute.

### 12.10. Bounty CU does not transfer

CU from a bounty does not transfer to other contexts. It is context-specific.

Cross-context recognition is per [reputation.md](./reputation.md#8-aggregation-across-contexts).

---

## 13. Payment Rails

### 13.1. Supported rails

| Rail | Method | Typical use |
|---|---|---|
| `stripe` | Fiat | Small to medium bounties |
| `wise` | Fiat | International transfers |
| `bank` | Fiat | Large bounties |
| `usdc` | Stablecoin | Fast, low-fee |
| `usdt` | Stablecoin | Fast, low-fee |
| `dai` | Stablecoin | Decentralized stablecoin |
| `btc` | Crypto | Optional |
| `eth` | Crypto | Optional |
| `in_kind` | Non-monetary | Access, services |

### 13.2. Fiat rails

**Stripe:**

- Payment intent created.
- Funds held in a connected account or Stripe's escrow.
- On completion, transfer to worker's Stripe account.

**Wise:**

- Funds held in a Wise Business account.
- On completion, transfer to worker's bank.

**Bank:**

- Wire transfer to an escrow account.
- Manual release.

### 13.3. Stablecoin rails

**USDC/USDT/DAI:**

- Issuer sends tokens to a multisig wallet.
- On completion, wallet releases to worker's address.
- Transaction hash is recorded.

**Advantages:**

- Fast (seconds to minutes);
- Low fees;
- Global.

**Disadvantages:**

- Requires crypto wallet;
- Regulatory uncertainty;
- Volatility (for non-stablecoins).

### 13.4. Crypto rails (optional)

**BTC/ETH:**

- Same as stablecoins, but with volatility risk.
- **Not recommended** for bounties (volatility makes pricing hard).

### 13.5. In-kind rails

Some bounties pay in:

- access (to a service, community, dataset);
- resources (compute credits, storage);
- services (design, hosting);
- recognition (titles, badges).

In-kind payments **MUST** be recorded as `payment.record` with `method = "in_kind"`.

The protocol does not enforce delivery. Disputes about in-kind payments go to arbitration.

### 13.6. Multi-rail bounties

A bounty **MAY** accept payment in multiple rails:

```json
"reward": {
  "amount": 500,
  "currency": "USD",
  "accepted_rails": ["stripe", "usdc"]
}
```

The worker chooses their preferred rail.

### 13.7. Currency conversion

If the worker prefers a different currency than the reward:

- conversion is done by the payment rail;
- the exchange rate is recorded in the `payment.record`;
- any conversion fees are deducted from the worker's payout (unless agreed otherwise).

### 13.8. Escrow fees

Escrow providers **MAY** charge a fee. Typical: 0.5–2%.

Fees are recorded in the `payment.record`:

```json
{
  "amount": 500,
  "currency": "USD",
  "fee": 5,
  "fee_currency": "USD",
  "net_amount": 495
}
```

### 13.9. Tax reporting

CL does **not** handle taxes. Users are responsible for their own tax obligations.

However, CL **MAY** provide:

- transaction history;
- annual summaries;
- CSV/JSON exports.

### 13.10. Compliance

For large bounties (> $10 000), escrow providers **MAY** require:

- KYC for the worker;
- tax forms;
- other compliance checks.

The protocol does not require these, but escrow providers may.

### 13.11. Payment privacy

Payment records are on-ledger. Amounts and currencies are public.

If privacy is required, escrow providers **MAY** use:

- privacy-preserving tokens;
- off-chain records with hashes on-chain.

CL **MAY** support these as future extensions.

### 13.12. Failure handling

If a payment fails:

- the `payment.record` is marked `failed`;
- the escrow is notified;
- arbitration **MAY** be requested;
- the worker is notified.

### 13.13. Reversals

Payments **MUST NOT** be reversible after settlement.

Exception: proven fraud. In that case:

- a dispute is opened;
- arbitration decides;
- the escrow **MAY** reverse (if the rail supports it).

---

## 14. Multi-Milestone Bounties

### 14.1. Purpose

Large bounties are often split into milestones:

- each milestone is a smaller deliverable;
- payment is released per milestone;
- reduces risk for both parties.

### 14.2. Structure

```json
{
  "type": "bounty.create",
  "payload": {
    "task": "Build a full authentication system",
    "reward": {
      "amount": 5000,
      "currency": "USD",
      "method": "milestone"
    },
    "milestones": [
      {
        "id": "m1",
        "description": "Design document",
        "reward": 500,
        "deadline": 1730100000
      },
      {
        "id": "m2",
        "description": "Implementation",
        "reward": 3000,
        "deadline": 1730200000
      },
      {
        "id": "m3",
        "description": "Documentation and tests",
        "reward": 1500,
        "deadline": 1730300000
      }
    ]
  }
}
```

### 14.3. Lifecycle

Each milestone follows its own lifecycle:

- created → claimed → submitted → verified → completed.

Milestones are sequential: m2 cannot start until m1 is completed.

### 14.4. Escrow

The total amount is escrowed upfront.

Payment is released per milestone.

If a milestone fails, the bounty **MAY** be cancelled from that point:

- completed milestones are paid;
- remaining milestones are refunded.

### 14.5. Disputes

Disputes **MAY** be opened per milestone.

The decision affects only that milestone.

### 14.6. Milestone events

```json
{"type": "bounty.milestone.start", "payload": {"bounty_id": "...", "milestone_id": "m1"}}
{"type": "bounty.milestone.submit", "payload": {"bounty_id": "...", "milestone_id": "m1", "evidence": [...]}}
{"type": "bounty.milestone.complete", "payload": {"bounty_id": "...", "milestone_id": "m1"}}
```

### 14.7. CU per milestone

Each milestone earns CU on completion.

CU is proportional to the milestone's reward relative to the total.

### 14.8. Milestone defaults

If a milestone fails:

- subsequent milestones are cancelled;
- completed milestones remain paid;
- CU is awarded for completed milestones only.

---

## 15. Bounty Types

### 15.1. By outcome

| Type | Description |
|---|---|
| **Task** | One-off deliverable (e.g., write docs). |
| **Ongoing** | Recurring work (e.g., weekly moderation). |
| **Competitive** | Multiple workers, best submission wins. |
| **Redundant** | Multiple workers, all paid if correct. |

### 15.2. By verification

| Type | Description |
|---|---|
| **Peer review** | Verified by peers (default). |
| **Automated** | Verified by tests/CI. |
| **Issuer-only** | Verified only by issuer (riskier). |
| **Hybrid** | Peer + automated. |

### 15.3. By reward

| Type | Description |
|---|---|
| **Fixed** | One amount. |
| **Milestone** | Multiple payments. |
| **Performance** | Reward depends on quality/metrics. |
| **Matching** | Multiple issuers match funds. |

### 15.4. By visibility

| Type | Description |
|---|---|
| **Public** | Visible to all. |
| **Context-only** | Visible only in the context. |
| **Invite-only** | Visible only to invited workers. |

### 15.5. Competitive bounties

In a competitive bounty:

- multiple workers claim;
- each submits work;
- the issuer (or verifiers) choose the best;
- only the winner is paid.

Rules **MUST** specify:

- how many winners;
- evaluation criteria;
- deadline for all submissions.

### 15.6. Redundant bounties

In a redundant bounty:

- multiple workers claim;
- each produces the same result;
- all are paid if correct;
- disagreement triggers arbitration.

Used for:

- verification tasks;
- sensitive computations;
- redundancy in compute (see [compute.md](./compute.md)).

### 15.7. Ongoing bounties

An ongoing bounty is a recurring task:

- monthly retainer for moderation;
- weekly documentation updates.

Rules:

- period (monthly, weekly);
- scope;
- payment per period;
- renewal conditions.

### 15.8. Performance bounties

Reward depends on performance:

- % of tests passing;
- number of bugs fixed;
- speed of completion.

The formula **MUST** be defined in the bounty.

### 15.9. Matching bounties

Multiple issuers contribute to the same bounty:

- each contributes a share;
- the worker is paid from the pool;
- CU is split across issuers.

Example: an open-source project and a company both fund a feature.

---

## 16. Anti-Abuse

### 16.1. Sybil attacks

**Threat:** Fake workers claim bounties, submit garbage, and try to get paid.

**Defense:**

- reputation thresholds for claiming;
- identity level requirements (Level 1+ for most, Level 2+ for high-value);
- escrow verification of worker identity (KYC for large amounts);
- pattern detection (worker submits low-quality work repeatedly);
- reputation penalties for failures.

### 16.2. Fake completion

**Threat:** Worker submits evidence that does not actually meet requirements.

**Defense:**

- peer verification;
- evidence hashes and links;
- automated checks (CI, tests);
- arbitration for disputes.

### 16.3. Issuer refusal to pay

**Threat:** Issuer refuses to release escrow after verified completion.

**Defense:**

- escrow releases automatically on verification;
- if verification fails, arbitration;
- reputation penalty for issuers with many disputes.

### 16.4. Verifier collusion

**Threat:** Verifiers collude to approve low-quality work or reject good work.

**Defense:**

- random verifier selection (for some contexts);
- verifier accountability (penalties);
- multiple verifiers required;
- arbitration as fallback.

### 16.5. Bounty spam

**Threat:** Issuer posts many bounties without intent to pay.

**Defense:**

- escrow required upfront (no unfunded bounties);
- escrow fees discourage spam;
- reputation threshold for issuers;
- rate limits per issuer.

### 16.6. Claim spam

**Threat:** Worker claims many bounties without intending to complete them.

**Defense:**

- `max_concurrent` limits;
- reputation penalty for abandoned claims;
- priority for workers with good history.

### 16.7. Deadline gaming

**Threat:** Worker submits just before deadline, preventing review.

**Defense:**

- verifiers have a window after submission;
- auto-approval only if no rejection or revision request;
- deadline extensions require issuer approval.

### 16.8. Evidence tampering

**Threat:** Worker submits evidence that changes after verification.

**Defense:**

- evidence hashes are stored;
- links are archived (e.g., via IPFS, Wayback Machine);
- verification includes hash checks.

### 16.9. Front-running

**Threat:** Someone sees a bounty and copies the worker's approach.

**Defense:**

- not a real threat in most cases (bounties are public);
- for sensitive bounties, invite-only mode.

### 16.10. Payment fraud

**Threat:** Issuer uses a fraudulent payment method (stolen card, fake stablecoin).

**Defense:**

- escrow validates funds before bounty goes `open`;
- for stablecoins, wait for confirmations;
- for fiat, use reputable processors (Stripe, Wise).

### 16.11. Dispute abuse

**Threat:** Parties open disputes frivolously to delay or harass.

**Defense:**

- arbitration fees;
- reputation penalties for frivolous disputes;
- limits on disputes per identity per period.

### 16.12. Cross-context reputation laundering

**Threat:** Worker earns reputation in a low-standard context and claims high-value bounties in a high-standard context.

**Defense:**

- contexts are isolated by default;
- recognition is explicit with weights and caps;
- high-value bounties require reputation in the same context.

---

## 17. Validation Rules

Nodes **MUST** enforce these rules for bounty-related events.

### 17.1. `bounty.create` rules

- The context **MUST** exist.
- The issuer **MUST** be Level 2+.
- The issuer **MUST** meet the context's requirements for creating bounties.
- `weight_class` **MUST** be defined in the context.
- `escrow_id` **MUST** be a valid escrow DID.
- `deadline` **MUST** be in the future (if set).
- `reward.amount` **MUST** be > 0.
- `reward.currency` **MUST** be supported by the escrow.
- `requirements` **MUST** be non-empty if specified.

### 17.2. `bounty.fund` rules

- The bounty **MUST** exist and be in `draft`.
- The escrow **MUST** be valid.
- The amount **MUST** match `reward.amount`.
- The transaction **MUST** be confirmed.

### 17.3. `bounty.claim` rules

- The bounty **MUST** be in `open`.
- The claimer **MUST** meet eligibility.
- The claimer **MUST NOT** have an active claim on the same bounty.
- The claimer **MUST NOT** exceed `max_concurrent`.
- The claimer **MUST** be Level 1+.

### 17.4. `bounty.submit` rules

- The bounty **MUST** be in `claimed`.
- The submitter **MUST** be the claimer.
- The submission **MUST** be before the deadline.
- Evidence **MUST** be included if `evidence_required`.

### 17.5. `bounty.verify` rules

- The bounty **MUST** be in `submitted`.
- The verifier **MUST** meet verification criteria.
- The verifier **MUST NOT** be the claimer.
- The verifier **MUST NOT** have already verified this submission.
- `result` **MUST** be `approve`, `reject`, or `revise`.
- `quality` **MUST** be in `[0, 1]` if present.

### 17.6. `bounty.complete` rules

- The bounty **MUST** be in `submitted`.
- The verification threshold **MUST** be met.
- The average quality **MUST** meet the context's minimum (if set).

### 17.7. `bounty.cancel` rules

- The bounty **MUST** be in `draft` or `open`.
- The canceller **MUST** be the issuer.
- If in `claimed`, cancellation **MUST** be mutual or via arbitration.

### 17.8. `bounty.dispute` rules

- The bounty **MUST** be in `claimed`, `submitted`, or `verified`.
- The disputer **MUST** have standing.
- The dispute **MUST** include a reason.

### 17.9. `bounty.resolve` rules

- The dispute **MUST** be open.
- The resolver **MUST** be one of the selected arbiters.
- The decision **MUST** be one of the allowed values.
- The threshold **MUST** be met.

### 17.10. `payment.record` rules

- The bounty **MUST** be in a state that allows payment.
- The recipient **MUST** match the worker (for completion) or issuer (for refund).
- The amount **MUST** match the escrow balance.
- The rail **MUST** be valid.

### 17.11. Escrow invariants

- Escrow balance **MUST** be ≥ total of active bounties.
- Escrow **MUST NOT** release more than funded.
- Escrow **MUST** be auditable.

### 17.12. Reputation thresholds

- The issuer **MUST** meet the context's threshold to create bounties.
- The worker **MUST** meet the threshold to claim.
- The verifier **MUST** meet the threshold to verify.
- The arbiter **MUST** meet the threshold to arbitrate.

### 17.13. State transitions

- Invalid transitions **MUST** be rejected.
- Terminal states **MUST NOT** be exited.
- Disputes **MUST** be resolved before final settlement.

---

## 18. Examples

### 18.1. Simple bounty lifecycle

**Step 1: Create.**

```json
{
  "type": "bounty.create",
  "author": "did:cl:org:startupX",
  "payload": {
    "task": "Write API docs",
    "context": "repo:x/y",
    "reward": {"amount": 500, "currency": "USD", "method": "escrow"},
    "escrow_id": "did:cl:escrow:main:123",
    "deadline": 1730100000,
    "requirements": ["All endpoints documented", "Examples tested"],
    "weight_class": "bounty_doc",
    "verification": {"threshold": 3, "min_reputation": 100}
  }
}
```

**Step 2: Fund.**

```json
{
  "type": "bounty.fund",
  "author": "did:cl:escrow:main:123",
  "payload": {
    "bounty_id": "blake3:...",
    "amount": 500,
    "currency": "USD",
    "rail": "stripe",
    "external_ref": "pi_..."
  }
}
```

**Step 3: Claim.**

```json
{
  "type": "bounty.claim",
  "author": "did:cl:main:alice",
  "payload": {
    "bounty_id": "blake3:...",
    "estimated_completion": 1730050000
  }
}
```

**Step 4: Submit.**

```json
{
  "type": "bounty.submit",
  "author": "did:cl:main:alice",
  "payload": {
    "bounty_id": "blake3:...",
    "summary": "Docs complete",
    "evidence": [
      {"type": "link", "value": "https://github.com/x/y/pull/42"}
    ]
  }
}
```

**Step 5: Verify (3 verifiers).**

```json
{"type": "bounty.verify", "author": "did:cl:main:reviewer1", "payload": {"bounty_id": "blake3:...", "result": "approve", "quality": 0.9}}
{"type": "bounty.verify", "author": "did:cl:main:reviewer2", "payload": {"bounty_id": "blake3:...", "result": "approve", "quality": 0.85}}
{"type": "bounty.verify", "author": "did:cl:main:reviewer3", "payload": {"bounty_id": "blake3:...", "result": "approve", "quality": 0.95}}
```

**Step 6: Complete.**

```json
{
  "type": "bounty.complete",
  "author": "did:cl:main:reviewer1",
  "payload": {
    "bounty_id": "blake3:...",
    "verified_by": ["did:cl:main:reviewer1", "did:cl:main:reviewer2", "did:cl:main:reviewer3"],
    "average_quality": 0.9
  }
}
```

**Step 7: Pay.**

```json
{
  "type": "payment.record",
  "author": "did:cl:escrow:main:123",
  "payload": {
    "bounty_id": "blake3:...",
    "recipient": "did:cl:main:alice",
    "amount": 500,
    "currency": "USD",
    "method": "stripe",
    "external_ref": "tr_...",
    "status": "settled"
  }
}
```

**Step 8: Contribution.**

```json
{
  "type": "contribution.create",
  "author": "did:cl:main:alice",
  "payload": {
    "subject": "did:cl:main:alice",
    "issuer": "did:cl:org:startupX",
    "action": "bounty_completion",
    "context": "repo:x/y",
    "weight_class": "bounty_doc",
    "metadata": {"bounty_id": "blake3:..."}
  }
}
```

### 18.2. Disputed bounty

Worker submits; verifiers reject; worker disputes.

1. `bounty.submit` by Alice.
2. `bounty.verify` by reviewer1: reject.
3. `bounty.verify` by reviewer2: reject.
4. `bounty.dispute` by Alice.
5. 3 arbiters selected.
6. Arbiters review.
7. Votes: favor_worker, favor_worker, split.
8. `bounty.resolve` with `favor_worker`.
9. Escrow releases full payment to Alice.
10. CU awarded per resolution.

### 18.3. Multi-milestone bounty

Three milestones, each verified separately.

- m1 completed → $500 released.
- m2 completed → $3000 released.
- m3 completed → $1500 released.

Total: $5000 to worker.

### 18.4. Auto-approval

Worker submits. No verifier responds within 7 days.

Auto-approval triggers. Escrow releases funds.

### 18.5. Expiration

Worker claims, does not submit within deadline.

Bounty expires. Escrow refunds issuer. Worker's reputation slightly penalized.

---

## 19. Test Vectors

Test vectors for bounties live in `spec/test-vectors/bounties.json`.

### 19.1. Coverage

- Bounty creation with all fields.
- Escrow funding.
- Claim with eligibility checks.
- Submission with evidence.
- Verification with multiple verifiers.
- Completion and payment.
- Cancellation (before claim, mutual, arbitration).
- Expiration.
- Dispute (all reasons).
- Arbitration (all outcomes).
- Multi-milestone.
- Auto-approval.
- Invalid cases: unfunded claim, ineligible worker, late submission, insufficient verifications.

### 19.2. Format

```json
{
  "description": "Simple bounty completion",
  "events": [
    {"type": "bounty.create", ...},
    {"type": "bounty.fund", ...},
    {"type": "bounty.claim", ...},
    {"type": "bounty.submit", ...},
    {"type": "bounty.verify", ...},
    {"type": "bounty.complete", ...},
    {"type": "payment.record", ...}
  ],
  "expected_final_state": "completed",
  "expected_payment": {"amount": 500, "recipient": "did:cl:main:alice"}
}
```

### 19.3. Determinism

All events **MUST** produce deterministic IDs and signatures.

### 19.4. Cross-implementation

Test vectors **MUST** pass on at least two implementations before v1.0.

---

## 20. Open Questions

- Should escrow be **per-context** or global?
- How to handle **cross-currency** bounties (issuer in USD, worker in EUR)?
- Should there be a **protocol-level escrow** or only external rails?
- How to handle **partial payments** when work is incomplete?
- Should **arbitration fees** be paid by the loser or split?
- How to prevent **arbiter collusion**?
- Should there be a **maximum dispute period**?
- How to handle **multi-party bounties** (multiple workers on one task)?
- Should **reputation thresholds** for claiming be enforced by protocol or context?
- How to handle **cross-context bounties** (posted in one context, claimed in another)?
- Should **evidence** be stored on-chain or only referenced?
- How to handle **evidence that becomes unavailable** (dead links)?
- Should there be a **bounty registry** for discovery?
- How to handle **AI-generated work** (was it done by a human or a model)?
- Should **verification** be open (anyone can verify) or gated (roles only)?

These will be resolved through RFCs and community discussion.

---

## Summary

**A bounty is:**

- A paid task.
- Funded upfront via escrow.
- Claimed by a worker.
- Verified by peers.
- Paid on completion.
- Recorded as a contribution.

**Lifecycle:**

```
draft → open → claimed → submitted → verified → completed
         │                 │           │
         │                 │           └──→ disputed → resolved
         │                 └──→ disputed → resolved
         └──→ cancelled
```

**Escrow:**

- Funds held upfront.
- Released on verification.
- Refunded on cancellation.
- Frozen during disputes.

**Verification:**

- Threshold of confirmations.
- Quality coefficient.
- Auto-approval fallback.
- Arbitration for disputes.

**Payment:**

- Fiat (Stripe, Wise, bank).
- Stablecoins (USDC, USDT, DAI).
- Crypto (optional).
- In-kind (access, services).

**CU and reputation:**

- Worker earns CU on completion.
- Issuer earns small CU for posting.
- Verifiers earn CU for verification.
- Arbiters earn CU for arbitration.
- Decay applies.

**Anti-abuse:**

- Escrow required.
- Reputation gates.
- Evidence verification.
- Arbitration.
- Rate limits.
- Reputation penalties.

**Key insight:**

Bounties are **the market mechanism of CL**. They turn contributions into income, and income into reputation. Everything else (grants, cooperatives, compute) is a variation on this theme.

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [identity.md](./identity.md) — identity model.
- [contribution.md](./contribution.md) — contribution records.
- [reputation.md](./reputation.md) — reputation calculation.
- [consensus.md](./consensus.md) — finalization.
- [vote.md](./vote.md) — governance votes.
- [compute.md](./compute.md) — compute tasks (similar to bounties).
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
