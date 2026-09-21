# Useful Work in Contribution Ledger

**Compute power, community help, and network support — earning CU without mining.**

**Version:** 1.0  
**Status:** Living document  
**Related:** [Whitepaper](../docs/whitepaper.md) · [Economics](./economics.md) · [FAQ](./faq.md)

---

## Table of Contents

1. [The Idea](#1-the-idea)
2. [Why Not Mining](#2-why-not-mining)
3. [The Trap](#3-the-trap)
4. [Three Rules to Avoid Cryptocurrency](#4-three-rules-to-avoid-cryptocurrency)
5. [Types of Useful Work](#5-types-of-useful-work)
6. [Phase 1: Community Help](#6-phase-1-community-help)
7. [Phase 2: Small Compute Tasks](#7-phase-2-small-compute-tasks)
8. [Phase 3: AI and Large-Scale Compute](#8-phase-3-ai-and-large-scale-compute)
9. [Task Lifecycle](#9-task-lifecycle)
10. [Verification Methods](#10-verification-methods)
11. [Pricing](#11-pricing)
12. [Compute Task Events](#12-compute-task-events)
13. [Anti-Abuse](#13-anti-abuse)
14. [Hardware and Rewards](#14-hardware-and-rewards)
15. [Why This Matters](#15-why-this-matters)
16. [Sequence and Scale](#16-sequence-and-scale)
17. [Open Questions](#17-open-questions)

---

## 1. The Idea

Instead of burning energy on hashes, participants in Contribution Ledger can contribute **useful work**:

- **Compute power** for AI training, inference, simulation, rendering.
- **Community help**: moderation, translation, verification, mentoring.
- **Network support**: relays, storage, indexing.

Each task has an issuer who pays for the result. Each result is verified. Each verified result earns CU and reputation.

**This is not mining.** Mining produces nothing useful — only security for a network that has no other purpose. Useful work produces a result someone needs.

---

## 2. Why Not Mining

Bitcoin mining consumes ~150 TWh per year — more than many countries. It produces:

- Heat.
- Hash collisions.
- Nothing else.

The security it provides is real but expensive. And it is security for a system whose only product is money.

CL starts from a different question: **if people are going to spend compute power, can it produce something useful?**

The answer is yes. AI models need training. Simulations need running. Data needs labeling. Renders need computing. These are real tasks, with real clients, paying real money.

The same hardware that mines uselessly can do useful work.

### 2.1. Comparison

| | Mining | Useful Work |
|---|---|---|
| Output | Hashes | Trained model, rendered frame, simulation result |
| Who needs it | No one | Client, researcher, studio |
| Who pays | Protocol (emission) | Client (money) |
| Energy | Wasted | Used |
| Value created | None | Real |
| Environmental cost | High | Low |
| Profit source | Token price | Client payment |

### 2.2. What CL does not do

- CL does **not** pay for hash power.
- CL does **not** reward time online.
- CL does **not** emit tokens for compute.
- CL does **not** create a "mining" economy.

CL records verified useful work and pays for it — from client money, not from emission.

---

## 3. The Trap

As soon as "connect compute — earn CU" appears, people assume:

> "CU can be sold."

Then:

1. Someone offers to buy CU for money.
2. A "CU rate" emerges.
3. An exchange appears.
4. Speculation follows.
5. CU becomes a de facto currency.
6. CL becomes a cryptocurrency.

**This must not happen.** The entire value of CL depends on CU being non-transferable.

The second trap is **verification**. If you simply pay for "compute time", everyone cheats:

- Weak machines claim to be strong.
- Tasks are duplicated.
- Results are plagiarized.
- Bots farm CU.
- Fake metrics are submitted.

These are classical problems of Proof of Useful Work. No project has fully solved them. Golem, iExec, and Bittensor all struggle with this.

CL does not pretend to solve them perfectly. It uses layered defenses (see [Section 10](#10-verification-methods)).

---

## 4. Three Rules to Avoid Cryptocurrency

These rules are non-negotiable. They distinguish CL from every compute-token project.

### Rule 1: CU awarded only for verified results

Not for time online. Not for "connected GPU". Not for "claimed hash rate".

**For a result that passes verification.**

Example:
- ❌ "Connected GPU for 1 hour → 10 CU."
- ✅ "Trained model, achieved accuracy 0.92, verified → 50 CU."

### Rule 2: Task issuer pays in money

The client pays in fiat or stablecoin. Money goes to the executor. CU is a reputation bonus, not the payment.

This means:
- Profit comes from a real customer.
- There is no emission.
- There is no inflation.
- The economy is funded by demand, not by speculation.

### Rule 3: CU cannot be exchanged for money

Not directly. Not indirectly. Not through a wrapper.

CU only becomes money through:

- **Cooperative payouts** — by community rules, proportional to CU.
- **Nothing else.**

This removes the incentive to farm CU and sell it. It makes CU a signal of contribution, not a financial asset.

**If any of these rules is broken, the system becomes a cryptocurrency and loses its reason to exist.**

---

## 5. Types of Useful Work

CL recognizes three categories.

### 5.1. Compute Work

Work that uses CPU, GPU, or specialized hardware.

- AI model training.
- Model fine-tuning.
- Inference (running models).
- Data labeling and annotation.
- Scientific simulation.
- Financial modeling.
- 3D rendering.
- Video encoding.
- Cryptographic computation (ZK proofs, verification).
- Data indexing and search.

### 5.2. Community Help

Work that helps the community directly. Does not require special hardware.

- Moderation.
- Translation.
- Documentation.
- Verification of claims.
- Mentorship.
- Onboarding new members.
- Reviewing contributions.
- Organizing events.
- Testing.
- Bug triage.

### 5.3. Network Support

Work that keeps the infrastructure running.

- Running a relay.
- Running a full node.
- Providing storage.
- Indexing the ledger.
- Offering APIs.
- Maintaining mirrors.

All three categories earn CU. The weights differ by context.

---

## 6. Phase 1: Community Help

**Available from day one.**

Community help requires no hardware, no special setup, no verification infrastructure. It is the easiest way to earn CU and the first to launch.

### 6.1. Examples and rates

| Task | Typical rate | Notes |
|---|---|---|
| Moderation hour | $5–15 | Per hour |
| Translation (per 1 000 words) | $10–30 | Quality-checked |
| Documentation page | $20–100 | Reviewed |
| Mentorship hour | $15–50 | Logged and confirmed |
| Review of a contribution | $5–20 | Per review |
| Onboarding a new member | $5–15 | Verified by the new member |
| Event organization | $50–500 | Per event |
| Bug triage | $5–20 | Per bug |
| Testing a release | $10–100 | Per test cycle |

Rates are set by the community or the task issuer. CL does not fix them.

### 6.2. Verification

- **Peer confirmation.** Another member confirms the work was done.
- **Automated checks.** E.g., translation length, documentation links.
- **Sampling.** 5–10% audited manually.
- **Reputation.** New members checked strictly; experienced members trusted more.

### 6.3. Why start here

- No hardware needed.
- No verification infrastructure needed.
- Low barrier to entry.
- Builds reputation for later compute tasks.
- Creates community cohesion.

**Every CL community starts with Phase 1.** Compute comes later.

---

## 7. Phase 2: Small Compute Tasks

**Available once the community has ~100 members and some funding.**

Small compute tasks are those that:

- fit on a single machine (or a few);
- complete in minutes to hours;
- produce verifiable results.

### 7.1. Examples and rates

| Task | Typical rate | Notes |
|---|---|---|
| 3D rendering (per frame) | $0.10–2 | Depends on complexity |
| Video encoding (per minute) | $0.05–0.50 | Depends on resolution |
| Scientific simulation (per run) | $1–100 | Depends on model |
| Data processing (per GB) | $0.10–1 | ETL, cleaning |
| ZK proof generation | $1–50 | Per proof |
| Indexing (per million records) | $1–20 | Search, analytics |
| Batch inference (per 1 000 items) | $0.50–5 | Small models |
| Test suite run | $0.50–10 | CI for external projects |

### 7.2. Verification

- **Redundancy.** Same task to 3 executors; results must match.
- **Sampling.** 5% audited manually.
- **Determinism.** For tasks with a correct answer (rendering, simulation), compare outputs.
- **Cryptographic proofs.** Where available (ZK).
- **Reputation.** New executors checked strictly.

### 7.3. Infrastructure

- Task scheduler: simple queue (Redis, RabbitMQ, or custom).
- Executor client: CLI or daemon that pulls tasks and returns results.
- Result verification: automated comparison + sampling.
- Payment: escrow in fiat or stablecoin.

This phase is technically feasible for a small team.

---

## 8. Phase 3: AI and Large-Scale Compute

**Available once the community has ~1 000 members and 50+ GPUs.**

Large-scale compute tasks require:

- distributed training infrastructure;
- robust verification;
- high trust;
- real clients paying real money.

### 8.1. Examples and rates

| Task | Typical rate | Notes |
|---|---|---|
| Model fine-tuning (small) | $50–500 | Hours on 1 GPU |
| Model fine-tuning (large) | $500–5 000 | Days on multiple GPUs |
| Training from scratch (small) | $1 000–10 000 | Days to weeks |
| Training from scratch (large) | $10 000–500 000 | Weeks on clusters |
| Inference (per 1 000 requests) | $0.50–5 | Production models |
| Dataset labeling (per 1 000 items) | $5–100 | Depends on complexity |
| Federated learning round | $100–5 000 | Aggregating updates |

### 8.2. Verification

- **Validation metric.** The trained model must achieve a declared metric on a held-out set.
- **Reference comparison.** Compare against a known baseline.
- **Redundancy.** For small jobs, run 3 times and compare.
- **Sampling.** Auditors review 5% of jobs.
- **Reputation.** Only trusted executors can take large jobs.

### 8.3. Infrastructure

- Distributed scheduler: Kubernetes, Ray, or Slurm.
- Model registry: tracked by the ledger (hashes, metadata).
- Dataset storage: IPFS, S3-compatible, or Arweave.
- GPU attestation: TEE (SGX, SEV) or signed hardware IDs where possible.
- Payment: escrow, milestone-based for large jobs.

### 8.4. What this is not

- Not a competitor to AWS or GCP for general compute.
- Not a token-based compute market.
- Not a "decentralized OpenAI".

It is a **marketplace for verified compute tasks**, funded by clients, with reputation as the trust layer.

### 8.5. Why this matters

Today, compute is concentrated in a few hyperscalers. Researchers, small studios, and independent labs struggle to access affordable GPU time.

CL offers an alternative: a network of contributors who can take tasks, verified by reputation, paid in money, tracked in a ledger.

It is not faster or cheaper than hyperscalers for all workloads. But it is **more accessible**, **more verifiable**, and **owned by no one**.

---

## 9. Task Lifecycle

Every compute task follows the same lifecycle.

```
create → claim → submit → verify → pay → record CU
                  ↓
              dispute → arbitration
```

### 9.1. Create

Task issuer posts the task:

```json
{
  "type": "compute.task.create",
  "issuer": "did:cl:org:ailab",
  "task": {
    "kind": "model_training",
    "dataset": "ipfs://...",
    "target_metric": {"name": "accuracy", "value": 0.92},
    "max_runtime_sec": 3600,
    "gpu_min_vram_gb": 12
  },
  "reward": {"amount": 50, "currency": "USD"},
  "redundancy": 3,
  "verification": "metric_threshold",
  "deadline": 1730100000
}
```

The issuer funds escrow before the task is visible.

### 9.2. Claim

A participant claims the task. Their CU may be staked (not money) to discourage spam.

```json
{
  "type": "compute.task.claim",
  "author": "did:cl:main:alice",
  "payload": {"task_id": "blake3:..."}
}
```

### 9.3. Submit

The participant runs the task and submits the result.

```json
{
  "type": "compute.task.submit",
  "author": "did:cl:main:alice",
  "payload": {
    "task_id": "blake3:...",
    "result_hash": "blake3:...",
    "result_uri": "ipfs://...",
    "metrics": {"accuracy": 0.93},
    "runtime_sec": 2400,
    "hardware": {"gpu": "RTX 4090", "vram_gb": 24}
  }
}
```

### 9.4. Verify

Verifiers check:

- The result matches the requirement.
- The metric meets the target.
- The result hash is correct.
- Redundant runs agree (if redundancy > 1).

```json
{
  "type": "compute.task.verify",
  "author": "did:cl:main:verifier1",
  "payload": {
    "task_id": "blake3:...",
    "result": "valid",
    "comment": "Metric achieved, hash matches"
  }
}
```

### 9.5. Pay

Escrow releases payment to the executor.

```json
{
  "type": "payment.record",
  "author": "did:cl:escrow:main:...",
  "payload": {
    "task_id": "blake3:...",
    "recipient": "did:cl:main:alice",
    "amount": 50,
    "currency": "USD",
    "method": "fiat",
    "external_ref": "stripe:ch_...",
    "status": "settled"
  }
}
```

### 9.6. Record CU

CU and reputation are awarded to the executor, based on the task weight class.

### 9.7. Dispute

If verification fails or the issuer rejects the result, either party opens a dispute. Three randomly chosen auditors review the evidence and vote.

---

## 10. Verification Methods

Layered defenses. No single method is sufficient; together they make fraud expensive.

### 10.1. Redundancy

Same task given to N executors. Results must match within tolerance.

- **Pros:** Strong, simple.
- **Cons:** Multiplies cost by N.
- **When to use:** Small tasks; tasks with deterministic output; high-value tasks.

Typical N: 3.

### 10.2. Sampling

A random fraction (5–10%) of tasks is manually audited.

- **Pros:** Cheap, catches patterns.
- **Cons:** Does not catch isolated fraud.
- **When to use:** Large volume, low-value tasks.

### 10.3. Cryptographic Proofs

For some tasks, the computation can be proven mathematically.

- **ZK proofs** — for verifiable computation.
- **TEE attestation** — for trusted hardware execution.
- **Signed hardware IDs** — for provenance.

- **Pros:** Strong, cheap verification.
- **Cons:** Limited to certain task types; overhead.
- **When to use:** ZK computations, sensitive workloads, high-value jobs.

### 10.4. Reference Comparison

Compare against a known baseline.

- **Pros:** Simple, catches gross errors.
- **Cons:** Does not catch subtle fraud.
- **When to use:** AI training (compare against a known model), rendering (compare against a reference render).

### 10.5. Reputation

New executors are checked strictly. Experienced executors are trusted more.

- **Pros:** Scales; rewards good behavior.
- **Cons:** Reputation can be farmed (mitigated by other methods).
- **When to use:** All tasks, as a layer.

### 10.6. CU Staking

Executors stake CU (not money) to claim a task. If fraud is detected, the CU is slashed.

- **Pros:** Real cost to cheating, but not a financial barrier.
- **Cons:** Only works for established executors (who have CU).
- **When to use:** High-value tasks; known executors.

### 10.7. Combination

In practice, all methods are combined:

| Task value | Redundancy | Sampling | Proofs | Staking |
|---|---|---|---|---|
| Low ($0.10–10) | 1 | 10% | — | — |
| Medium ($10–100) | 3 | 5% | where possible | small |
| High ($100–1 000) | 3 | 5% + audit | where possible | medium |
| Critical ($1 000+) | 5 | 100% audit | yes | large |

The exact configuration is set by the task issuer or the community.

---

## 11. Pricing

Prices are set by the **task issuer**, not by CL. CL only records the price.

### 11.1. Typical rates

| Task | Rate |
|---|---|
| Moderation hour | $5–15 |
| Translation (per 1 000 words) | $10–30 |
| GPU hour (consumer, e.g., RTX 4090) | $0.10–0.50 |
| GPU hour (datacenter, e.g., A100) | $1–5 |
| CPU hour | $0.01–0.10 |
| AI training job (small) | $50–500 |
| AI training job (large) | $500–5 000 |
| Inference (per 1 000 requests) | $0.50–5 |
| Dataset labeling (per 1 000 items) | $5–100 |
| Rendering (per frame) | $0.10–2 |
| Simulation (per run) | $1–100 |

### 11.2. Factors affecting price

- **Hardware.** GPU generation matters. A100 vs RTX 4090 is 10×.
- **Verification.** Tasks with heavy verification cost more.
- **Urgency.** Deadlines increase price.
- **Trust.** New executors may need to offer lower prices.
- **Market.** Supply and demand set the baseline.

### 11.3. Comparison to hyperscalers

| Provider | A100 hour |
|---|---|
| AWS | $3–5 |
| GCP | $3–4 |
| Azure | $3–5 |
| CL network | $1–5 |

CL is competitive when:

- the task is small or intermittent;
- the client cannot commit to long-term contracts;
- the client values verifiability;
- the client wants to support open infrastructure.

CL is not competitive for:

- massive, continuous workloads;
- latency-critical inference;
- compliance-heavy enterprise use.

**CL is not trying to replace hyperscalers. It is trying to add an alternative.**

---

## 12. Compute Task Events

CL extends the ledger with compute-specific event types.

### 12.1. Event types

- `compute.task.create` — issuer posts a task.
- `compute.task.claim` — executor claims a task.
- `compute.task.submit` — executor submits a result.
- `compute.task.verify` — verifier confirms a result.
- `compute.task.reject` — verifier rejects a result.
- `compute.task.dispute` — either party opens a dispute.
- `compute.task.resolve` — arbitration resolves a dispute.
- `compute.task.complete` — task is finished and paid.
- `compute.task.cancel` — task is cancelled.
- `compute.executor.register` — executor registers hardware and capabilities.
- `compute.executor.attest` — hardware attestation (TEE, signed ID).

### 12.2. Example: full task

```json
[
  {"type": "compute.task.create", "issuer": "did:cl:org:ailab", "task": {...}},
  {"type": "compute.task.claim", "author": "did:cl:main:alice", "payload": {...}},
  {"type": "compute.task.submit", "author": "did:cl:main:alice", "payload": {...}},
  {"type": "compute.task.verify", "author": "did:cl:main:verifier1", "payload": {...}},
  {"type": "compute.task.verify", "author": "did:cl:main:verifier2", "payload": {...}},
  {"type": "compute.task.verify", "author": "did:cl:main:verifier3", "payload": {...}},
  {"type": "compute.task.complete", "author": "did:cl:org:ailab", "payload": {...}},
  {"type": "payment.record", "author": "did:cl:escrow:main:...", "payload": {...}}
]
```

Every step is signed, chained, and immutable.

---

## 13. Anti-Abuse

### 13.1. Sybil attacks

**Threat:** Fake accounts claim tasks and submit garbage.

**Defense:**
- Attestation via organizations.
- Reputation thresholds for task classes.
- CU staking (not money) to claim tasks.
- Rate limits for new accounts.
- Invitation-only for high-value tasks.

### 13.2. Fake hardware

**Threat:** A weak machine claims to be strong.

**Defense:**
- Benchmark tasks with known expected runtime.
- TEE attestation where available.
- Signed hardware IDs.
- Reputation: past performance is visible.

### 13.3. Result plagiarism

**Threat:** Executor copies someone else's result.

**Defense:**
- Result hashes are unique.
- Random nonces in inputs.
- Redundancy with different random seeds.
- Content analysis.

### 13.4. Metric manipulation

**Threat:** Executor games the validation metric.

**Defense:**
- Held-out test sets (not shared with executor).
- Multiple metrics.
- Adversarial evaluation.
- Manual review for high-value tasks.

### 13.5. Bot farms

**Threat:** One operator runs many fake executors.

**Defense:**
- Hardware fingerprinting.
- IP and network analysis.
- CU staking per identity.
- Reputation graph analysis.

### 13.6. Task flooding

**Threat:** Spam tasks to drain verification resources.

**Defense:**
- Task creation fee (in CU, not money).
- Reputation threshold for issuers.
- Rate limits.
- Community moderation.

### 13.7. Collusion

**Threat:** Issuer and executor collude to fake results and split payment.

**Defense:**
- Escrow audited by third parties.
- Random verifier selection.
- Redundancy with independent executors.
- Public records reveal patterns.

**No defense is perfect.** The goal is to make fraud expensive, not impossible.

---

## 14. Hardware and Rewards

### 14.1. Consumer hardware

| Hardware | Typical use | Reward range |
|---|---|---|
| CPU (8–16 cores) | Community help, small tasks | $0.01–0.10/hour |
| Consumer GPU (RTX 3060–4090) | Rendering, small training, inference | $0.10–0.50/hour |
| Apple Silicon (M1–M4) | Inference, small tasks | $0.10–0.50/hour |

### 14.2. Prosumer hardware

| Hardware | Typical use | Reward range |
|---|---|---|
| RTX 4090, 5090 | Medium training, rendering | $0.50–1/hour |
| A6000, RTX 6000 Ada | Medium training | $1–2/hour |
| Multiple GPUs (home lab) | Small clusters | $2–5/hour total |

### 14.3. Datacenter hardware

| Hardware | Typical use | Reward range |
|---|---|---|
| A100 40GB | Large training | $1–3/hour |
| A100 80GB | Large training | $2–4/hour |
| H100 | Cutting-edge training | $3–5/hour |
| H200, B200 | Frontier training | $4–10/hour |

### 14.4. Realistic earnings

**Casual contributor (1 consumer GPU, 20 hours/week):**
- $0.20/hour × 20 = $4/week = **~$200/year**.

**Serious contributor (4 GPUs, 40 hours/week):**
- $0.50/hour × 4 × 40 = $80/week = **~$4 000/year**.

**Small datacenter (8× A100, 24/7):**
- $2/hour × 8 × 168 = $2 688/week = **~$140 000/year**.

These are estimates. Real earnings depend on tasks available, competition, and verification overhead.

### 14.5. What this is not

- Not a get-rich scheme.
- Not a replacement for a job.
- Not a passive income stream.
- Not a way to "mine" CU.

**It is a way to be paid for compute you already have, doing work someone needs.**

---

## 15. Why This Matters

### 15.1. For participants

- Monetize idle hardware.
- Earn without a token.
- Build reputation alongside income.
- Contribute to useful work (AI, science, open source).

### 15.2. For clients

- Access to compute without hyperscaler lock-in.
- Verifiable results.
- Transparent pricing.
- Support for open infrastructure.

### 15.3. For the field

- A model for **useful work** instead of wasted energy.
- A model for **verified computation** without token economics.
- A model for **distributed compute** with reputation as trust.

### 15.4. For the environment

If even 1% of mining energy went to useful work, the environmental impact would be significant. CL is one attempt to make that happen.

### 15.5. For AI

Compute is the bottleneck for AI research. Access is concentrated. CL offers an alternative: distributed, verifiable, reputation-based.

It will not replace a cluster of 10 000 GPUs. It can serve researchers, small labs, and open-source projects who cannot afford one.

---

## 16. Sequence and Scale

Useful work does not launch all at once. It scales with the community.

### 16.1. Stage 1 — Community help (10–100 members)

- Moderation.
- Translation.
- Documentation.
- Mentorship.
- Testing.

No hardware. No verification infrastructure. Just people and a ledger.

### 16.2. Stage 2 — Small compute (100–500 members)

- Rendering.
- Simulation.
- Test runs.
- Data processing.
- Indexing.

Simple scheduler. Basic verification. First paying clients.

### 16.3. Stage 3 — AI and large compute (1 000+ members)

- Model training.
- Fine-tuning.
- Inference at scale.
- Dataset labeling.
- Federated learning.

Distributed scheduler. Robust verification. Real AI clients.

### 16.4. Why the order matters

- **Verification comes before scale.** You cannot verify 1 000 tasks if you cannot verify 10.
- **Reputation comes before trust.** A new community cannot offer high-value compute.
- **Clients come before hardware.** It is easy to attract executors; it is hard to attract clients.

**Starting compute on 11 members is a toy.** Starting it on 1 000 members is a market.

---

## 17. Open Questions

- How to verify large-scale AI training without 3× redundancy?
- How to attract real clients in a market dominated by hyperscalers?
- How to price compute fairly across regions?
- How to handle hardware failures and partial work?
- How to handle privacy-preserving compute (federated, secure enclaves)?
- How to prevent CU from becoming a de facto currency via compute payouts?
- How to attract contributors without the promise of speculation?
- How to compete with free tier offerings (Google Colab, Kaggle, Hugging Face)?
- How to handle jobs that fail after partial execution?
- How to verify against adversarial metrics?

These are subjects of open discussion. RFCs are welcome.

---

## Summary

**Useful work is CL's answer to mining.**

- Instead of burning energy on hashes, contribute compute.
- Instead of paying for time online, pay for verified results.
- Instead of a token economy, use reputation.
- Instead of speculation, use client money.

**Three rules:**

1. CU awarded only for verified results.
2. Task issuer pays in money, not CU.
3. CU cannot be exchanged for money directly.

**Three phases:**

1. Community help (10+ members).
2. Small compute (100+ members).
3. AI and large compute (1 000+ members).

**This is not a get-rich scheme. It is a way to make work useful.**

---

**Related documents:**

- [Whitepaper](../docs/whitepaper.md) — full design.
- [Economics](./economics.md) — how participants earn.
- [FAQ](./faq.md) — common questions.
- [CONTRIBUTING](../CONTRIBUTING.md) — how to help.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 1.0

---

