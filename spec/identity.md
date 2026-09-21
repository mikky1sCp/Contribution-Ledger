# Identity

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md)  
**Related:** [contribution.md](./contribution.md) · [reputation.md](./reputation.md) · [consensus.md](./consensus.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [Cryptographic Primitives](#3-cryptographic-primitives)
4. [DID Format](#4-did-format)
5. [Identity Creation](#5-identity-creation)
6. [Identity Levels](#6-identity-levels)
7. [Attestations](#7-attestations)
8. [Recovery](#8-recovery)
9. [Key Rotation](#9-key-rotation)
10. [Multiple Identities](#10-multiple-identities)
11. [Deactivation](#11-deactivation)
12. [Validation Rules](#12-validation-rules)
13. [Examples](#13-examples)
14. [Test Vectors](#14-test-vectors)
15. [Open Questions](#15-open-questions)

---

## 1. Overview

An **identity** in Contribution Ledger is a cryptographic keypair that authorizes actions. Every event is signed by an identity. Every contribution, confirmation, vote, and bounty is attributed to an identity.

CL does **not** require real names, emails, or personal data. An identity is a public key. Everything else — display name, affiliations, verification — is optional and expressed through **attestations**.

**This file defines:**

- How keys are generated and encoded (Section 3).
- How DIDs are formatted (Section 4).
- How identities are created (Section 5).
- What identity levels exist (Section 6).
- How attestations work (Section 7).
- How recovery works (Section 8).
- How key rotation works (Section 9).
- How multiple identities interact (Section 10).
- How identities are deactivated (Section 11).
- What rules validators enforce (Section 12).

Identity is the foundation of trust in CL. Without a well-defined identity model, reputation is meaningless.

---

## 2. Design Principles

### 2.1. No personal data in the protocol

CL **MUST NOT** store names, emails, phone numbers, addresses, passports, or biometrics on the ledger.

What is stored:

- public keys;
- DIDs;
- attestations (signed claims, not personal data);
- signatures.

Personal data **MAY** be stored off-ledger (in profiles, in external systems), but it is never required by the protocol.

### 2.2. Pseudonymity by default

New identities are **pseudonymous**. They are not linked to real-world identity unless the holder chooses to link them.

### 2.3. Verifiability without identification

An identity can prove things without revealing who it is:

- "I have reputation > 1000 in this context."
- "I am a member of this organization."
- "I have completed 50 bounties."

These are proven via **attestations** and **zero-knowledge proofs**, not via personal data.

### 2.4. Recoverable

Losing a private key **MUST NOT** mean losing reputation. Recovery is part of the protocol.

### 2.5. Rotatable

Keys **MUST** be rotatable. A compromised key can be replaced without losing history.

### 2.6. Forkable

If a community disagrees with an identity's behavior, it can ignore or blacklist the identity. If a key is compromised, the community can be notified via attestation.

### 2.7. Contextual

An identity exists globally, but its **reputation is contextual**. Reputation in one community does not automatically transfer to another.

---

## 3. Cryptographic Primitives

### 3.1. Signature algorithm

Identities **MUST** use **Ed25519** ([RFC 8032](https://www.rfc-editor.org/rfc/rfc8032.html)) for signing.

| Property | Value |
|---|---|
| Public key size | 32 bytes |
| Private key size | 32 bytes (seed) |
| Signature size | 64 bytes |
| Security level | ~128 bits |
| Deterministic | Yes (RFC 8032, Section 5.1.6) |

### 3.2. Key exchange

For encrypted communication and private contexts, identities **MAY** use **X25519** for key exchange.

| Property | Value |
|---|---|
| Public key size | 32 bytes |
| Private key size | 32 bytes |
| Shared secret size | 32 bytes |

### 3.3. Derivation

If an identity needs both signing and encryption keys, they **SHOULD** be derived from a single master seed using **HKDF-SHA256**:

```
signing_key   = HKDF(seed, info="cl-sign-ed25519",   length=32)
encryption_key = HKDF(seed, info="cl-enc-x25519",    length=32)
```

The master seed is never shared and never stored on-ledger.

### 3.4. Encoding

- **Keys:** Base58 (Bitcoin alphabet).
- **Signatures:** Base58, prefixed with `ed25519:`.
- **DIDs:** `did:cl:<network>:<base58-pubkey>`.
- **Hashes:** `blake3:<hex>`.

### 3.5. Hash function

**BLAKE3** is used for:

- event IDs (see [events.md](./events.md#5-hashing-and-event-ids));
- recovery commitments;
- attestation IDs;
- key rotation links.

### 3.6. Randomness

Key generation **MUST** use a cryptographically secure random number generator (CSPRNG). Do not derive keys from passwords, timestamps, or weak sources.

**Recommended:** `/dev/urandom`, `getrandom(2)`, or the operating system's CSPRNG. Never `Math.random()`, `rand()` without seeding, or `time()`.

---

## 4. DID Format

### 4.1. Structure

```
did:cl:<network>:<base58-pubkey>
```

| Component | Description |
|---|---|
| `did` | Fixed prefix (Decentralized Identifier). |
| `cl` | Method name (Contribution Ledger). |
| `<network>` | Network identifier (e.g., `main`, `test`, `dev`). |
| `<base58-pubkey>` | Base58-encoded Ed25519 public key (32 bytes). |

### 4.2. Examples

**Main network:**

```
did:cl:main:7Xk9fQ2mNpL3vR8sT1wY6zA4bC5dE6fG7hJ8kL9mN0pQ
```

**Test network:**

```
did:cl:test:3aB4cD5eF6gH7iJ8kL9mN0pQ1rS2tU3vW4xY5zA6bC7d
```

**Development network:**

```
did:cl:dev:9zY8xW7vU6tS5rQ4pN3mL2kJ1iH0gF9eD8cB7aZ6yX5w
```

### 4.3. Network identifiers

| Network | Purpose |
|---|---|
| `main` | Production. Real contributions, real money. |
| `test` | Testnet. Fake contributions, no money. |
| `dev` | Development. Local testing. |
| Other | Communities **MAY** define custom networks. |

Network identifiers are **case-sensitive** and **lowercase**.

### 4.4. Base58 encoding

Public keys **MUST** be encoded in **Base58** using the **Bitcoin alphabet**:

```
123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz
```

Characters not included: `0` (zero), `O` (uppercase o), `I` (uppercase i), `l` (lowercase L). This avoids visual ambiguity.

### 4.5. Base58 decoding

To extract the public key:

1. Strip the `did:cl:<network>:` prefix.
2. Decode the remaining string as Base58.
3. Result **MUST** be exactly 32 bytes.
4. If decoding fails or length is wrong, the DID is invalid.

### 4.6. Case sensitivity

- Network identifiers: **lowercase only**.
- Base58 public keys: **case-sensitive**.
- DIDs are **case-sensitive** as a whole.

Two DIDs that differ only in case are **different identities**.

### 4.7. Uniqueness

A DID is unique if and only if its public key is unique. Two identities with the same public key are the same identity (or a collision, which is cryptographically infeasible for Ed25519).

### 4.8. No registration

DIDs are **not registered** anywhere. They are derived from keys. Creating a DID is a local operation.

To use a DID in the ledger, the holder creates an `identity.create` event (Section 5). Until then, the DID exists mathematically but not socially.

### 4.9. Resolution

Resolving a DID means looking up its state in the ledger:

- is it active?
- what is its reputation?
- what attestations does it have?
- what key is current?

Resolution is done by querying a node's API (see [api.md](./api.md)).

### 4.10. Comparison to W3C DID

CL's DID format is **compatible in spirit** with [W3C DID](https://www.w3.org/TR/did-core/) but uses a custom method (`cl`). It is not registered with the W3C DID registry.

A future version **MAY** register the method formally.

---

## 5. Identity Creation

### 5.1. Process

1. Generate an Ed25519 keypair (Section 3).
2. Encode the public key as Base58.
3. Construct the DID: `did:cl:<network>:<base58-pubkey>`.
4. (Optional) Generate a recovery commitment.
5. Create an `identity.create` event.
6. Sign and submit the event.

### 5.2. Event structure

```json
{
  "version": 1,
  "type": "identity.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "did": "did:cl:main:alice",
    "pubkey": "base58:7Xk9fQ2mNpL3vR8sT1wY6zA4bC5dE6fG7hJ8kL9mN0pQ",
    "recovery_commitment": "blake3:...",
    "metadata": {
      "display_name": "Alice",
      "context": "optional"
    }
  },
  "signature": "ed25519:..."
}
```

### 5.3. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `did` | string | MUST | The new DID. |
| `pubkey` | string | MUST | The public key (Base58). |
| `recovery_commitment` | string | MAY | Commitment to recovery keys. |
| `metadata` | object | MAY | Display name, description, links. |

### 5.4. Validation

- `did` **MUST** be a valid DID (Section 4).
- `pubkey` **MUST** match the key encoded in `did`.
- The event **author** **MUST** equal `did`.
- The **signature** **MUST** verify against `pubkey`.
- `did` **MUST NOT** already exist in the ledger.

### 5.5. Genesis identity

The **genesis event** of a ledger (see [events.md](./events.md#74-genesis-event)) **MAY** create the first identity. This is the founding identity of the community.

Genesis identity **MAY** have additional privileges defined by the community (e.g., initial validator, initial council member).

### 5.6. Metadata

The `metadata` field is **optional** and **informative**. It does not affect validation.

| Field | Type | Description |
|---|---|---|
| `display_name` | string | Human-readable name. |
| `description` | string | Short bio. |
| `avatar` | string | URL or IPFS hash. |
| `links` | array | Links to external profiles. |

Metadata **MAY** be updated by creating a new `identity.update` event (similar to `identity.create`).

### 5.7. Recovery commitment

If the identity wants to enable recovery (Section 8), it **MUST** include a `recovery_commitment` in the creation event.

The commitment is:

```
recovery_commitment = BLAKE3(recovery_config)
```

Where `recovery_config` is a canonical CBOR structure containing:

- list of recovery contact DIDs (or their public keys);
- threshold (M of N);
- optional expiry.

The recovery config itself is **not** published at creation. Only the commitment is. This prevents attackers from seeing who the recovery contacts are.

### 5.8. Multiple creation attempts

If two `identity.create` events exist for the same DID:

- The **first** one (by DAG order) is valid.
- Subsequent ones **MUST** be rejected.

If they are in parallel branches of the DAG, the ledger forks — see [consensus.md](./consensus.md) for resolution.

### 5.9. No cost

Creating an identity is **free**. There is no fee, no stake, no proof-of-work.

This is intentional: identity should not be a financial barrier.

Sybil resistance is achieved through other means (attestations, reputation, invitation — see Section 6).

---

## 6. Identity Levels

Not all identities are equal. CL defines four levels, each with different rights.

### 6.1. Levels

| Level | Name | How to obtain | Rights |
|---|---|---|---|
| 0 | Anonymous | Generate key | Read, limited write |
| 1 | Pseudonymous | Invitation from a member | Contribute, earn CU |
| 2 | Verified | Attestation from an organization | Vote, roles, bounties |
| 3 | Organizational | Organization key | Issue attestations, create bounties |

### 6.2. Level 0 — Anonymous

**Obtained by:** generating a keypair and creating an `identity.create` event.

**Rights:**

- Read the ledger.
- Create `contribution.create` events with `weight_class` marked as `unverified`.
- Confirm own contributions (which count for 0 CU until verified by a higher-level identity).

**Limits:**

- Cannot vote.
- Cannot confirm others' contributions.
- Cannot claim bounties.
- Cannot receive grants.
- Cannot be a validator.

**Purpose:** allows anyone to participate read-only or as a "sandbox" identity. Useful for testing, exploration, and slow onboarding.

### 6.3. Level 1 — Pseudonymous

**Obtained by:** invitation from an existing Level 1+ identity. The inviter creates an `identity.invite` event (an attestation, see Section 7).

**Rights:**

- Everything from Level 0.
- Create `contribution.create` events with full weight.
- Confirm contributions (if reputation threshold is met).
- Receive CU and reputation.
- Comment and discuss.
- Join communities.

**Limits:**

- Cannot vote on governance (unless community rules allow).
- Cannot hold roles (auditor, maintainer, council).
- Cannot claim high-value bounties.
- Cannot be a validator.

**Purpose:** allows real participation without requiring legal identity. Suitable for open-source, volunteer work, and pseudonymous contribution.

### 6.4. Level 2 — Verified

**Obtained by:** attestation from a recognized organization (Section 7). The organization signs a claim binding the DID to a real-world identity (or a verified pseudonym).

**Rights:**

- Everything from Level 1.
- Vote in governance (if community rules allow).
- Hold roles (auditor, maintainer, council).
- Claim bounties with escrow.
- Receive grants.
- Be a validator (if technical requirements are met).

**Limits:**

- Cannot issue attestations (unless the identity is also an organization).
- Cannot create bounties on behalf of an organization (unless authorized).

**Purpose:** allows full participation in the economy. Required for anything involving money, legal responsibility, or high trust.

### 6.5. Level 3 — Organizational

**Obtained by:** creating a special `identity.create` event with `type: "organization"` and being recognized by the community (e.g., via a vote).

**Rights:**

- Everything from Level 2.
- Issue attestations.
- Create bounties and fund escrow.
- Grant roles.
- Represent a legal entity.

**Limits:**

- Must be recognized by at least one community.
- Subject to community rules.

**Purpose:** allows companies, funds, cooperatives, and other organizations to participate officially.

### 6.6. Level transitions

- **0 → 1:** invitation from a Level 1+ identity.
- **1 → 2:** attestation from a recognized organization.
- **2 → 3:** community recognition (vote).
- **Any → lower:** voluntary downgrade or community action (e.g., revocation of attestation).

Levels are **not** automatically granted. Each transition requires a signed event.

### 6.7. Level in different contexts

An identity may have different levels in different contexts:

- Level 2 in one community.
- Level 1 in another.
- Level 0 in a third.

Each community defines its own rules for what levels mean and how they are granted.

### 6.8. Level checks

When an event requires a certain level (e.g., voting requires Level 2), validators **MUST** check:

- the identity's level **in that context**;
- the level at the time of the event (using `created_at`).

Levels are **historical**. An identity that was Level 2 at the time of a vote is counted as Level 2 for that vote, even if later downgraded.

---

## 7. Attestations

An **attestation** is a signed claim by one identity about another.

### 7.1. Purpose

Attestations are how CL expresses:

- "This DID belongs to a real person." (identity verification)
- "This DID is a member of our organization." (membership)
- "This DID has completed our course." (education)
- "This DID is a trusted partner." (trust)
- "This DID has been banned by our community." (negative attestation)

### 7.2. Structure

```json
{
  "version": 1,
  "type": "identity.attest",
  "author": "did:cl:org:university",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "subject": "did:cl:main:alice",
    "claim": "student",
    "value": {
      "program": "Computer Science",
      "year": 2024,
      "verified": true
    },
    "valid_until": 1760000000,
    "evidence": [
      {"type": "link", "value": "ipfs://..."}
    ]
  },
  "signature": "ed25519:..."
}
```

### 7.3. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `subject` | string (DID) | MUST | The identity being attested. |
| `claim` | string | MUST | The type of claim. |
| `value` | object | MAY | Claim-specific data. |
| `valid_until` | integer | MAY | Unix timestamp. |
| `evidence` | array | MAY | Links or hashes supporting the claim. |

### 7.4. Claim types

Standard claim types (communities **MAY** define their own):

| Claim | Meaning |
|---|---|
| `member` | Subject is a member of the issuer. |
| `student` | Subject is a student. |
| `employee` | Subject is an employee. |
| `alumni` | Subject is an alumnus. |
| `verified_human` | Subject is a verified human. |
| `verified_organization` | Subject is a verified organization. |
| `skill` | Subject has a specific skill. |
| `ban` | Subject is banned (negative). |
| `endorsement` | Subject is endorsed by the issuer. |

### 7.5. Validation

- The **author** **MUST** be a valid identity.
- The author **MUST** have the right to issue the claim (e.g., only an organization can issue `member`).
- The **subject** **MUST** be a valid identity.
- The **subject** **MUST NOT** equal the author (no self-attestation).
- If `valid_until` is set, it **MUST** be in the future at `created_at`.

### 7.6. Revocation

To revoke an attestation:

```json
{
  "type": "identity.revoke_attest",
  "author": "did:cl:org:university",
  "payload": {
    "attestation_id": "blake3:...",
    "reason": "student graduated"
  }
}
```

Only the **original issuer** may revoke. Revocation is permanent (in the sense that the attestation is marked as revoked; the history is preserved).

### 7.7. Multiple attestations

An identity **MAY** have multiple attestations for the same claim from different issuers.

Example: Alice has `verified_human` attestations from three different organizations. This strengthens her claim.

### 7.8. Attestation chains

Attestations can form chains:

- Organization A attests Organization B is legitimate.
- Organization B attests Alice is a member.

This creates a **web of trust**. Communities **MAY** use graph analysis to determine trust levels.

### 7.9. Negative attestations

A `ban` claim is a **negative** attestation. It signals that the issuer considers the subject untrustworthy.

Rules:

- Bans are **context-specific** (a ban in one community does not affect others).
- Bans **MUST** include a reason.
- Bans **MAY** be contested via a `identity.dispute` event.
- Communities **MAY** ignore bans from issuers they do not trust.

### 7.10. Privacy

Attestations do **not** reveal personal data. They reveal only:

- that the issuer attests to the claim;
- the claim type;
- optional metadata.

To verify "Alice is a student" without revealing her name:

- the university attests "DID `did:cl:main:alice` is a student";
- the DID is not linked to Alice's legal name.

To link the DID to a legal name (for KYC or legal purposes), an additional attestation is needed, which the user can choose to disclose selectively.

### 7.11. Expiry

Attestations with `valid_until` automatically expire.

Expired attestations:

- are still in the ledger (immutable);
- are ignored by validators when computing current state;
- MAY be renewed by a new attestation.

### 7.12. Attestation as a service

Organizations **MAY** offer attestation as a service:

- a university attests its graduates;
- a company attests its employees;
- a KYC provider attests verified humans.

This is not part of the protocol. It is a market that the protocol enables.

---

## 8. Recovery

Losing a private key **MUST NOT** mean losing reputation. CL defines recovery mechanisms.

### 8.1. Recovery models

Three models are supported:

1. **Social recovery** — a set of trusted contacts can help recover access.
2. **Multisig recovery** — a backup key (or keys) can recover access.
3. **Time-locked recovery** — after a delay, a recovery key can take over.

A single identity **MAY** use multiple models.

### 8.2. Social recovery

#### 8.2.1. Setup

At identity creation (or later), the identity commits to a recovery configuration:

```
recovery_config = {
  "contacts": [list of DIDs or pubkeys],
  "threshold": M,       // M of N
  "delay": seconds,     // optional delay
}
recovery_commitment = BLAKE3(canonical_cbor(recovery_config))
```

Only the commitment is published. The config itself is shared privately with the contacts.

#### 8.2.2. Recovery process

If the private key is lost:

1. The identity's contacts learn about the loss out-of-band.
2. The contacts create `identity.recover` events, each signed by their own key, proposing a new key for the identity.
3. When **M** of **N** contacts have signed, the recovery is complete.
4. If `delay` is set, there is an additional waiting period during which the old key (if still available) can cancel the recovery.

#### 8.2.3. Recovery event

```json
{
  "version": 1,
  "type": "identity.recover",
  "author": "did:cl:main:contact1",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "subject": "did:cl:main:alice",
    "new_pubkey": "base58:...",
    "reason": "key_lost"
  },
  "signature": "ed25519:..."
}
```

Each contact signs their own event. Once threshold is met, a `identity.recover_complete` event is created (by any party), which finalizes the recovery.

#### 8.2.4. Validation

- Each recovery event **MUST** be signed by a listed contact.
- The contact **MUST** have been in the commitment at the time of the original identity creation (or at the last update).
- The threshold **MUST** be met.
- If `delay` is set, the recovery is not valid until the delay has passed.

### 8.3. Multisig recovery

#### 8.3.1. Setup

At identity creation, the identity **MAY** include a backup public key:

```
recovery_backup_pubkey = "base58:..."
```

This key is stored offline by the identity holder.

#### 8.3.2. Recovery

If the primary key is lost:

1. The holder creates an `identity.recover` event signed by the backup key.
2. The event proposes a new primary key.
3. If `delay` is set, waiting period applies.

#### 8.3.3. Validation

- The recovery event **MUST** be signed by the backup key.
- The backup key **MUST** match the commitment from creation.

### 8.4. Time-locked recovery

Any recovery method **MAY** include a `delay` parameter.

During the delay:

- The old key (if still active) **MAY** create a `identity.cancel_recover` event to stop the recovery.
- No other events signed by the old key are accepted during recovery.
- After the delay, recovery is final.

This protects against:

- theft of the backup key;
- malicious recovery by colluding contacts.

Typical delay: 7 days.

### 8.5. Recovery commitment update

To change the recovery configuration (e.g., change contacts):

1. The identity creates an `identity.update` event with a new `recovery_commitment`.
2. The old commitment is invalidated.
3. Contacts **MUST** be re-issued the new config offline.

### 8.6. Loss without recovery

If an identity loses its key and has no recovery mechanism:

- The identity is effectively dead.
- The ledger still contains all history.
- Reputation remains attributed to the DID, but no new events can be signed.
- A community **MAY** choose to transfer reputation to a new DID (by vote), but this is outside the protocol.

### 8.7. Recovery does not reset history

Recovery changes the key, not the identity.

- All historical events remain valid.
- All reputation remains attributed to the same DID.
- Attestations remain valid (unless the issuer revokes them).

The DID does not change. Only the key that controls it changes.

---

## 9. Key Rotation

Key rotation replaces the signing key without losing the identity.

### 9.1. Why rotate

- **Compromise.** If a key is suspected of being leaked, rotate immediately.
- **Scheduled.** Best practice: rotate every 1–2 years.
- **Algorithm upgrade.** If a stronger algorithm becomes available, rotate to it (future).
- **Hardware change.** If moving to a hardware wallet, rotate.

### 9.2. Process

1. Generate a new keypair.
2. Create an `identity.key_rotate` event signed by the **old** key.
3. The event includes the new public key.
4. The event is signed by the old key (proving control) and **MAY** also be signed by the new key (proving possession).
5. After finalization, the new key is the active key.

### 9.3. Event structure

```json
{
  "version": 1,
  "type": "identity.key_rotate",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "old_pubkey": "base58:...",
    "new_pubkey": "base58:...",
    "reason": "scheduled",
    "new_key_signature": "ed25519:..."
  },
  "signature": "ed25519:..."
}
```

### 9.4. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `old_pubkey` | string | MUST | Current public key. |
| `new_pubkey` | string | MUST | New public key. |
| `reason` | string | SHOULD | `scheduled`, `compromise`, `upgrade`, `hardware`. |
| `new_key_signature` | string | MAY | Signature by the new key over the event ID. |

### 9.5. Validation

- The event **MUST** be signed by the **old** key.
- The `old_pubkey` **MUST** match the current active key.
- The `new_pubkey` **MUST** be a valid Ed25519 public key.
- The `new_pubkey` **MUST NOT** already be in use by another identity.
- If `reason` is `compromise`, rotation **MUST** be immediate (no delay).
- If `reason` is `scheduled`, rotation **MUST** include a delay (e.g., 7 days) unless the event is signed by both keys.

### 9.6. Delay

Scheduled rotations **MAY** include a delay to allow detection of unauthorized rotation.

During the delay:

- The old key **MAY** cancel the rotation via `identity.cancel_rotate`.
- Both keys **MAY** sign events (during transition).
- After the delay, only the new key is active.

### 9.7. Historical events

Events signed by the old key **remain valid**. Signature verification uses the key that was active at the time of the event (`created_at`).

### 9.8. Rotation chain

An identity **MAY** rotate multiple times. The full chain is in the ledger:

```
key0 → key1 → key2 → key3 (current)
```

To verify a signature from any historical event, find the key active at that event's `created_at` by tracing the rotation chain.

### 9.9. Rotation and DID

The DID **does not change** on rotation.

Wait — this is a design decision. The DID is `did:cl:main:<base58-pubkey>`. If the key rotates, the DID would change.

Two options:

**Option A: DID changes on rotation.**

- DID stays tied to the key.
- Rotation creates a new DID linked by a `key_rotate` event.
- Historical events are linked via the rotation chain.

**Option B: DID stays, key rotates.**

- DID is decoupled from the key.
- The DID becomes a persistent identifier.
- The key is looked up via the ledger.

**Decision:** CL uses **Option A**. The DID is derived from the key. Rotation creates a new DID, linked to the old one by a `key_rotate` event.

**Rationale:** Option B requires a separate identifier registry, which adds complexity. Option A keeps DIDs simple and derivable.

**Consequence:** All references to the old DID must be updated. To make this easier:

- The `key_rotate` event links the old DID to the new DID.
- Reputation **MAY** be transferred from old DID to new DID (per community rules).
- Attestations **MAY** be re-issued for the new DID.

**Warning:** this is a significant decision. It affects how reputation, attestations, and references work. Communities **MUST** decide their policy.

### 9.10. Compromise handling

If a key is compromised:

1. The holder **MUST** rotate immediately.
2. A `reason: compromise` rotation is valid without delay.
3. Any events signed by the compromised key after the rotation **MUST** be rejected.
4. A community **MAY** vote to invalidate specific events signed by the compromised key.

---

## 10. Multiple Identities

A single person or organization **MAY** control multiple identities.

### 10.1. Legitimate uses

- **Separate contexts.** One DID for work, one for volunteering, one for personal projects.
- **Separation of concerns.** One DID for code, one for governance.
- **Testing.** A separate DID for experiments.
- **Organizations.** A person may control their own DID and act on behalf of an organization's DID.

### 10.2. Linking identities

Identities **MAY** be linked via a mutual attestation:

```json
{
  "type": "identity.link",
  "author": "did:cl:main:alice",
  "payload": {
    "other": "did:cl:main:alice-work",
    "claim": "same_controller"
  },
  "signature": "ed25519:..."
}
```

Both identities **MUST** sign a `identity.link` event referencing each other. This proves they are controlled by the same party.

Linking is **optional**. Many users prefer to keep identities separate.

### 10.3. Reputation across identities

By default, reputation is **per identity, per context**. It does not transfer between linked identities.

Communities **MAY** define rules for aggregating reputation across linked identities. For example:

- A context may count the sum of reputation across linked identities.
- A context may cap the contribution of linked identities to prevent gaming.

### 10.4. Sybil resistance

Multiple identities are allowed. But:

- Creating many identities to farm reputation is **Sybil behavior**.
- Communities **MAY** require attestations for participation.
- Reputation thresholds **MAY** be higher for unlinked identities.
- Graph analysis **MAY** detect suspicious patterns (many identities controlled by one party, all voting the same way).

### 10.5. No global identity

CL does **not** enforce a single global identity. There is no "one person, one vote" at the protocol level.

Each context defines its own rules. Some contexts may require verified identity. Others may allow pseudonymous participation.

---

## 11. Deactivation

An identity **MAY** be deactivated voluntarily or involuntarily.

### 11.1. Voluntary deactivation

```json
{
  "type": "identity.deactivate",
  "author": "did:cl:main:alice",
  "payload": {
    "reason": "user_request"
  },
  "signature": "ed25519:..."
}
```

Effects:

- The identity can no longer sign events.
- Historical events remain valid.
- Reputation remains attributed but frozen.
- Attestations remain unless revoked.

Reactivation **MAY** be possible via recovery (Section 8).

### 11.2. Involuntary deactivation

A community **MAY** vote to deactivate an identity in its context. This does not deactivate the identity globally — only within that community.

Effects within the community:

- The identity cannot participate.
- Its contributions may be revoked.
- Its votes may be discounted.

Rules for involuntary deactivation:

- **MUST** be defined in the community's rules.
- **MUST** require a qualified majority (e.g., 2/3).
- **MUST** include a reason.
- **MAY** be appealed.

### 11.3. Global deactivation

There is **no** global deactivation. No single entity can deactivate an identity across all communities.

This is intentional: decentralization means no central authority.

---

## 12. Validation Rules

Validators **MUST** enforce these rules for identity-related events.

### 12.1. General identity rules

- `author` **MUST** be a valid DID (Section 4).
- The event **MUST** be signed by the key encoded in `author`.
- If `author` has rotated keys, the signature **MUST** use the key active at `created_at`.
- If `author` is deactivated, events **MUST** be rejected (except recovery).

### 12.2. `identity.create` rules

- `did` **MUST** match `author`.
- `pubkey` **MUST** match the key in `did`.
- `did` **MUST NOT** already exist.
- `recovery_commitment` **MUST** be a valid BLAKE3 hash if present.

### 12.3. `identity.attest` rules

- `author` **MUST** be a Level 2+ identity.
- `author` **MUST** have the right to issue the claim (e.g., organizations only).
- `subject` **MUST** be a valid identity.
- `subject` **MUST NOT** equal `author`.
- `valid_until` **MUST** be in the future if present.
- The claim type **MUST** be known (or allowed by community rules).

### 12.4. `identity.revoke_attest` rules

- `author` **MUST** equal the author of the original attestation.
- `attestation_id` **MUST** reference an existing attestation.

### 12.5. `identity.recover` rules

- The event **MUST** be signed by a listed recovery contact.
- The contact **MUST** be in the commitment.
- Threshold **MUST** be met for completion.
- Delay **MUST** have passed (if applicable).
- The old key **MUST NOT** have been used to cancel the recovery.

### 12.6. `identity.key_rotate` rules

- The event **MUST** be signed by the old key.
- `old_pubkey` **MUST** match the current active key.
- `new_pubkey` **MUST** be valid and unused.
- If `reason` is `compromise`, rotation **MUST** be immediate.
- If `reason` is `scheduled`, delay **MUST** be observed (unless signed by both keys).

### 12.7. `identity.deactivate` rules

- The event **MUST** be signed by the identity being deactivated.
- The identity **MUST** be active.
- The reason **MUST** be present.

---

## 13. Examples

### 13.1. Full identity lifecycle

**Step 1: Create.**

```json
{
  "version": 1,
  "type": "identity.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": [],
  "payload": {
    "did": "did:cl:main:alice",
    "pubkey": "base58:7Xk9fQ...",
    "recovery_commitment": "blake3:abc...",
    "metadata": {"display_name": "Alice"}
  },
  "signature": "ed25519:..."
}
```

**Step 2: Attestation.**

```json
{
  "version": 1,
  "type": "identity.attest",
  "author": "did:cl:org:university",
  "created_at": 1730001000,
  "parents": ["blake3:abc..."],
  "payload": {
    "subject": "did:cl:main:alice",
    "claim": "student",
    "value": {"program": "Computer Science", "year": 2024},
    "valid_until": 1793000000
  },
  "signature": "ed25519:..."
}
```

**Step 3: Key rotation.**

```json
{
  "version": 1,
  "type": "identity.key_rotate",
  "author": "did:cl:main:alice",
  "created_at": 1731000000,
  "parents": ["blake3:def..."],
  "payload": {
    "old_pubkey": "base58:7Xk9fQ...",
    "new_pubkey": "base58:9zY8xW...",
    "reason": "scheduled",
    "new_key_signature": "ed25519:..."
  },
  "signature": "ed25519:..."
}
```

**Step 4: New DID.**

After rotation, the identity uses the new DID:

```
did:cl:main:9zY8xW7vU6tS5rQ4pN3mL2kJ1iH0gF9eD8cB7aZ6yX5w
```

The `key_rotate` event links the old and new DIDs.

### 13.2. Social recovery

Alice loses her key. Her recovery contacts are Bob, Carol, and Dave (threshold 2 of 3).

1. Alice informs Bob, Carol, and Dave out-of-band.
2. Bob creates `identity.recover` for Alice, proposing a new key.
3. Carol does the same.
4. Threshold (2 of 3) is met.
5. After the delay (7 days), the recovery is finalized.
6. Alice can now sign with the new key.

### 13.3. Malicious recovery attempt

An attacker steals Alice's backup key and tries to recover.

1. Attacker creates `identity.recover` with a new key.
2. Alice, still in possession of her primary key, sees the recovery attempt.
3. Alice creates `identity.cancel_recover`, signed by her primary key.
4. Recovery is cancelled. The attacker's new key is rejected.
5. Alice rotates to a new key to invalidate the compromised backup.

---

## 14. Test Vectors

Test vectors for identity live in `spec/test-vectors/identity.json`.

### 14.1. Coverage

- Key generation from a fixed seed.
- Base58 encoding/decoding.
- DID construction and parsing.
- `identity.create` with all fields.
- `identity.attest` for each claim type.
- `identity.revoke_attest`.
- `identity.recover` with threshold and delay.
- `identity.key_rotate` (scheduled and compromise).
- `identity.deactivate`.
- Invalid events: bad signature, wrong DID, duplicate creation.

### 14.2. Fixed test keys

```
seed_1: 0000000000000000000000000000000000000000000000000000000000000001
pub_1:  4cb5abf6ad79fbf5abbccafcc269d85cd2651ed4b885b5869f241aedf0a5ba29
did_1:  did:cl:test:<base58(pub_1)>

seed_2: 0000000000000000000000000000000000000000000000000000000000000002
pub_2:  <...>
did_2:  did:cl:test:<base58(pub_2)>
```

### 14.3. Verifying

Implementations **MUST** produce byte-identical results for these vectors.

---

## 15. Open Questions

- Should the DID change on key rotation, or stay fixed? (Current: changes.)
- How to handle reputation transfer on rotation across communities?
- Should there be a maximum number of linked identities?
- How to prevent Sybil attacks without requiring legal identity?
- Should recovery be mandatory for Level 2+ identities?
- How to handle multiple recovery configurations (e.g., different contacts for different contexts)?
- Should there be a "dead man's switch" for identities (automatic deactivation after inactivity)?
- How to handle identity in federated contexts (one identity across multiple ledgers)?
- Should attestations be transferable between contexts?
- How to handle identity disputes (e.g., someone claims to be someone else)?

These will be resolved through RFCs and community discussion.

---

## Summary

**Identity is:**

- A keypair (Ed25519).
- Represented by a DID: `did:cl:<network>:<base58-pubkey>`.
- Pseudonymous by default.
- Recoverable.
- Rotatable.
- Contextual for reputation.

**Levels:**

- 0 — Anonymous.
- 1 — Pseudonymous.
- 2 — Verified.
- 3 — Organizational.

**Attestations:**

- Signed claims about an identity.
- Issued by Level 2+ identities.
- Revocable by the issuer.
- Context-specific.

**Recovery:**

- Social (M-of-N contacts).
- Multisig (backup key).
- Time-locked (delay).

**Rotation:**

- Replaces the signing key.
- Creates a new DID.
- Links old and new via `key_rotate`.

**Validation:**

- Structural, signature, level, attestation, recovery, rotation rules.

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [contribution.md](./contribution.md) — contribution events.
- [reputation.md](./reputation.md) — reputation calculation.
- [consensus.md](./consensus.md) — validator rules.
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
