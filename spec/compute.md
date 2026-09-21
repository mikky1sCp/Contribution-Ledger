# Compute

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md) · [identity.md](./identity.md) · [contribution.md](./contribution.md) · [reputation.md](./reputation.md) · [bounty.md](./bounty.md)  
**Related:** [consensus.md](./consensus.md) · [sync.md](./sync.md) · [api.md](./api.md) · [privacy.md](./privacy.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [Why Not Mining](#3-why-not-mining)
4. [The Three Rules](#4-the-three-rules)
5. [Compute Task Types](#5-compute-task-types)
6. [Task Lifecycle](#6-task-lifecycle)
7. [Task Creation](#7-task-creation)
8. [Task Claiming and CU Staking](#8-task-claiming-and-cu-staking)
9. [Submission](#9-submission)
10. [Verification](#10-verification)
11. [Payment](#11-payment)
12. [Disputes and Arbitration](#12-disputes-and-arbitration)
13. [CU and Reputation](#13-cu-and-reputation)
14. [Executor Registration](#14-executor-registration)
15. [Pricing](#15-pricing)
16. [Anti-Abuse](#16-anti-abuse)
17. [Phases and Scaling](#17-phases-and-scaling)
18. [Validation Rules](#18-validation-rules)
19. [Examples](#19-examples)
20. [Test Vectors](#20-test-vectors)
21. [Open Questions](#21-open-questions)

---

## 1. Overview

**Compute tasks** are paid work that uses CPU, GPU, or specialized hardware. They are the CL answer to mining: instead of burning energy on hashes, participants run useful computations for real clients.

Compute tasks are structurally similar to [bounties](./bounty.md):

- an issuer posts a task with a reward;
- funds are escrowed;
- a participant claims the task;
- the participant runs the computation and submits a result;
- verifiers check the result;
- escrow releases payment;
- a contribution record is created;
- CU and reputation are awarded.

The differences are:

- **task format** — machine-readable specification (not free-form text);
- **verification** — often automated (metrics, hashes, tests);
- **staking** — executors stake CU to claim high-value tasks;
- **hardware attestation** — optional proof of hardware capabilities;
- **redundancy** — tasks may be run by multiple executors.

**This file defines:**

- Why compute is not mining (Section 3).
- The three rules that keep compute non-speculative (Section 4).
- Types of compute tasks (Section 5).
- The full lifecycle (Section 6).
- Task creation format (Section 7).
- Claiming with CU staking (Section 8).
- Submission format (Section 9).
- Verification methods (Section 10).
- Payment (Section 11).
- Disputes (Section 12).
- CU and reputation (Section 13).
- Executor registration and attestation (Section 14).
- Pricing (Section 15).
- Anti-abuse (Section 16).
- Phases and scaling (Section 17).
- Validation rules (Section 18).

This file is the technical counterpart to [docs/useful-work.md](../docs/useful-work.md), which explains the concept. Here we define the protocol.

---

## 2. Design Principles

### 2.1. Useful work, not wasted hashes

Every compute task produces a result that someone needs:

- a trained model;
- an inference output;
- a rendered frame;
- a simulation result;
- a labeled dataset;
- a proof.

If the result is not needed, the task does not exist.

### 2.2. Money from outside

The task issuer pays in fiat or stablecoin. The protocol does not print money. CU is awarded as reputation, not as payment.

See [docs/economics.md](../docs/economics.md) for the economic model.

### 2.3. Verified results, not time online

Payment and CU are awarded only for **verified results**, not for:

- connecting a GPU;
- claiming to run a task;
- being online;
- staking.

Verification is the gate.

### 2.4. CU staking (not money staking)

Executors stake **CU**, not money, to claim high-value tasks.

CU is non-transferable (see [contribution.md](./contribution.md)). Staking:

- signals commitment;
- provides a penalty for fraud;
- does not create a financial barrier to entry.

### 2.5. Redundancy where it matters

Not all tasks require redundant execution. Redundancy scales with task value:

- low-value tasks: 1 executor, sampling;
- medium-value: 3 executors, comparison;
- high-value: 5 executors, full verification.

The redundancy level is set by the issuer or the context.

### 2.6. No token

There is no compute token. There is no mining reward. There is no emission.

Payment comes from the issuer. CU comes from verified work.

### 2.7. Hardware-agnostic

The protocol does not require specific hardware. Any executor that can run the task is eligible.

Hardware attestation is optional and used only where needed.

### 2.8. Federated

Compute tasks are scoped to a context. Different contexts may have different rules, verification methods, and pricing.

### 2.9. Privacy-aware

Some tasks involve sensitive data (medical, financial, personal). The protocol supports:

- encrypted inputs;
- trusted execution environments (TEEs);
- zero-knowledge verification;
- privacy-preserving aggregation.

### 2.10. Fail-safe

If verification fails or is inconclusive:

- the task goes to arbitration;
- funds are frozen;
- a decision is made by humans.

The protocol does not pretend to solve verification perfectly. It provides layers.

---

## 3. Why Not Mining

### 3.1. Mining produces nothing useful

Proof-of-Work mining:

- consumes ~150 TWh/year globally;
- produces heat and hash collisions;
- secures a network whose only product is money.

The work is deliberately useless. That is the point: useless work is hard to fake.

### 3.2. CL's alternative

CL replaces mining with tasks that:

- have a verifiable result;
- are paid by a real client;
- produce value outside the protocol.

Same hardware. Same energy. Different output.

### 3.3. Comparison

| | Mining | Compute Task |
|---|---|---|
| Output | Hashes | Model, render, simulation |
| Who needs it | No one | Client, researcher, studio |
| Who pays | Protocol (emission) | Client (money) |
| Energy | Wasted | Used |
| Value created | None | Real |
| Environmental cost | High | Low |
| Profit source | Token price | Client payment |
| CU awarded | No | Yes (reputation) |
| Verification | Hash puzzle | Result verification |

### 3.4. What CL does not do

- CL does **not** pay for hash power.
- CL does **not** reward time online.
- CL does **not** emit tokens for compute.
- CL does **not** create a "mining" economy.
- CL does **not** allow CU to be exchanged for money.

---

## 4. The Three Rules

These rules are non-negotiable. They distinguish CL from every compute-token project.

### 4.1. Rule 1: CU awarded only for verified results

Not for time online. Not for "connected GPU". Not for "claimed hash rate".

**For a result that passes verification.**

Examples:

- ❌ "Connected GPU for 1 hour → 10 CU."
- ✅ "Trained model, achieved accuracy 0.92, verified → 50 CU."

### 4.2. Rule 2: Task issuer pays in money

The client pays in fiat or stablecoin. Money goes to the executor. CU is a reputation bonus, not the payment.

This means:

- profit comes from a real customer;
- there is no emission;
- there is no inflation;
- the economy is funded by demand, not by speculation.

### 4.3. Rule 3: CU cannot be exchanged for money

Not directly. Not indirectly. Not through a wrapper.

CU only becomes money through:

- **Cooperative payouts** — by community rules, proportional to CU.
- **Nothing else.**

This removes the incentive to farm CU and sell it. It makes CU a signal of contribution, not a financial asset.

### 4.4. Enforcement

Violations of these rules:

- are rejected by validators;
- invalidate the task;
- result in reputation penalties;
- may result in removal from the context.

---

## 5. Compute Task Types

### 5.1. Categories

| Category | Description |
|---|---|
| **Training** | Train or fine-tune a model. |
| **Inference** | Run a model on inputs. |
| **Labeling** | Annotate data. |
| **Rendering** | Render 3D scenes, video, graphics. |
| **Simulation** | Run scientific, engineering, or financial simulations. |
| **Data processing** | ETL, cleaning, transformation. |
| **Indexing** | Build search indexes, analytics. |
| **Proof generation** | Generate ZK proofs, cryptographic proofs. |
| **Verification** | Verify computations, signatures. |
| **Batch jobs** | Any task that fits the format. |

### 5.2. Task kinds

Each task declares a `kind`:

```json
"kind": "model_training"
```

Allowed values:

- `model_training`
- `model_finetuning`
- `inference`
- `data_labeling`
- `rendering`
- `simulation`
- `data_processing`
- `indexing`
- `proof_generation`
- `batch`
- `custom` (with `kind_spec`).

### 5.3. Task specification

The task's `task` object contains:

- `kind` — the type;
- `input` — input data (hash, URI, or inline);
- `parameters` — kind-specific parameters;
- `output` — expected output format;
- `constraints` — hardware, time, cost constraints.

### 5.4. Examples

**Model training:**

```json
{
  "kind": "model_training",
  "input": {
    "dataset": "ipfs://Qm...",
    "base_model": "ipfs://Qm...",
    "architecture": "transformer"
  },
  "parameters": {
    "epochs": 10,
    "batch_size": 32,
    "learning_rate": 0.0001,
    "optimizer": "adam"
  },
  "output": {
    "type": "model_weights",
    "format": "safetensors",
    "target_metric": {"name": "accuracy", "value": 0.92}
  },
  "constraints": {
    "max_runtime_sec": 3600,
    "gpu_min_vram_gb": 12,
    "max_cost_usd": 50
  }
}
```

**Inference:**

```json
{
  "kind": "inference",
  "input": {
    "model": "ipfs://Qm...",
    "batch": "ipfs://Qm...",
    "count": 1000
  },
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 512
  },
  "output": {
    "type": "inference_results",
    "format": "jsonl"
  },
  "constraints": {
    "max_runtime_sec": 600,
    "gpu_min_vram_gb": 8
  }
}
```

**Rendering:**

```json
{
  "kind": "rendering",
  "input": {
    "scene": "ipfs://Qm...",
    "frame_range": [0, 100]
  },
  "parameters": {
    "resolution": "1920x1080",
    "samples": 128,
    "engine": "cycles"
  },
  "output": {
    "type": "frames",
    "format": "png_sequence"
  },
  "constraints": {
    "max_runtime_sec": 7200,
    "gpu_min_vram_gb": 8
  }
}
```

### 5.5. Custom kinds

For custom task kinds, the issuer **MUST** provide:

- `kind_spec` — a URI to the specification;
- `verification_method` — how the result is verified.

Custom kinds **MAY** be rejected by validators if the verification method is not supported.

---

## 6. Task Lifecycle

### 6.1. States

```
draft → open → claimed → submitted → verified → completed
         │         │           │
         │         │           └──→ disputed → resolved
         │         └──→ disputed → resolved
         └──→ cancelled
```

| State | Description |
|---|---|
| `draft` | Created locally, not yet funded. |
| `open` | Funded, visible, claimable. |
| `claimed` | Claimed by an executor. |
| `submitted` | Executor submitted a result. |
| `verified` | Verifiers approved the result. |
| `completed` | Payment released, CU awarded. |
| `disputed` | Dispute opened. |
| `resolved` | Dispute resolved. |
| `cancelled` | Cancelled before claim. |
| `expired` | Deadline passed without completion. |

### 6.2. Transitions

**draft → open:**
- Escrow funded.
- Task format validated.

**open → claimed:**
- An executor claims the task.
- CU staked (if required).
- Claim meets eligibility.

**claimed → submitted:**
- Executor submits a result with evidence.
- Before or at deadline.

**submitted → verified:**
- Verification threshold met.

**submitted → disputed:**
- Either party opens a dispute.

**verified → completed:**
- Payment released.
- CU awarded.

**open → cancelled:**
- Issuer cancels before claim.

**claimed → expired:**
- Deadline passed, no submission.
- Escrow refunded (or partially).
- Executor's CU stake returned (or slashed on fraud).

### 6.3. Terminal states

- `completed`
- `cancelled`
- `resolved`
- `expired`

### 6.4. Timeline

| Step | Typical duration |
|---|---|
| Draft → open (funding) | Minutes |
| Open → claimed | Seconds to hours |
| Claimed → submitted | Per constraints |
| Submitted → verified | Minutes to hours |
| Verified → completed | Minutes |

Disputes add 3–14 days.

---

## 7. Task Creation

### 7.1. Prerequisites

To create a compute task, the issuer **MUST**:

- be a Level 2+ identity;
- have reputation ≥ threshold in the context (if required);
- have funds to escrow;
- provide a valid task specification.

### 7.2. Creation event

```json
{
  "version": 1,
  "type": "compute.task.create",
  "author": "did:cl:org:ailab",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "task": {
      "kind": "model_training",
      "input": {
        "dataset": "ipfs://Qm...",
        "base_model": "ipfs://Qm..."
      },
      "parameters": {
        "epochs": 10,
        "batch_size": 32
      },
      "output": {
        "type": "model_weights",
        "target_metric": {"name": "accuracy", "value": 0.92}
      },
      "constraints": {
        "max_runtime_sec": 3600,
        "gpu_min_vram_gb": 12
      }
    },
    "context": "lab:research",
    "reward": {
      "amount": 50,
      "currency": "USD",
      "method": "escrow"
    },
    "escrow_id": "did:cl:escrow:main:456",
    "deadline": 1730100000,
    "redundancy": 3,
    "verification": "metric_threshold",
    "staking": {
      "required": true,
      "amount_cu": 10
    },
    "weight_class": "compute_training",
    "eligibility": {
      "min_reputation": 100,
      "min_level": 2,
      "gpu_min_vram_gb": 12
    }
  },
  "signature": "ed25519:..."
}
```

### 7.3. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `task` | object | MUST | Task specification. |
| `context` | string | MUST | Context of the task. |
| `reward` | object | MUST | Amount, currency, method. |
| `escrow_id` | string | MUST | Escrow DID. |
| `deadline` | integer | MUST | Unix timestamp. |
| `redundancy` | integer | MUST | Number of redundant runs. |
| `verification` | string | MUST | Verification method. |
| `staking` | object | MAY | CU staking requirement. |
| `weight_class` | string | MUST | CU weight class. |
| `eligibility` | object | MAY | Who can claim. |
| `auto_approve_after` | integer | MAY | Seconds; auto-approval. |

### 7.4. Redundancy

`redundancy` is the number of executors that must produce the same result.

- `1` — single executor, sampling verification.
- `3` — three executors, results compared.
- `5` — five executors, higher confidence.

Redundancy multiplies cost. Use the minimum needed.

### 7.5. Verification method

| Method | Description |
|---|---|
| `hash_match` | Result hash must match a known value. |
| `metric_threshold` | Result metric must meet a threshold. |
| `redundancy` | Multiple executors must agree. |
| `zk_proof` | ZK proof of correct computation. |
| `tee_attestation` | TEE attestation. |
| `manual` | Manual review by verifiers. |
| `hybrid` | Combination. |

The method **MUST** be supported by the context.

### 7.6. Staking

```json
"staking": {
  "required": true,
  "amount_cu": 10
}
```

- `required`: whether staking is required to claim.
- `amount_cu`: CU amount to stake.

Staked CU is:

- returned on successful completion;
- slashed (partially or fully) on proven fraud;
- returned on expiration (unless fraud is suspected).

### 7.7. Eligibility

```json
"eligibility": {
  "min_reputation": 100,
  "min_level": 2,
  "gpu_min_vram_gb": 12,
  "allowed_dids": ["did:cl:main:alice"]
}
```

If absent, defaults apply:

- `min_reputation`: 10;
- `min_level`: 1;
- `gpu_min_vram_gb`: 0.

### 7.8. Validation

On creation:

- The context **MUST** exist.
- `weight_class` **MUST** be defined.
- `verification` **MUST** be supported.
- `redundancy` **MUST** be ≥ 1.
- `deadline` **MUST** be in the future.
- Escrow **MUST** be valid.

### 7.9. Escrow funding

Same as bounties (see [bounty.md](./bounty.md#5-escrow)):

- fiat via Stripe/Wise;
- stablecoins via multisig;
- payment is released on verification.

### 7.10. Activation

Once escrow is funded, the task becomes `open` and visible to eligible executors.

---

## 8. Task Claiming and CU Staking

### 8.1. Eligibility

An executor **MUST**:

- meet eligibility criteria;
- have the required CU to stake (if staking is required);
- have no active claims on the same task;
- have no active disputes.

### 8.2. Claim event

```json
{
  "version": 1,
  "type": "compute.task.claim",
  "author": "did:cl:main:alice",
  "created_at": 1730000100,
  "parents": ["blake3:..."],
  "payload": {
    "task_id": "blake3:...",
    "hardware": {
      "gpu": "RTX 4090",
      "vram_gb": 24,
      "attestation": "optional-tee-proof"
    },
    "stake_cu": 10
  },
  "signature": "ed25519:..."
}
```

### 8.3. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `task_id` | string | MUST | The task event ID. |
| `hardware` | object | MAY | Hardware capabilities. |
| `stake_cu` | number | MAY | CU to stake (if required). |

### 8.4. Staking mechanism

Staking is implemented as:

1. A `compute.stake` event is created by the executor.
2. The staked CU is locked (marked as staked in the ledger).
3. The CU is not available for other uses until the task is resolved.
4. On completion: stake is returned.
5. On fraud: stake is slashed (partially or fully).

### 8.5. Slashing rules

| Outcome | Stake |
|---|---|
| Successful completion | Returned fully |
| Expiration (no fraud) | Returned fully |
| Dispute lost (fraud proven) | Slashed fully |
| Dispute split | Partially slashed (per decision) |
| Task cancelled by issuer | Returned fully |

Slashing is recorded as a `compute.slash` event.

### 8.6. Multiple executors (redundancy)

When `redundancy > 1`:

- multiple executors **MAY** claim the same task;
- each stakes the required CU;
- each submits a result;
- results are compared;
- all correct executors are paid (shared reward);
- incorrect results are slashed.

### 8.7. Claim lock

Once claimed, the task is locked for the claimer(s):

- the issuer cannot cancel without arbitration;
- the executor has until the deadline to submit.

### 8.8. Claim withdrawal

An executor **MAY** withdraw before submitting:

```json
{
  "type": "compute.task.withdraw",
  "payload": {
    "task_id": "blake3:...",
    "reason": "cannot_complete"
  }
}
```

The stake is returned, but repeated withdrawals reduce reputation.

### 8.9. Deadline

If the deadline passes without submission:

- the task enters `expired`;
- the escrow refunds the issuer;
- executors' stakes are returned;
- executor's reputation is slightly penalized (if repeated).

---

## 9. Submission

### 9.1. Submission event

```json
{
  "version": 1,
  "type": "compute.task.submit",
  "author": "did:cl:main:alice",
  "created_at": 1730050000,
  "parents": ["blake3:..."],
  "payload": {
    "task_id": "blake3:...",
    "result_hash": "blake3:...",
    "result_uri": "ipfs://Qm...",
    "metrics": {
      "accuracy": 0.93,
      "loss": 0.12
    },
    "runtime_sec": 2400,
    "hardware": {
      "gpu": "RTX 4090",
      "vram_gb": 24
    },
    "logs_hash": "blake3:..."
  },
  "signature": "ed25519:..."
}
```

### 9.2. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `task_id` | string | MUST | The task event ID. |
| `result_hash` | string | MUST | BLAKE3 hash of the result. |
| `result_uri` | string | MAY | URI to the result (IPFS, S3, etc.). |
| `metrics` | object | MAY | Measured metrics. |
| `runtime_sec` | integer | MAY | Runtime in seconds. |
| `hardware` | object | MAY | Actual hardware used. |
| `logs_hash` | string | MAY | Hash of logs. |

### 9.3. Result storage

Results **MUST** be stored somewhere retrievable:

- IPFS (content-addressed);
- S3-compatible storage;
- Arweave (permanent);
- inline (for small results, base64).

The `result_hash` is the BLAKE3 of the result. The `result_uri` is where it can be retrieved.

### 9.4. Metric verification

For `metric_threshold` verification, the executor **MUST** report the metric:

```json
"metrics": {
  "accuracy": 0.93
}
```

The verifier recomputes or validates the metric.

### 9.5. Multiple submissions

An executor **MAY** submit multiple times (e.g., to fix issues).

Rules:

- the latest submission is used for verification;
- earlier submissions are kept in the ledger.

### 9.6. Redundant submissions

If `redundancy > 1`, each executor submits independently.

The verifier compares:

- `result_hash` (must match);
- `metrics` (within tolerance);
- `runtime_sec` (within tolerance).

If results match, all correct executors are paid.

### 9.7. Result encoding

Results **MUST** be:

- deterministic (same input → same output);
- canonical (no platform-specific variations);
- hashed with BLAKE3.

For non-deterministic computations (e.g., ML training with randomness), the task **MUST** specify a seed or tolerance.

---

## 10. Verification

### 10.1. Verification methods

| Method | Use case |
|---|---|
| `hash_match` | Deterministic computations (rendering, simulation). |
| `metric_threshold` | ML training, inference quality. |
| `redundancy` | Any computation, via multiple executors. |
| `zk_proof` | Verifiable computation (where feasible). |
| `tee_attestation` | Trusted hardware execution. |
| `manual` | Human review (for subjective tasks). |
| `hybrid` | Combination of above. |

### 10.2. Hash match

For deterministic tasks:

1. Issuer provides `expected_hash` (or a reference implementation).
2. Executor submits `result_hash`.
3. Verifier compares.
4. If match: verified.
5. If mismatch: rejected.

**Problem:** deterministic tasks may still have platform-specific differences (floating point, CPU instructions). Issuer **MUST** specify the environment.

### 10.3. Metric threshold

For ML tasks:

1. Issuer provides `target_metric`.
2. Executor submits `metrics`.
3. Verifier runs the model on a held-out test set (or uses a pre-computed result).
4. If metric meets or exceeds target: verified.

**Anti-gaming:**

- test set is not shared with the executor;
- multiple metrics (not just one);
- adversarial examples.

### 10.4. Redundancy

For any task:

1. Multiple executors run the same task.
2. Results are compared.
3. If they match (within tolerance): verified.
4. If they differ: dispute.

**Cost:** redundancy multiplies cost by the redundancy factor.

### 10.5. ZK proof

For verifiable computations:

1. Executor runs the computation.
2. Executor generates a ZK proof of correct execution.
3. Verifier checks the proof.

**Use case:** tasks where the input is private, or the computation is expensive to re-run.

### 10.6. TEE attestation

For trusted hardware:

1. Executor runs the computation inside a TEE (SGX, SEV).
2. Executor provides an attestation.
3. Verifier checks the attestation.

**Trust assumption:** the TEE manufacturer.

### 10.7. Manual review

For subjective tasks:

1. Executor submits the result.
2. Verifiers review manually.
3. Verifiers vote: approve or reject.

**Use case:** creative tasks, quality assessment.

### 10.8. Hybrid verification

Combining methods:

- hash match + sampling;
- metric threshold + redundancy;
- ZK + TEE.

The issuer specifies the combination in `verification`.

### 10.9. Verification event

```json
{
  "version": 1,
  "type": "compute.task.verify",
  "author": "did:cl:main:verifier1",
  "created_at": 1730050100,
  "parents": ["blake3:..."],
  "payload": {
    "task_id": "blake3:...",
    "result": "valid",
    "method": "metric_threshold",
    "metrics_verified": {"accuracy": 0.93},
    "comment": "Metric met, model checked."
  },
  "signature": "ed25519:..."
}
```

### 10.10. Verification threshold

The task is completed when:

- the verification threshold is met (e.g., 2 of 3 verifiers agree);
- the metric meets the target;
- no rejection is registered.

### 10.11. Verifier selection

Verifiers **MUST**:

- have reputation ≥ `min_reputation`;
- be eligible for the context;
- not be the executor;
- not be the issuer (unless allowed).

For redundancy tasks, verifiers **MAY** be selected randomly.

### 10.12. Automated verifiers

Some verifiers **MAY** be automated:

- CI systems (run tests);
- metric evaluators (compute accuracy);
- hash checkers.

Automated verifiers **MUST** be signed by a system identity.

### 10.13. Verification window

Verifiers **MUST** submit within a window (e.g., 24 hours).

If no verification occurs:

- auto-approval triggers (if set);
- or the task goes to arbitration.

### 10.14. Auto-approval

If `auto_approve_after` is set, and no rejection or dispute occurs within the window:

- the task is auto-approved;
- payment is released;
- CU is awarded.

### 10.15. Rejection

If verification rejects:

- the task returns to `claimed` (if time remains);
- or goes to dispute.

The executor's CU stake is frozen during dispute.

### 10.16. Verification transparency

All verification events are on-ledger. Anyone can audit.

---

## 11. Payment

### 11.1. Completion

On verified completion:

1. A `compute.task.complete` event is created.
2. Escrow releases funds.
3. A `payment.record` is created.
4. A `contribution.create` event is created.
5. CU and reputation are awarded.

### 11.2. Payment event

```json
{
  "type": "payment.record",
  "author": "did:cl:escrow:main:456",
  "payload": {
    "task_id": "blake3:...",
    "recipient": "did:cl:main:alice",
    "amount": 50,
    "currency": "USD",
    "method": "stripe",
    "external_ref": "tr_...",
    "status": "settled",
    "reward_share": 1.0
  }
}
```

### 11.3. Reward sharing (redundancy)

If `redundancy > 1`, the reward is split:

- correct executors share the reward equally;
- incorrect executors receive nothing (and may be slashed).

Example: $50 reward, 3 executors, 2 correct → each gets $25.

### 11.4. Escrow fees

Escrow **MAY** charge a fee (0.5–2%). Recorded in the payment.

### 11.5. Payment rails

Same as bounties (see [bounty.md](./bounty.md#13-payment-rails)):

- fiat (Stripe, Wise, bank);
- stablecoins (USDC, USDT, DAI);
- crypto (optional).

### 11.6. Failure to pay

If escrow does not release funds within 24 hours:

- executor may open a dispute;
- escrow provider is penalized in reputation;
- community may intervene.

### 11.7. Partial payments

For multi-stage tasks (e.g., training with checkpoints), partial payments **MAY** be released per stage.

---

## 12. Disputes and Arbitration

### 12.1. When disputes occur

- executor believes result is correct, but verification rejects;
- issuer believes result is incorrect, but verification approves;
- disagreement on metric or hash;
- escrow does not release funds.

### 12.2. Opening a dispute

```json
{
  "type": "compute.task.dispute",
  "author": "did:cl:main:alice",
  "payload": {
    "task_id": "blake3:...",
    "reason": "result_rejected_unfairly",
    "evidence": [
      {"type": "link", "value": "ipfs://Qm..."},
      {"type": "hash", "algo": "blake3", "value": "..."}
    ]
  }
}
```

### 12.3. Dispute process

Same as bounties:

1. Dispute opened.
2. 3 arbiters selected.
3. Arbiters review evidence.
4. Vote: favor executor / favor issuer / split.
5. Decision final.

### 12.4. Re-execution

For disputes about results, arbiters **MAY** re-run the computation:

- on their own hardware;
- or by assigning to a trusted verifier.

If re-execution matches the executor's result: executor wins.

If re-execution matches the issuer's claim: issuer wins.

### 12.5. Slashing on dispute

If executor is proven fraudulent:

- CU stake is slashed;
- reputation is penalized;
- executor may be banned from future tasks.

### 12.6. Appeals

Appeals possible (same as bounties).

### 12.7. Dispute timeouts

- Arbiters must vote within 7 days.
- Default split 50/50 if no decision.

---

## 13. CU and Reputation

### 13.1. CU on completion

On successful completion, the executor earns CU:

```
CU = weight_class_value × quality × decay
```

Where:

- `weight_class_value` is from the context's rules for the task's `weight_class`;
- `quality` is derived from verification (1.0 if approved, lower if partial);
- `decay` is 1.0 for new contributions.

### 13.2. Weight classes

Suggested weight classes:

| Weight class | Typical CU |
|---|---|
| `compute_labeling` | 1–5 |
| `compute_rendering` | 2–10 |
| `compute_simulation` | 5–20 |
| `compute_inference` | 3–15 |
| `compute_training` | 20–100 |
| `compute_proof` | 5–30 |

Contexts **MAY** define their own.

### 13.3. Reputation

CU from compute tasks contributes to the executor's reputation in the context.

### 13.4. Issuer reputation

Issuers earn small CU for posting completed tasks:

```
CU_issuer = task_issuer_weight × completion_factor
```

Where `completion_factor` is:

- 1.0 if completed;
- 0.5 if disputed;
- 0 if cancelled.

### 13.5. Verifier reputation

Verifiers earn CU:

```
CU_verifier = verification_weight × agreement_factor
```

Where `agreement_factor` is:

- 1.0 if the verifier's vote matched the outcome;
- 0.5 otherwise.

### 13.6. Slashing

Slashing reduces CU:

```json
{
  "type": "compute.slash",
  "payload": {
    "task_id": "blake3:...",
    "executor": "did:cl:main:alice",
    "amount_cu": 10,
    "reason": "fraud",
    "evidence": [...]
  }
}
```

Slashed CU is:

- deducted from the executor's CU in the context;
- NOT transferred to the issuer (burned, to avoid incentive to falsely accuse);
- recorded on-ledger.

### 13.7. Decay

CU from compute tasks decays per the context's rules (see [reputation.md](./reputation.md#6-decay-function)).

### 13.8. Snapshot for disputes

For disputes involving reputation thresholds, the reputation at the time of the dispute **MUST** be used.

### 13.9. Cross-context recognition

CU from one context **MAY** be recognized by another, per [reputation.md](./reputation.md#8-aggregation-across-contexts).

---

## 14. Executor Registration

### 14.1. Purpose

Executors **MAY** register their capabilities to be discoverable by issuers.

### 14.2. Registration event

```json
{
  "type": "compute.executor.register",
  "author": "did:cl:main:alice",
  "payload": {
    "hardware": {
      "cpu": "AMD Ryzen 9 7950X",
      "cpu_cores": 16,
      "ram_gb": 64,
      "gpus": [
        {"model": "RTX 4090", "vram_gb": 24, "count": 1}
      ]
    },
    "software": {
      "os": "Ubuntu 22.04",
      "cuda": "12.1",
      "docker": true
    },
    "availability": {
      "hours_per_week": 40,
      "timezone": "UTC+3"
    },
    "attestation": {
      "type": "tee",
      "proof": "optional"
    }
  },
  "signature": "ed25519:..."
}
```

### 14.3. Attestation

Executors **MAY** provide hardware attestation:

- **TEE** (SGX, SEV) for trusted execution;
- **Signed hardware IDs** for provenance;
- **Benchmark results** for performance verification.

Attestation is optional. Not all tasks require it.

### 14.4. Benchmarking

Executors **MAY** submit benchmark results:

```json
{
  "type": "compute.executor.benchmark",
  "payload": {
    "benchmark": "resnet50_inference",
    "result": {"throughput": 1000, "unit": "images/sec"}
  }
}
```

Benchmarks help issuers estimate runtime and cost.

### 14.5. Deregistration

An executor **MAY** deregister:

```json
{
  "type": "compute.executor.deregister",
  "payload": {
    "reason": "no_longer_available"
  }
}
```

### 14.6. Registration is not required

Registration is optional. Executors **MAY** claim tasks without registering.

Registration is a discovery tool, not a gate.

---

## 15. Pricing

### 15.1. Set by issuer

Prices are set by the task issuer, not by the protocol.

### 15.2. Typical rates

| Task | Rate |
|---|---|
| Moderation hour | $5–15 |
| Translation (1000 words) | $10–30 |
| GPU hour (consumer) | $0.10–0.50 |
| GPU hour (datacenter) | $1–5 |
| CPU hour | $0.01–0.10 |
| AI training (small) | $50–500 |
| AI training (large) | $500–5000 |
| Inference (1000 requests) | $0.50–5 |
| Dataset labeling (1000 items) | $5–100 |
| Rendering (frame) | $0.10–2 |
| Simulation (run) | $1–100 |

### 15.3. Factors

- **Hardware** — GPU generation, VRAM.
- **Verification** — heavier verification costs more.
- **Urgency** — deadlines increase price.
- **Trust** — new executors may need to offer lower prices.
- **Market** — supply and demand.

### 15.4. Comparison to hyperscalers

| Provider | A100 hour |
|---|---|
| AWS | $3–5 |
| GCP | $3–4 |
| Azure | $3–5 |
| CL | $1–5 |

CL is competitive for:

- small or intermittent tasks;
- clients who value verifiability;
- open-source and research workloads.

CL is not competitive for:

- massive continuous workloads;
- latency-critical inference;
- compliance-heavy enterprise use.

### 15.5. Fees

- **Escrow fee:** 0.5–2%.
- **Protocol fee:** 0% (there is no protocol fee).
- **Arbitration fee:** only if dispute.

### 15.6. Currency

Prices are set in a currency (`USD`, `USDC`, `EUR`). Conversion happens at payment time.

---

## 16. Anti-Abuse

### 16.1. Sybil attacks

**Threat:** fake executors claim tasks, submit garbage, get paid.

**Defense:**

- reputation thresholds;
- CU staking;
- identity level requirements;
- attestation;
- redundancy;
- sampling.

### 16.2. Fake results

**Threat:** executor submits a plausible but incorrect result.

**Defense:**

- hash match (deterministic tasks);
- metric verification (ML);
- redundancy (multiple executors);
- ZK proofs;
- TEE attestation.

### 16.3. Result plagiarism

**Threat:** executor copies another's result.

**Defense:**

- unique nonces in inputs;
- random seeds;
- content analysis.

### 16.4. Metric gaming

**Threat:** executor games the metric (e.g., overfits to a leaked test set).

**Defense:**

- held-out test sets (not shared);
- multiple metrics;
- adversarial evaluation.

### 16.5. Bot farms

**Threat:** one operator runs many fake executors.

**Defense:**

- hardware fingerprinting;
- IP analysis;
- CU staking per identity;
- graph analysis.

### 16.6. Task flooding

**Threat:** spam tasks to drain verification.

**Defense:**

- task creation fee (in CU);
- reputation threshold for issuers;
- rate limits.

### 16.7. Collusion

**Threat:** issuer and executor collude to fake results and split payment.

**Defense:**

- escrow audited by third parties;
- random verifier selection;
- redundancy with independent executors;
- public records.

### 16.8. CU staking abuse

**Threat:** executors stake CU, then withdraw before submission.

**Defense:**

- staking locked until task resolution;
- reputation penalty for withdrawal;
- reduced claim priority.

### 16.9. Verification collusion

**Threat:** verifiers approve fraudulent results.

**Defense:**

- random verifier selection;
- verifier accountability (slashing);
- multiple verifiers required;
- arbitration fallback.

### 16.10. No perfect defense

No verification method is perfect. The goal is to make fraud expensive, not impossible.

---

## 17. Phases and Scaling

### 17.1. Phase 1 — Community help

10–100 members.

- Moderation, translation, documentation.
- No compute hardware.
- Simple verification.
- First CU awarded.

### 17.2. Phase 2 — Small compute

100–500 members.

- Rendering, simulation, test runs.
- Simple scheduler.
- Redundancy-based verification.
- First paying clients.

### 17.3. Phase 3 — AI and large compute

1000+ members, 50+ GPUs.

- Model training, fine-tuning, inference at scale.
- Distributed scheduler (Ray, Kubernetes).
- Advanced verification (ZK, TEE).
- Real AI clients.

### 17.4. Why the order matters

- Verification must work at small scale before scaling.
- Reputation must be built before trust.
- Clients must exist before hardware.

### 17.5. Scaling considerations

- **Throughput:** number of tasks per second.
- **Latency:** task-to-result time.
- **Storage:** results must be stored somewhere.
- **Bandwidth:** large inputs and outputs.
- **Cost:** verification overhead.

---

## 18. Validation Rules

Nodes **MUST** enforce these rules for compute-related events.

### 18.1. `compute.task.create` rules

- Context **MUST** exist.
- `weight_class` **MUST** be defined.
- `verification` **MUST** be supported.
- `redundancy` **MUST** be ≥ 1.
- `deadline` **MUST** be in the future.
- Escrow **MUST** be valid.
- Issuer **MUST** be Level 2+.

### 18.2. `compute.task.claim` rules

- Task **MUST** be `open`.
- Claimer **MUST** meet eligibility.
- Claimer **MUST** have stake CU (if required).
- Claimer **MUST NOT** have an active claim on the same task.

### 18.3. `compute.task.submit` rules

- Task **MUST** be `claimed`.
- Submitter **MUST** be the claimer.
- Submission **MUST** be before deadline.
- `result_hash` **MUST** be valid.

### 18.4. `compute.task.verify` rules

- Task **MUST** be `submitted`.
- Verifier **MUST** meet verification criteria.
- Verifier **MUST NOT** be the executor.
- Verifier **MUST NOT** have already verified.

### 18.5. `compute.task.complete` rules

- Task **MUST** be `submitted`.
- Verification threshold **MUST** be met.
- Metric **MUST** meet target (if applicable).

### 18.6. `compute.slash` rules

- Fraud **MUST** be proven.
- Slashing **MUST** be authorized.
- Amount **MUST NOT** exceed the stake.

### 18.7. Determinism

All compute task IDs, hashes, and signatures **MUST** be deterministic.

### 18.8. Result verification

- `result_hash` **MUST** match the canonical hash of the result.
- Metrics **MUST** be validated by verifiers.

### 18.9. Redundancy

- If `redundancy > 1`, all executors' results **MUST** be compared.
- Matching results → all paid.
- Mismatch → dispute.

### 18.10. Staking

- Staked CU **MUST** be locked until resolution.
- Slashing **MUST** be recorded.

---

## 19. Examples

### 19.1. Simple rendering task

**Creation:**

```json
{
  "type": "compute.task.create",
  "author": "did:cl:org:studio",
  "payload": {
    "task": {
      "kind": "rendering",
      "input": {"scene": "ipfs://Qm..."},
      "parameters": {"resolution": "1920x1080", "samples": 128},
      "output": {"type": "frames", "format": "png_sequence"}
    },
    "context": "studio:render",
    "reward": {"amount": 10, "currency": "USD", "method": "escrow"},
    "escrow_id": "did:cl:escrow:main:789",
    "deadline": 1730100000,
    "redundancy": 1,
    "verification": "hash_match",
    "weight_class": "compute_rendering"
  }
}
```

**Claim, submit, verify:**

1. Alice claims.
2. Alice renders, submits `result_hash`.
3. Verifier checks hash.
4. Match → complete.
5. Payment: $10 to Alice.
6. CU awarded.

### 19.2. Model training with redundancy

**Creation:**

```json
{
  "type": "compute.task.create",
  "payload": {
    "task": {
      "kind": "model_training",
      "input": {"dataset": "ipfs://Qm...", "base_model": "ipfs://Qm..."},
      "parameters": {"epochs": 10},
      "output": {"target_metric": {"name": "accuracy", "value": 0.92}}
    },
    "reward": {"amount": 100, "currency": "USD"},
    "redundancy": 3,
    "verification": "metric_threshold",
    "staking": {"required": true, "amount_cu": 20}
  }
}
```

**Claims:** Alice, Bob, Carol.

**Submissions:**

- Alice: accuracy 0.93.
- Bob: accuracy 0.91.
- Carol: accuracy 0.93.

**Verification:**

- Alice and Carol meet target (0.92).
- Bob does not (0.91).

**Outcome:**

- Alice and Carol are paid ($50 each).
- Bob is not paid; his stake is returned (no fraud, just underperformed).
- Alice and Carol earn CU; Bob earns none.

### 19.3. ZK proof task

**Creation:**

```json
{
  "type": "compute.task.create",
  "payload": {
    "task": {
      "kind": "proof_generation",
      "input": {"circuit": "ipfs://Qm...", "witness": "ipfs://Qm..."},
      "output": {"type": "zk_proof", "format": "groth16"}
    },
    "reward": {"amount": 5, "currency": "USD"},
    "verification": "zk_proof",
    "weight_class": "compute_proof"
  }
}
```

**Submission:** Alice generates the proof.

**Verification:** Verifier checks the proof.

**Completion:** Alice paid.

### 19.4. Dispute over metric

**Scenario:** Executor submits accuracy 0.92; verifier recomputes 0.89.

**Dispute:** Executor opens dispute.

**Arbiters:** Re-run the evaluation on a held-out test set.

**Decision:** If the arbiters' result matches the executor's, executor wins. If it matches the verifier's, verifier wins.

### 19.5. Slashing

**Scenario:** Executor submits a result that was copied from another task.

**Detection:** Hash matches an earlier submission.

**Dispute:** Issuer opens.

**Decision:** Fraud proven.

**Slashing:** CU stake slashed; reputation reduced; possible ban.

### 19.6. Auto-approval

**Scenario:** Executor submits; no verifier responds in 24 hours.

**Auto-approval:** Task completed; payment released; CU awarded.

### 19.7. Expiration

**Scenario:** Executor claims but does not submit within deadline.

**Expiration:** Task expired; escrow refunded; stake returned; small reputation penalty.

---

## 20. Test Vectors

Test vectors for compute live in `spec/test-vectors/compute.json`.

### 20.1. Coverage

- Task creation with each `kind`.
- Claim with and without staking.
- Submission with metrics.
- Verification: hash match, metric threshold, redundancy.
- Completion and payment.
- Slashing.
- Disputes.
- Auto-approval.
- Expiration.
- Invalid cases: insufficient stake, missed deadline, wrong hash, ineligible claimer.

### 20.2. Format

```json
{
  "description": "Model training with redundancy",
  "events": [
    {"type": "compute.task.create", ...},
    {"type": "compute.task.claim", ...},
    {"type": "compute.task.claim", ...},
    {"type": "compute.task.claim", ...},
    {"type": "compute.task.submit", ...},
    {"type": "compute.task.verify", ...},
    {"type": "compute.task.complete", ...},
    {"type": "payment.record", ...}
  ],
  "expected_final_state": "completed",
  "expected_payments": [
    {"recipient": "did:cl:main:alice", "amount": 50},
    {"recipient": "did:cl:main:carol", "amount": 50}
  ]
}
```

### 20.3. Determinism

All event IDs, hashes, and signatures **MUST** be deterministic.

### 20.4. Cross-implementation

Test vectors **MUST** pass on at least two implementations before v1.0.

### 20.5. ZK test vectors

For ZK verification:

- proof generation (with a known circuit);
- proof verification;
- invalid proof rejection.

These require a specific ZK library. Implementations **MUST** agree on the variant.

### 20.6. TEE test vectors

For TEE attestation:

- valid attestation;
- invalid attestation;
- replay prevention.

These require a specific TEE implementation (SGX or SEV).

---

## 21. Open Questions

- How to verify **large-scale AI training** without 3× redundancy?
- How to attract **real clients** in a market dominated by hyperscalers?
- How to price compute **fairly across regions**?
- How to handle **hardware failures** and partial work?
- How to handle **privacy-preserving compute** (federated, secure enclaves)?
- How to prevent **CU from becoming a de facto currency** via compute payouts?
- How to attract contributors **without the promise of speculation**?
- How to compete with **free tier offerings** (Google Colab, Kaggle, Hugging Face)?
- How to handle jobs that **fail after partial execution**?
- How to verify against **adversarial metrics**?
- Should there be a **minimum CU stake** for high-value tasks?
- How to handle **multi-party computations** (MPC)?
- How to handle **training on private data** (differential privacy)?
- Should there be a **compute marketplace** (order book) or just task posting?
- How to handle **cross-context compute** (task in one context, executors in another)?
- Should there be a **compute difficulty adjustment** (like Bitcoin) or fixed pricing?
- How to handle **quantum-resistant verification**?

These will be resolved through RFCs and community discussion.

---

## Summary

**Compute tasks are:**

- Paid work using CPU/GPU.
- Funded by real clients.
- Verified by peers or automated systems.
- Rewarded with money + CU.
- Not mining. Not speculation.

**Three rules:**

1. CU awarded only for verified results.
2. Task issuer pays in money, not CU.
3. CU cannot be exchanged for money.

**Lifecycle:**

```
draft → open → claimed → submitted → verified → completed
         │         │           │
         │         │           └──→ disputed → resolved
         │         └──→ disputed → resolved
         └──→ cancelled
```

**Task types:**

- Training, inference, labeling, rendering, simulation, data processing, indexing, proof generation, batch.

**Staking:**

- CU (not money) staked to claim.
- Returned on success.
- Slashed on fraud.

**Verification:**

- Hash match, metric threshold, redundancy, ZK proof, TEE, manual, hybrid.

**Payment:**

- Fiat, stablecoins, crypto.
- Escrow held upfront.
- Released on verification.
- Split among redundant executors.

**Anti-abuse:**

- Reputation gates.
- CU staking.
- Redundancy.
- Sampling.
- Random verifier selection.
- Arbitration.

**Phases:**

1. Community help (10+ members).
2. Small compute (100+ members).
3. AI and large compute (1000+ members, 50+ GPUs).

**Key insight:**

Compute is where CL's economics become real. Unlike mining, every joule produces something someone needs. Unlike speculation, every dollar comes from a real client. Unlike tokens, CU cannot be bought or sold.

**This is not a get-rich scheme. It is a way to make compute useful.**

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [identity.md](./identity.md) — identity model.
- [contribution.md](./contribution.md) — contribution records.
- [reputation.md](./reputation.md) — reputation calculation.
- [bounty.md](./bounty.md) — bounty lifecycle (parallel mechanics).
- [consensus.md](./consensus.md) — finalization.
- [sync.md](./sync.md) — synchronization.
- [docs/useful-work.md](../docs/useful-work.md) — conceptual overview.
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
