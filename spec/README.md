# Specification — How to Read It

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Living document  
**Related:** [Whitepaper](../docs/whitepaper.md) · [REPO_STRUCTURE](../REPO_STRUCTURE.md) · [CONTRIBUTING](../CONTRIBUTING.md)

---

## Table of Contents

1. [Purpose of This Specification](#1-purpose-of-this-specification)
2. [What This Specification Is Not](#2-what-this-specification-is-not)
3. [Structure of the Specification](#3-structure-of-the-specification)
4. [Normative Language (RFC 2119)](#4-normative-language-rfc-2119)
5. [Reading Order](#5-reading-order)
6. [Versioning](#6-versioning)
7. [Compatibility](#7-compatibility)
8. [Test Vectors](#8-test-vectors)
9. [How to Propose Changes](#9-how-to-propose-changes)
10. [Conventions Used in This Spec](#10-conventions-used-in-this-spec)
11. [Open Questions](#11-open-questions)

---

## 1. Purpose of This Specification

The specification defines **how Contribution Ledger works at the protocol level**.

It answers:

- What events exist.
- How events are formatted, signed, and hashed.
- How state is derived from events.
- How nodes synchronize.
- How consensus is reached.
- How reputation is computed.
- How bounties, votes, and compute tasks are processed.

**The specification is the reference for implementers.** If the code and the specification disagree, the specification wins — unless the specification has an error, in which case the error is fixed by an RFC.

### 1.1. Who this is for

- **Implementers** — building a node, client, or tool.
- **Auditors** — reviewing the design for correctness and security.
- **Researchers** — studying the protocol.
- **Contributors** — proposing changes.

### 1.2. Who this is not for

- **End users** — read [docs/whitepaper.md](../docs/whitepaper.md) and [docs/faq.md](../docs/faq.md) instead.
- **Decision makers** — read [SUMMARY.md](../SUMMARY.md) and [docs/economics.md](../docs/economics.md) instead.
- **Crypto speculators** — this project has no token, and there is nothing here for you.

---

## 2. What This Specification Is Not

To avoid confusion:

### 2.1. Not a whitepaper

The [whitepaper](../docs/whitepaper.md) explains **why** CL exists and **what** it does.  
The specification explains **how** it does it.

If the whitepaper says "reputation decays over time", the specification says exactly what formula, what parameters, and what edge cases.

### 2.2. Not a tutorial

The specification is a reference, not a guide. It assumes you know:

- basic cryptography (hashes, signatures, Merkle trees);
- basic distributed systems (gossip, consensus);
- basic data structures (DAG, JSON, CBOR).

### 2.3. Not final

This is a **draft**. The protocol is not frozen. Parts may change. Test vectors will evolve. Do not build a production system on this yet.

### 2.4. Not complete

Some parts are marked as **TODO** or **open questions**. These are known gaps, not oversights. They will be filled as the design matures.

### 2.5. Not a guarantee of security

No specification is secure just because it exists. Security comes from implementation, review, and audit. This spec is a starting point, not an endorsement.

---

## 3. Structure of the Specification

The specification is split by topic. Each file is self-contained but references others.

| File | Purpose |
|---|---|
| `README.md` | This file. How to read the spec. |
| `events.md` | Event format, canonical serialization, hashing, signatures, DAG. |
| `identity.md` | Keys, DID, attestations, recovery, rotation. |
| `contribution.md` | Contribution records, weights, confirmations, decay, revocation. |
| `reputation.md` | Reputation formula, context, caching, determinism. |
| `ledger.md` | DAG structure, Merkle trees, checkpoints, storage. |
| `consensus.md` | Validators, finalization, rotation, fork, federation. |
| `bounty.md` | Bounty lifecycle, escrow, arbitration, payment recording. |
| `vote.md` | Proposals, quadratic weight, delegation, secret voting. |
| `compute.md` | Compute tasks, verification, staking, anti-abuse. |
| `sync.md` | P2P synchronization, gossip, header exchange. |
| `api.md` | REST, WebSocket, gRPC endpoints. |
| `privacy.md` | Selective disclosure, ZK proofs, private contexts. |
| `test-vectors/` | JSON test vectors for compatibility. |

### 3.1. Dependencies between files

Some files depend on others. Reading order matters.

```
events.md  ←  everything depends on this
    │
    ├── identity.md
    ├── contribution.md
    │       │
    │       └── reputation.md
    │
    ├── ledger.md
    ├── consensus.md
    │
    ├── bounty.md
    ├── vote.md
    └── compute.md
```

**Rule:** read `events.md` first. Everything else builds on it.

---

## 4. Normative Language (RFC 2119)

This specification uses the keywords defined in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) to distinguish requirements from suggestions.

### 4.1. Keywords

| Keyword | Meaning |
|---|---|
| **MUST** | Absolute requirement. An implementation that violates this is not compliant. |
| **MUST NOT** | Absolute prohibition. |
| **SHOULD** | Recommended. There may be valid reasons to deviate, but the implications must be understood. |
| **SHOULD NOT** | Not recommended. Deviating is allowed but discouraged. |
| **MAY** | Optional. Implementation decides. |
| **REQUIRED** | Synonym for MUST. |
| **RECOMMENDED** | Synonym for SHOULD. |
| **OPTIONAL** | Synonym for MAY. |

### 4.2. Examples

**MUST:**
> Every event **MUST** include a valid Ed25519 signature from its author.

This is not optional. A node that accepts unsigned events is broken.

**SHOULD:**
> A validator **SHOULD** rotate out after 12 months of continuous service.

Rotating is recommended, but a community may choose different rules.

**MAY:**
> A community **MAY** enable CU decay.

Decay is optional. Each community decides.

### 4.3. How to read keywords

Keywords are written in **UPPERCASE** to distinguish them from ordinary use.

- "The signature must be valid" — ordinary English, not a formal requirement.
- "The signature **MUST** be valid" — a formal requirement.

### 4.4. Not all requirements are normative

Some text is **informative** — it explains, gives context, or provides examples. Informative text does not create requirements.

If a statement is not marked with a keyword, it is informative by default.

### 4.5. Language precision

- **"is"** — describes the current design.
- **"MUST be"** — a requirement.
- **"SHOULD be"** — a recommendation.
- **"MAY be"** — an option.

When in doubt, treat vague statements as informative, not normative.

---

## 5. Reading Order

Different readers need different paths.

### 5.1. If you are an implementer

1. `README.md` (this file) — how to read.
2. `events.md` — the foundation.
3. `identity.md` — who can act.
4. `contribution.md` — what actions exist.
5. `reputation.md` — how state is computed.
6. `ledger.md` — how data is stored.
7. `consensus.md` — how nodes agree.
8. `sync.md` — how nodes communicate.
9. `api.md` — how clients interact.
10. `bounty.md`, `vote.md`, `compute.md` — feature-specific.
11. `privacy.md` — optional features.
12. `test-vectors/` — how to verify your implementation.

### 5.2. If you are an auditor

1. `README.md` — how to read.
2. `events.md` — the foundation.
3. `consensus.md` — the riskiest part.
4. `reputation.md` — the core logic.
5. `identity.md` — where attacks start.
6. `privacy.md` — where leaks happen.
7. `compute.md` — where fraud is possible.
8. Everything else as needed.

### 5.3. If you are proposing a change

1. `README.md` — how to read.
2. The file relevant to your change.
3. `../CONTRIBUTING.md` — how to propose.
4. `../rfcs/README.md` — the RFC process.

### 5.4. If you are just curious

1. `../SUMMARY.md` — one-page overview.
2. `../docs/whitepaper.md` — full design.
3. `events.md` — how it works at the lowest level.
4. Anything else that interests you.

---

## 6. Versioning

The specification uses **semantic versioning** with a twist.

### 6.1. Format

```
MAJOR.MINOR.PATCH
```

- **MAJOR** — breaking changes. Existing implementations will not work with new ones.
- **MINOR** — backward-compatible additions. Old implementations can still read new data (with limitations).
- **PATCH** — clarifications, typo fixes, non-normative changes.

### 6.2. Examples

**MAJOR change:**  
Changing the signature algorithm from Ed25519 to something else.  
Changing the event envelope structure.  
Removing an event type.

**MINOR change:**  
Adding a new event type (e.g., `compute.task.verify`).  
Adding a new optional field.  
Adding a new API endpoint.

**PATCH change:**  
Fixing a typo.  
Clarifying ambiguous wording.  
Adding an example.

### 6.3. Version declaration

Each spec file declares its version at the top:

```markdown
**Version:** 0.1
```

The **protocol version** is separate and declared in `events.md`:

```json
{
  "version": 1,
  ...
}
```

Implementations MUST declare which protocol version they support.

### 6.4. Current version

**Protocol version:** 0 (draft, not frozen)  
**Spec version:** 0.1 (draft)

Until the protocol reaches version 1.0, no backward compatibility is guaranteed.

### 6.5. When 1.0 is reached

Version 1.0 will be declared when:

- All core spec files are complete.
- Test vectors are published.
- Two independent implementations pass the test vectors.
- A security audit has been completed.

After 1.0, breaking changes require a MAJOR version bump and a migration path.

---

## 7. Compatibility

### 7.1. What "compatible" means

Two implementations are **compatible** if:

- They can read each other's events.
- They compute the same state from the same events.
- They agree on which events are valid.

Compatibility is verified by **test vectors** (see [Section 8](#8-test-vectors)).

### 7.2. Forward compatibility

A node running version N SHOULD be able to:

- Read events created by version N+1 (if no MAJOR change).
- Ignore unknown fields.
- Reject unknown event types without crashing.

### 7.3. Backward compatibility

A node running version N+1 SHOULD be able to:

- Read events created by version N.
- Interpret them according to the rules of version N.

### 7.4. No guarantee before 1.0

Before version 1.0, backward and forward compatibility are **not guaranteed**. The protocol may change in breaking ways. This is a draft.

### 7.5. Federation compatibility

Different communities may run different versions. To federate, they MUST agree on:

- A shared protocol version.
- A shared event format.
- A shared interpretation of reputation.

If they cannot agree, they remain separate ledgers.

---

## 8. Test Vectors

Test vectors are the backbone of compatibility. They are JSON files with known inputs and expected outputs.

### 8.1. Purpose

Test vectors ensure that:

- Two implementations produce the same hash for the same event.
- Two implementations compute the same reputation.
- Two implementations tally votes identically.
- Bugs are caught before deployment.

### 8.2. Location

```
spec/test-vectors/
├── events.json          # Event serialization, hashing, signing
├── reputation.json      # Reputation calculation
├── votes.json           # Vote tallying
├── bounties.json        # Bounty lifecycle
├── compute.json         # Compute task verification
└── README.md            # How to use the vectors
```

### 8.3. Format

Each test vector file contains an array of test cases:

```json
{
  "description": "Minimal contribution event",
  "input": {
    "type": "contribution.create",
    "version": 1,
    "author": "did:cl:main:alice",
    "payload": {
      "subject": "did:cl:main:alice",
      "action": "code_commit",
      "weight_class": "commit",
      "timestamp": 1730000000
    }
  },
  "expected": {
    "canonical_cbor": "a1...",
    "event_id": "blake3:...",
    "signature": "ed25519:..."
  }
}
```

### 8.4. Coverage

Test vectors MUST cover:

- Minimal valid event of each type.
- Invalid events (bad signature, missing fields, wrong types).
- Edge cases (empty payloads, maximum values).
- Deterministic outputs (hashes, signatures with fixed keys).
- Reputation calculations with known inputs.
- Vote tallies with quadratic weights.
- Bounty lifecycle states.
- Compute task verification outcomes.

### 8.5. How to use

1. Read the test vector.
2. Feed the input into your implementation.
3. Compare the output to the expected output.
4. If they differ, your implementation is not compatible.

### 8.6. How to contribute

To add a test vector:

1. Open an issue describing the case.
2. Submit a PR to `spec/test-vectors/`.
3. Include a reference implementation output.

Test vectors are versioned together with the spec.

### 8.7. Deterministic signing

Test vectors for signatures use **fixed private keys** (not real keys — do not use them in production). This ensures reproducible signatures.

**Warning:** fixed keys are for testing only. Never use them outside test vectors.

---

## 9. How to Propose Changes

The specification is not frozen. It changes through the RFC process.

### 9.1. Small changes

Typos, clarifications, and non-normative fixes can be submitted as direct PRs.

Examples:
- Fix a broken link.
- Clarify ambiguous wording.
- Add an example.

### 9.2. Medium changes

New event types, new fields, new API endpoints, or clarifications of existing rules.

Process:
1. Open an issue describing the change.
2. Discuss with maintainers.
3. Submit a PR.

### 9.3. Large changes

Changes to core structures, consensus, reputation formula, or anything breaking.

Process:
1. Write an RFC (see `../rfcs/README.md`).
2. Open a PR to `rfcs/`.
3. Discussion period (minimum 7 days).
4. If accepted, update the specification in a follow-up PR.

### 9.4. Who decides

- Small changes: any maintainer.
- Medium changes: rough consensus among maintainers.
- Large changes: rough consensus + no unresolved objections from implementers.

### 9.5. Rejected proposals

Rejected RFCs are kept in `rfcs/`. They are part of the project's history.

---

## 10. Conventions Used in This Spec

### 10.1. Code blocks

JSON examples:

```json
{
  "type": "contribution.create",
  "version": 1
}
```

Command examples:

```bash
cl-node --config ./config.toml
```

### 10.2. Field names

- Field names are **lowercase with underscores**: `weight_class`, `created_at`.
- Field names are **stable** — do not rename without a MAJOR version bump.

### 10.3. Timestamps

- All timestamps are **Unix time in seconds** (integer).
- Example: `1730000000` = 2024-10-27T02:13:20Z.
- Timestamps are **UTC** — no timezones.

### 10.4. Identifiers

- **DID:** `did:cl:<network>:<base58-pubkey>`
- **Event ID:** `blake3:<hex>` or `blake3:<base58>`
- **Hash:** `blake3:<...>` or `sha256:<...>`

### 10.5. Signature format

```
ed25519:<base58-signature>
```

### 10.6. Numbers

- Integers: no leading zeros.
- Floats: only where explicitly allowed; use fixed precision.
- Reputation: floating point, rounded to 6 decimal places for comparison.

### 10.7. Ordering

- JSON objects: keys sorted lexicographically for canonical form.
- Arrays: order matters unless stated otherwise.

### 10.8. References

Internal references use relative links:

```markdown
See [events.md](./events.md#3-event-envelope).
```

External references use full URLs.

### 10.9. Diagrams

Diagrams use ASCII art for portability:

```
create → claim → submit → verify → pay
                  ↓
              dispute
```

### 10.10. Emphasis

- **Bold** for key terms.
- `Monospace` for code, identifiers, and field names.
- _Italics_ for emphasis (sparingly).

---

## 11. Open Questions

The specification is a draft. These questions remain open.

### 11.1. Structural

- Should the spec be split differently? (e.g., separate files for each event type)
- Should there be a formal grammar for events?
- Should the spec be machine-readable (e.g., JSON Schema)?

### 11.2. Process

- How often should the spec be versioned?
- Should there be a spec committee?
- How to handle conflicting RFCs?

### 11.3. Test vectors

- How to version test vectors independently?
- Should there be a test vector generator tool?
- How to handle platform-specific differences (endianness, float precision)?

### 11.4. Compatibility

- What is the minimum compatibility guarantee for version 1.0?
- How long should old protocol versions be supported?
- How to handle federation between different protocol versions?

### 11.5. Tooling

- Should there be a reference parser/serializer library?
- Should there be a formal verification of the spec?
- Should there be a spec linter?

These will be resolved through RFCs and community discussion.

---

## Summary

**This specification is:**

- **A reference** for implementers, auditors, researchers.
- **A draft** — version 0.1, not frozen.
- **A work in progress** — open questions remain.

**How to read it:**

- Start with `events.md`.
- Follow the dependency graph.
- Use RFC 2119 keywords as requirements.

**How to verify compatibility:**

- Use test vectors.
- If two implementations disagree, one is wrong.

**How to change it:**

- Small changes: PR.
- Medium changes: issue + PR.
- Large changes: RFC.

**Golden rules:**

- The spec wins over the code.
- Test vectors win over opinions.
- RFCs win over arguments.

---

**Related documents:**

- [Whitepaper](../docs/whitepaper.md) — full design.
- [REPO_STRUCTURE](../REPO_STRUCTURE.md) — repository map.
- [CONTRIBUTING](../CONTRIBUTING.md) — how to help.
- [events.md](./events.md) — start here.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
