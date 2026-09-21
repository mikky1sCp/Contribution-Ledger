
---

# Events

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Related:** [README](./README.md) · [identity.md](./identity.md) · [ledger.md](./ledger.md) · [consensus.md](./consensus.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [Event Envelope](#3-event-envelope)
4. [Canonical Serialization](#4-canonical-serialization)
5. [Hashing and Event IDs](#5-hashing-and-event-ids)
6. [Signatures](#6-signatures)
7. [Parent References (DAG)](#7-parent-references-dag)
8. [Event Types](#8-event-types)
9. [Payload Schemas](#9-payload-schemas)
10. [Validation Rules](#10-validation-rules)
11. [Examples](#11-examples)
12. [Test Vectors](#12-test-vectors)
13. [Open Questions](#13-open-questions)

---

## 1. Overview

An **event** is the atomic unit of the Contribution Ledger. Everything that happens in CL — creating an identity, recording a contribution, confirming it, casting a vote, submitting a compute task — is expressed as an event.

Events are:

- **Immutable.** Once finalized, an event is never modified or deleted.
- **Signed.** Every event is signed by its author.
- **Hash-linked.** Every event references its parents by hash, forming a DAG.
- **Deterministic.** Given the same input, every implementation produces the same event ID.
- **Self-contained.** An event contains everything needed to verify it, except its parents (which are referenced by hash).

State is not stored directly. State is **derived** by applying events in topological order. Two nodes that have the same set of events and apply them in the same way will have the same state.

**This file defines:**

- The event envelope (Section 3).
- How events are serialized (Section 4).
- How events are hashed and identified (Section 5).
- How events are signed (Section 6).
- How events reference each other (Section 7).
- What event types exist (Section 8).
- What each event type contains (Section 9).
- What rules validators enforce (Section 10).

Everything else in the specification builds on this file.

---

## 2. Design Principles

The event format follows seven principles.

### 2.1. Determinism

Given the same event data, every implementation **MUST** produce the same serialization, the same hash, and the same signature.

Non-determinism is a critical bug. It breaks consensus, federation, and test vectors.

### 2.2. Canonical serialization

Events are serialized in **CBOR** (Concise Binary Object Representation) with **deterministic encoding rules**.

JSON is used only for human-readable examples and API responses — never for hashing or signing.

### 2.3. Minimal envelope

The event envelope contains only what is necessary:

- version;
- type;
- author;
- timestamp;
- parents;
- payload;
- signature.

No optional envelope fields. No metadata that can be derived. No redundant data.

### 2.4. Self-describing types

Every event declares its `type`. The type determines the schema of the `payload`.

Implementations **MUST** reject events with unknown types (unless forward compatibility is explicitly enabled).

### 2.5. Append-only

Events are never deleted. Revocation is expressed as a new event (`*.revoke`), not as deletion of the original.

### 2.6. Context-aware

Many events are scoped to a **context** (a community, a repository, a project). Context is part of the payload, not the envelope.

This keeps the envelope simple and lets contexts define their own rules.

### 2.7. Forward-compatible

Implementations **SHOULD** ignore unknown fields in known event types. This allows adding fields in MINOR versions without breaking older nodes.

Implementations **MUST NOT** ignore unknown event types.

---

## 3. Event Envelope

Every event has the same envelope structure, regardless of type.

### 3.1. Structure

```json
{
  "version": 1,
  "type": "contribution.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:abc...", "blake3:def..."],
  "payload": { ... },
  "signature": "ed25519:..."
}
```

### 3.2. Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `version` | integer | MUST | Protocol version. Currently `1`. |
| `type` | string | MUST | Event type. See [Section 8](#8-event-types). |
| `author` | string (DID) | MUST | The identity that created the event. |
| `created_at` | integer | MUST | Unix timestamp in seconds (UTC). |
| `parents` | array of strings | MUST | Event IDs of parent events. May be empty for the genesis event. |
| `payload` | object | MUST | Event-specific data. Schema depends on `type`. |
| `signature` | string | MUST | Ed25519 signature over the event ID. |

### 3.3. Field rules

#### `version`

- **MUST** be an integer.
- **MUST** be `1` for the current protocol version.
- Nodes **MUST** reject events with a `version` they do not support.

#### `type`

- **MUST** be a string.
- **MUST** be one of the defined event types.
- Nodes **MUST** reject unknown types.

#### `author`

- **MUST** be a valid DID (see [identity.md](./identity.md)).
- **MUST** correspond to the public key that produced the signature.
- Nodes **MUST** reject events where the author does not match the signature.

#### `created_at`

- **MUST** be an integer.
- **MUST** be a Unix timestamp in seconds (UTC).
- **MUST NOT** be more than 5 minutes in the future relative to the receiving node's clock (see [Section 10.6](#106-timestamp-validation)).
- **SHOULD** be monotonically increasing per author, but this is not enforced.

#### `parents`

- **MUST** be an array (may be empty).
- **MUST** contain only valid event IDs (hashes).
- **MUST** reference events that exist in the ledger (or are pending).
- **MUST NOT** contain duplicates.
- **SHOULD** reference the author's most recent events and the events they are responding to.
- **MAY** be empty only for the genesis event.

#### `payload`

- **MUST** be an object (CBOR map).
- **MUST** conform to the schema for the given `type`.
- **MUST NOT** contain fields not defined in the schema, unless the schema allows extensions.

#### `signature`

- **MUST** be a valid Ed25519 signature.
- **MUST** be over the event ID (see [Section 5](#5-hashing-and-event-ids)).
- **MUST** verify against the public key encoded in `author`.

### 3.4. What is not in the envelope

The following are **not** part of the envelope:

- **Event ID** — derived from the event (see [Section 5](#5-hashing-and-event-ids)).
- **Context** — part of `payload` where applicable.
- **Nonce** — not used. Events are unique by content, not by nonce.
- **Gas, fee, priority** — none. Events have no cost.
- **Block height, block hash** — none. CL uses a DAG, not a block chain.

### 3.5. Empty parents

Only the **genesis event** may have empty `parents`. All other events **MUST** have at least one parent.

The genesis event is defined by the community that starts the ledger. It is the root of the DAG.

---

## 4. Canonical Serialization

Serialization is critical for determinism. Two implementations that serialize the same event differently will produce different hashes and break compatibility.

### 4.1. Format: CBOR

Events **MUST** be serialized using **CBOR** ([RFC 8949](https://www.rfc-editor.org/rfc/rfc8949.html)) with the following constraints:

- **Deterministic encoding** ([RFC 8949, Section 4.2](https://www.rfc-editor.org/rfc/rfc8949.html#name-deterministically-encoded-c)).
- **No indefinite-length items.** All arrays and maps have explicit lengths.
- **No tags.** CBOR tags are not used.
- **Preferred serialization.** Integers use the smallest encoding that fits.

### 4.2. Map key ordering

Map keys **MUST** be sorted in **bytewise lexicographic order** of their CBOR-encoded form.

For string keys, this means sorting by UTF-8 bytes, not by Unicode code points.

**Example:** keys `"a"`, `"b"`, `"aa"` sort as:

```
"a"  (0x61)
"aa" (0x61 0x61)
"b"  (0x62)
```

Bytewise ordering gives `"a" < "aa" < "b"`. This differs from natural language ordering, and it is intentional.

### 4.3. Integer encoding

Integers **MUST** use the smallest CBOR encoding:

- 0 to 23: 1 byte.
- 24 to 255: 2 bytes.
- 256 to 65535: 3 bytes.
- 65536 to 4294967295: 5 bytes.
- Larger: 9 bytes.

Negative integers use CBOR major type 1.

### 4.4. String encoding

Strings **MUST** be:

- valid UTF-8;
- encoded with CBOR major type 3;
- without normalization (Unicode NFC or NFD are **not** applied — the bytes are used as-is).

**Warning:** two strings that look the same but have different Unicode normalization will produce different hashes. This is intentional. Authors **SHOULD** use NFC for human-readable fields.

### 4.5. Byte strings

Byte strings (e.g., hashes, signatures when not in string form) **MUST** use CBOR major type 2.

### 4.6. Arrays

Arrays **MUST**:

- preserve order (arrays are ordered);
- not contain duplicate elements where the schema forbids it;
- use explicit lengths (no indefinite arrays).

### 4.7. Maps

Maps **MUST**:

- have unique keys (duplicate keys are invalid);
- sort keys as described in [Section 4.2](#42-map-key-ordering);
- use explicit lengths.

### 4.8. Null and undefined

- **Null** (`null`) is allowed where the schema permits.
- **Undefined** is not used. Absent fields are simply absent.

### 4.9. Floats

Floats **MUST NOT** be used in event payloads unless explicitly allowed by the schema.

When floats are used (e.g., in reputation calculations), they **MUST**:

- use IEEE 754 double precision (CBOR major type 7, additional info 27);
- be rounded to 6 decimal places before serialization;
- avoid NaN and Infinity.

**Rationale:** floating-point determinism is hard. Minimizing float usage reduces the risk of cross-implementation divergence.

### 4.10. Example

**JSON (human-readable):**

```json
{
  "version": 1,
  "type": "contribution.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:abc"],
  "payload": {
    "subject": "did:cl:main:alice",
    "action": "code_commit",
    "weight_class": "commit",
    "timestamp": 1730000000
  }
}
```

**CBOR (canonical, hex):**

```
a7                                      # map(7)
   67 76657273696f6e                    # "version"
   01                                   # 1
   64 74797065                          # "type"
   72 636f6e747269627574696f6e2e637265617465  # "contribution.create"
   66 617574686f72                      # "author"
   77 6469643a636c3a6d61696e3a616c696365  # "did:cl:main:alice"
   6a 637265617465645f6174              # "created_at"
   1a 671a6c00                          # 1730000000
   66 706172656e7473                    # "parents"
   81                                   # array(1)
      6a 626c616b65333a616263           # "blake3:abc"
   67 7061796c6f6164                    # "payload"
   a4                                   # map(4)
      67 7375626a656374                 # "subject"
      77 6469643a636c3a6d61696e3a616c696365  # "did:cl:main:alice"
      66 616374696f6e                   # "action"
      6b 636f64655f636f6d6d6974         # "code_commit"
      6c 7765696768745f636c617373       # "weight_class"
      66 636f6d6d6974                   # "commit"
      69 74696d657374616d70             # "timestamp"
      1a 671a6c00                       # 1730000000
```

(The signature is added after hashing and is not part of the canonical form used for the event ID.)

### 4.11. Why CBOR and not JSON?

- **Deterministic.** JSON has multiple valid representations of the same data.
- **Compact.** Binary, smaller than JSON.
- **Typed.** Distinguishes integers from floats, byte strings from text.
- **Widely supported.** Libraries exist in every major language.
- **IETF standard.** RFC 8949.

JSON is used for examples and APIs, but never for hashing or signing.

---

## 5. Hashing and Event IDs

### 5.1. Hash function

Events **MUST** be hashed using **BLAKE3**.

BLAKE3 is chosen for:

- speed (faster than SHA-256);
- security (256-bit output);
- simplicity (no length extension issues);
- wide availability (official implementations in Rust, C, Go, Python, etc.).

### 5.2. What is hashed

The **event ID** is the hash of the **canonical CBOR serialization** of the event **without the `signature` field**.

The `signature` is excluded because:

- it is derived from the event ID, not part of it;
- including it would create a circular dependency.

### 5.3. Event ID format

The event ID is a string with a prefix:

```
blake3:<hex-encoded-hash>
```

**Example:**

```
blake3:7a3b9c1e4f2d5a6b8c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b
```

- Prefix: `blake3:`
- Hash: 64 lowercase hex characters (256 bits).

### 5.4. Canonical form for hashing

To compute the event ID:

1. Remove the `signature` field from the envelope.
2. Serialize the remaining fields as canonical CBOR (Section 4).
3. Hash the CBOR bytes with BLAKE3.
4. Encode the hash as lowercase hex.
5. Prefix with `blake3:`.

### 5.5. Determinism check

Two implementations **MUST** produce the same event ID for the same event data.

Test vectors in `spec/test-vectors/events.json` verify this.

### 5.6. Collisions

BLAKE3 with 256-bit output has negligible collision probability. A collision would be a cryptographic break, not a design failure.

### 5.7. Why not include signature in the ID?

If the signature were part of the ID:

- The ID would depend on the signature.
- The signature depends on the ID.
- Circular dependency.

By excluding the signature, we break the cycle: ID first, then signature over the ID.

### 5.8. IDs in parent references

Parent references use the full event ID format:

```json
"parents": ["blake3:7a3b9c1e...", "blake3:1f2e3d4c..."]
```

Implementations **MUST** validate that parent IDs correspond to existing events.

---

## 6. Signatures

### 6.1. Algorithm

Events **MUST** be signed using **Ed25519** ([RFC 8032](https://www.rfc-editor.org/rfc/rfc8032.html)).

Ed25519 is chosen for:

- speed;
- small keys (32 bytes public, 32 bytes private);
- small signatures (64 bytes);
- strong security;
- wide availability;
- no parameter choices (unlike ECDSA).

### 6.2. What is signed

The signature is over the **event ID** (the BLAKE3 hash of the canonical CBOR without signature).

In other words:

```
signature = Ed25519_sign(private_key, event_id_bytes)
```

Where `event_id_bytes` is the raw 32-byte hash (not the hex string, not the `blake3:` prefix).

### 6.3. Signature format

The signature is a string:

```
ed25519:<base58-signature>
```

**Example:**

```
ed25519:3sF7kQ2mNpL3vR8sT1wY6zA4bC5dE6fG7hJ8kL9mN0pQ1rS2tU3vW4xY5zA6bC7dE8fG9hJ0kL1mN2pQ3rS4tU
```

- Prefix: `ed25519:`
- Signature: Base58-encoded 64-byte signature.

**Why Base58?** It avoids ambiguous characters (`0`, `O`, `I`, `l`), which reduces human error when copying signatures.

### 6.4. Key encoding

Public keys are encoded as **Base58** in DIDs:

```
did:cl:main:<base58-32-byte-pubkey>
```

Private keys are never shared, never stored in events, and never transmitted.

### 6.5. Signature verification

To verify an event:

1. Compute the event ID (Section 5).
2. Extract the public key from `author` (the DID).
3. Decode the signature from Base58.
4. Verify using Ed25519.

If verification fails, the event is invalid and **MUST** be rejected.

### 6.6. Signature malleability

Ed25519 signatures are **not malleable**. There is exactly one valid signature for a given message and key (assuming deterministic signing per RFC 8032).

Implementations **MUST** use deterministic signing (RFC 8032, Section 5.1.6) to ensure reproducibility in test vectors.

### 6.7. Test vector keys

Test vectors use **fixed private keys**. These are publicly known and **MUST NOT** be used in production.

Example fixed key (for test vectors only):

```
private_key: 0000000000000000000000000000000000000000000000000000000000000001
public_key:  4cb5abf6ad79fbf5abbccafcc269d85cd2651ed4b885b5869f241aedf0a5ba29
```

(These are for illustration. Real test vectors will be in `spec/test-vectors/events.json`.)

### 6.8. Key rotation

When a key is rotated (see [identity.md](./identity.md)), old events remain signed with the old key. Signature verification for those events uses the old key.

New events use the new key. The key rotation event links the two.

---

## 7. Parent References (DAG)

Events form a **directed acyclic graph** (DAG), not a linear chain.

### 7.1. Why a DAG?

- **Parallel writes.** Multiple authors can create events simultaneously without contention.
- **No blocks.** There is no "next block" to wait for.
- **Fast finalization.** Events finalize independently, once they have enough validator signatures.

### 7.2. Parent rules

- Every event **MUST** reference at least one parent (except genesis).
- Parents **MUST** exist in the ledger or be pending.
- Parents **MUST NOT** create cycles.
- Parents **MAY** be from any author, not just the same author.

### 7.3. Choosing parents

Authors **SHOULD** reference:

- their own most recent event (to preserve author order);
- the events they are responding to (e.g., the contribution being confirmed);
- the current "head" of the DAG (to ensure inclusion).

**Example:** Alice creates a contribution, then Bob confirms it. Bob's event references:

- Alice's contribution event (the event he is confirming);
- Bob's own most recent event (to preserve his author order);
- the current DAG head (to anchor in the graph).

### 7.4. Genesis event

The **genesis event** is the first event in the ledger. It has empty `parents`.

Genesis is defined by the community that starts the ledger. Its content is a `community.create` event or similar (see [Section 8](#8-event-types)).

Genesis is referenced directly or indirectly by every subsequent event.

### 7.5. Topological order

Events are processed in **topological order**: an event is processed only after all its parents.

Two events with no ancestor relationship **MAY** be processed in either order — the result must be the same (determinism requirement).

### 7.6. Heads and tips

The **heads** of the DAG are events that have no children yet.

- A new event **SHOULD** reference at least one current head.
- If a head is not referenced by any new event within a timeout, it may be "orphaned" (but not deleted).

### 7.7. Merging branches

When two branches of the DAG exist (e.g., two authors writing in parallel), a new event **SHOULD** reference heads from both branches. This merges the branches.

If branches are never merged, they remain separate until a merge event appears.

### 7.8. Cycle prevention

A cycle would mean an event is its own ancestor. This is impossible by construction:

- An event's ID depends on its parents' IDs.
- Parents exist before the event.
- Therefore, an event cannot be its own ancestor.

Implementations **MUST** verify this when accepting events.

---

## 8. Event Types

Event types are organized by category.

### 8.1. Identity events

| Type | Purpose |
|---|---|
| `identity.create` | Create a new DID. |
| `identity.attest` | Organization attests a claim about an identity. |
| `identity.revoke_attest` | Revoke a previous attestation. |
| `identity.recover` | Recover access to an identity. |
| `identity.key_rotate` | Rotate the signing key. |
| `identity.deactivate` | Mark an identity as inactive. |

### 8.2. Contribution events

| Type | Purpose |
|---|---|
| `contribution.create` | Claim a contribution. |
| `contribution.confirm` | Confirm a contribution. |
| `contribution.revoke` | Revoke a contribution. |
| `contribution.dispute` | Dispute a contribution. |

### 8.3. Bounty events

| Type | Purpose |
|---|---|
| `bounty.create` | Create a bounty. |
| `bounty.fund` | Fund a bounty's escrow. |
| `bounty.claim` | Claim a bounty. |
| `bounty.submit` | Submit work for a bounty. |
| `bounty.complete` | Complete a bounty and release payment. |
| `bounty.cancel` | Cancel a bounty. |
| `bounty.dispute` | Open a dispute. |
| `bounty.resolve` | Resolve a dispute. |

### 8.4. Compute events

| Type | Purpose |
|---|---|
| `compute.task.create` | Create a compute task. |
| `compute.task.claim` | Claim a task. |
| `compute.task.submit` | Submit a result. |
| `compute.task.verify` | Verify a result. |
| `compute.task.reject` | Reject a result. |
| `compute.task.complete` | Mark task as complete. |
| `compute.task.dispute` | Open a dispute. |
| `compute.executor.register` | Register an executor. |
| `compute.executor.attest` | Attest hardware capabilities. |

### 8.5. Governance events

| Type | Purpose |
|---|---|
| `vote.create` | Create a proposal. |
| `vote.cast` | Cast a vote. |
| `vote.delegate` | Delegate voting power. |
| `vote.undelegate` | Revoke a delegation. |
| `vote.close` | Close a vote. |
| `role.grant` | Grant a role. |
| `role.revoke` | Revoke a role. |

### 8.6. System events

| Type | Purpose |
|---|---|
| `validator.add` | Add a validator. |
| `validator.remove` | Remove a validator. |
| `rule.change` | Change a rule. |
| `checkpoint` | Publish a checkpoint. |
| `fork.declare` | Declare a fork. |
| `payment.record` | Record a payment. |

### 8.7. Community events

| Type | Purpose |
|---|---|
| `community.create` | Create a new community (context). |
| `community.update` | Update community rules. |
| `community.join` | Join a community. |
| `community.leave` | Leave a community. |

### 8.8. Full list

Event types **MUST** be one of the above. Implementations **MUST** reject unknown types.

New event types are added through the RFC process (MINOR version bump).

---

## 9. Payload Schemas

Each event type has a defined payload schema. This section defines the schemas for the most important types.

### 9.1. `identity.create`

```json
{
  "did": "did:cl:main:alice",
  "pubkey": "base58:...",
  "recovery_commitment": "blake3:...",
  "metadata": {
    "display_name": "Alice",
    "context": "optional"
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `did` | string | MUST | The new DID. Must match `pubkey`. |
| `pubkey` | string | MUST | The public key (Base58). |
| `recovery_commitment` | string | MAY | Commitment to recovery keys. |
| `metadata` | object | MAY | Display name, context, etc. |

**Validation:**

- `did` **MUST** be a valid DID format.
- `did` **MUST** encode the same key as `pubkey`.
- The event author **MUST** be the same as `did`.

### 9.2. `contribution.create`

```json
{
  "subject": "did:cl:main:alice",
  "issuer": "did:cl:org:projectX",
  "action": "code_commit",
  "context": "repo:github.com/x/y",
  "weight_class": "commit",
  "evidence": [
    {"type": "hash", "algo": "sha256", "value": "..."},
    {"type": "link", "value": "ipfs://..."}
  ],
  "timestamp": 1730000000
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `subject` | string (DID) | MUST | The identity that did the work. |
| `issuer` | string (DID) | MAY | The identity that attests the work. |
| `action` | string | MUST | The type of action. |
| `context` | string | MAY | The community or project. |
| `weight_class` | string | MUST | The weight class (determines CU value). |
| `evidence` | array | MAY | Hashes or links to evidence. |
| `timestamp` | integer | MUST | When the work was done (Unix time). |

**Validation:**

- The event author **MUST** be either `subject` or `issuer`.
- If `context` is present, it **MUST** refer to a known community.
- `weight_class` **MUST** be defined in the context's rules.
- `evidence` entries **MUST** have `type` and either `value` or `link`.

### 9.3. `contribution.confirm`

```json
{
  "contribution_id": "blake3:...",
  "quality": 0.9,
  "comment": "Looks good"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `contribution_id` | string | MUST | The event ID of the contribution. |
| `quality` | float | MAY | Quality coefficient (0..1). Default: 1.0. |
| `comment` | string | MAY | Explanation. |

**Validation:**

- `contribution_id` **MUST** reference a `contribution.create` event.
- The confirmer **MUST** have the right to confirm in the context.
- The confirmer **MUST NOT** be the same as the subject (no self-confirmation).

### 9.4. `bounty.create`

```json
{
  "task": "Write API documentation",
  "context": "repo:github.com/x/y",
  "reward": {"amount": 500, "currency": "USD", "method": "escrow"},
  "escrow_id": "did:cl:escrow:main:123",
  "deadline": 1730100000,
  "requirements": ["3 reviews", "grammar check"],
  "weight_class": "bounty_doc"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `task` | string | MUST | Description of the task. |
| `context` | string | MUST | The context of the bounty. |
| `reward` | object | MUST | Amount, currency, method. |
| `escrow_id` | string | MUST | The escrow identity. |
| `deadline` | integer | MAY | Unix timestamp. |
| `requirements` | array | MAY | Requirements for completion. |
| `weight_class` | string | MUST | Weight class for CU. |

### 9.5. `vote.create`

```json
{
  "proposal": "change_weight_code_review",
  "context": "repo:github.com/x/y",
  "options": ["yes", "no", "abstain"],
  "deadline": 1730100000,
  "threshold": "2/3",
  "weighting": "quadratic",
  "snapshot": "blake3:..."
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `proposal` | string | MUST | The proposal being voted on. |
| `context` | string | MUST | The context of the vote. |
| `options` | array | MUST | Voting options. |
| `deadline` | integer | MUST | Unix timestamp. |
| `threshold` | string | MUST | Required threshold (e.g., "2/3", "50%+1"). |
| `weighting` | string | MUST | "simple", "quadratic", "delegated". |
| `snapshot` | string | MUST | Hash of reputation state at creation. |

### 9.6. `vote.cast`

```json
{
  "vote_id": "blake3:...",
  "option": "yes",
  "weight_proof": "optional"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `vote_id` | string | MUST | The event ID of the vote. |
| `option` | string | MUST | One of the defined options. |
| `weight_proof` | string | MAY | ZK proof for secret voting. |

### 9.7. `compute.task.create`

```json
{
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

| Field | Type | Required | Description |
|---|---|---|---|
| `task` | object | MUST | Task specification. |
| `reward` | object | MUST | Payment. |
| `redundancy` | integer | MUST | Number of redundant runs. |
| `verification` | string | MUST | Verification method. |
| `deadline` | integer | MAY | Unix timestamp. |

### 9.8. Other event types

The remaining event types have similar schemas. They are documented in their respective spec files:

- **Identity events** — [identity.md](./identity.md).
- **Bounty events** — [bounty.md](./bounty.md).
- **Compute events** — [compute.md](./compute.md).
- **Governance events** — [vote.md](./vote.md).
- **System events** — [consensus.md](./consensus.md).

---

## 10. Validation Rules

Every node **MUST** validate events before accepting them. Invalid events **MUST** be rejected.

### 10.1. Structural validation

- `version` **MUST** be supported.
- `type` **MUST** be known.
- `author` **MUST** be a valid DID.
- `created_at` **MUST** be an integer.
- `parents` **MUST** be an array of valid event IDs.
- `payload` **MUST** conform to the schema for `type`.
- `signature` **MUST** be present and valid.

### 10.2. Signature validation

- The signature **MUST** verify against the public key in `author`.
- The signature **MUST** be over the correct event ID.
- If `author` was rotated, the signature **MUST** use the current key (or the key valid at `created_at`).

### 10.3. Parent validation

- Every parent **MUST** exist in the ledger or be pending.
- Parents **MUST** be processed before the event (topological order).
- Parents **MUST NOT** form a cycle (guaranteed by construction).

### 10.4. Semantic validation

- `subject` in contribution events **MUST** be a valid DID.
- `context` **MUST** refer to a known community (if required).
- `weight_class` **MUST** be defined in the context.
- `contribution_id` **MUST** reference a valid contribution.
- `vote_id` **MUST** reference a valid vote.
- `escrow_id` **MUST** reference a valid escrow.

### 10.5. Authorization validation

- Only the author of an event may sign it.
- Only authorized identities may perform certain actions:
  - Confirming a contribution: must have the right role in the context.
  - Granting a role: must be a council member.
  - Adding a validator: must be approved by the community.
  - Creating a bounty: must have reputation > threshold (or be an organization).

### 10.6. Timestamp validation

- `created_at` **MUST** be within ±5 minutes of the receiving node's clock.
- `created_at` **MUST NOT** be in the future by more than 5 minutes.
- For historical events, timestamps are accepted as-is (not re-validated).

### 10.7. Duplicate validation

- An event with the same `id` **MUST** be rejected if already present.
- Events are deduplicated by `id`.

### 10.8. Rate limiting

- Nodes **MAY** enforce rate limits per author (e.g., 100 events per hour).
- Rate limits are a local policy, not a protocol rule.

### 10.9. Rejection reasons

Rejected events **SHOULD** return a reason:

- `invalid_signature`
- `unknown_type`
- `unsupported_version`
- `missing_parent`
- `unauthorized`
- `invalid_payload`
- `duplicate`
- `rate_limited`

### 10.10. Invalid events

Invalid events **MUST NOT** be added to the ledger. They **MAY** be stored in a "rejected" log for debugging, but this is not part of the protocol.

---

## 11. Examples

### 11.1. Minimal contribution event

**JSON:**

```json
{
  "version": 1,
  "type": "contribution.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:abc..."],
  "payload": {
    "subject": "did:cl:main:alice",
    "action": "code_commit",
    "weight_class": "commit",
    "timestamp": 1730000000
  },
  "signature": "ed25519:..."
}
```

### 11.2. Confirmation event

```json
{
  "version": 1,
  "type": "contribution.confirm",
  "author": "did:cl:main:bob",
  "created_at": 1730000100,
  "parents": ["blake3:abc...", "blake3:def..."],
  "payload": {
    "contribution_id": "blake3:abc...",
    "quality": 0.9,
    "comment": "Clean code, good tests."
  },
  "signature": "ed25519:..."
}
```

### 11.3. Bounty creation

```json
{
  "version": 1,
  "type": "bounty.create",
  "author": "did:cl:org:startupX",
  "created_at": 1730000200,
  "parents": ["blake3:ghi..."],
  "payload": {
    "task": "Write API documentation for v2",
    "context": "repo:github.com/x/y",
    "reward": {"amount": 500, "currency": "USD", "method": "escrow"},
    "escrow_id": "did:cl:escrow:main:123",
    "deadline": 1730100000,
    "requirements": ["3 peer reviews", "grammar check"],
    "weight_class": "bounty_doc"
  },
  "signature": "ed25519:..."
}
```

### 11.4. Vote

```json
{
  "version": 1,
  "type": "vote.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000300,
  "parents": ["blake3:jkl..."],
  "payload": {
    "proposal": "change_weight_code_review",
    "context": "repo:github.com/x/y",
    "options": ["yes", "no", "abstain"],
    "deadline": 1730100000,
    "threshold": "2/3",
    "weighting": "quadratic",
    "snapshot": "blake3:mno..."
  },
  "signature": "ed25519:..."
}
```

---

## 12. Test Vectors

Test vectors live in `spec/test-vectors/events.json`.

### 12.1. Format

```json
{
  "description": "Minimal contribution event",
  "input": { ... },
  "expected": {
    "canonical_cbor_hex": "a7...",
    "event_id": "blake3:...",
    "signature": "ed25519:..."
  }
}
```

### 12.2. Coverage

Test vectors **MUST** cover:

- Every event type, at least once.
- Minimal valid events.
- Events with all optional fields.
- Events with empty `parents` (genesis).
- Events with multiple parents.
- Invalid events (bad signature, missing fields, wrong types).
- Unicode edge cases (combining characters, emoji, normalization).
- Integer edge cases (0, 1, 23, 24, 255, 256, 65535, 65536, 2^32-1).
- Map key ordering edge cases.

### 12.3. Deterministic keys

Test vectors use fixed keys. Example:

```
private_key_hex: 0000000000000000000000000000000000000000000000000000000000000001
public_key_hex:  4cb5abf6ad79fbf5abbccafcc269d85cd2651ed4b885b5869f241aedf0a5ba29
```

### 12.4. How to verify

1. Read the test vector.
2. Serialize the input as canonical CBOR.
3. Compare to `canonical_cbor_hex`.
4. Hash with BLAKE3.
5. Compare to `event_id`.
6. Sign with the fixed key.
7. Compare to `signature`.

If any step differs, the implementation is not compliant.

### 12.5. Adding test vectors

To add a test vector:

1. Open an issue.
2. Submit a PR to `spec/test-vectors/events.json`.
3. Include a reference implementation output.

---

## 13. Open Questions

- Should events support **extensions** (custom fields) for community-specific data?
- How to handle **large payloads** (e.g., datasets) — inline or by reference?
- Should there be a **maximum event size**? If so, what?
- How to handle **time skew** across nodes?
- Should **parent selection** be part of the protocol, or left to implementations?
- How to prevent **parent spam** (referencing many irrelevant parents)?
- Should there be a **genesis protocol** (standardized way to start a ledger)?
- How to handle **compaction** of old events without losing verifiability?
- Should **checkpoints** be a separate event type or a separate structure?
- How to handle **multiple signatures** (multisig events)?

These will be resolved through RFCs and community discussion.

---

## Summary

**An event is:**

- Immutable.
- Signed (Ed25519).
- Hash-linked (BLAKE3).
- Serialized canonically (CBOR).
- Self-contained.
- Typed.

**The event envelope contains:**

- `version`, `type`, `author`, `created_at`, `parents`, `payload`, `signature`.

**The event ID is:**

- BLAKE3 hash of the canonical CBOR without the signature.
- Format: `blake3:<hex>`.

**Parents form a DAG:**

- Every event references at least one parent (except genesis).
- No cycles.
- Topological order for processing.

**Validation:**

- Structural, signature, parent, semantic, authorization, timestamp, duplicate, rate limit.

**Test vectors:**

- In `spec/test-vectors/events.json`.
- Cover every event type and edge cases.
- Used to verify compatibility.

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [identity.md](./identity.md) — identity events.
- [contribution.md](./contribution.md) — contribution events.
- [ledger.md](./ledger.md) — how events are stored.
- [consensus.md](./consensus.md) — how events are finalized.
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
