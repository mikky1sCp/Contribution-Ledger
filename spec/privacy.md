# Privacy

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md) · [identity.md](./identity.md) · [contribution.md](./contribution.md) · [reputation.md](./reputation.md) · [vote.md](./vote.md) · [ledger.md](./ledger.md) · [api.md](./api.md)  
**Related:** [consensus.md](./consensus.md) · [sync.md](./sync.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [Threat Model](#3-threat-model)
4. [Data Classification](#4-data-classification)
5. [Data Minimization](#5-data-minimization)
6. [Selective Disclosure](#6-selective-disclosure)
7. [Zero-Knowledge Proofs](#7-zero-knowledge-proofs)
8. [Private Contexts](#8-private-contexts)
9. [Anonymous Identities](#9-anonymous-identities)
10. [Metadata Privacy](#10-metadata-privacy)
11. [Encrypted Evidence](#11-encrypted-evidence)
12. [Right to Be Forgotten](#12-right-to-be-forgotten)
13. [Cross-Context Privacy](#13-cross-context-privacy)
14. [GDPR and Legal Compliance](#14-gdpr-and-legal-compliance)
15. [Threats and Defenses](#15-threats-and-defenses)
16. [Validation Rules](#16-validation-rules)
17. [Examples](#17-examples)
18. [Test Vectors](#18-test-vectors)
19. [Open Questions](#19-open-questions)

---

## 1. Overview

**Privacy** in CL is not about hiding everything. It is about **controlling what is revealed, to whom, and when**.

CL is a public ledger. By default, all events are visible to all nodes. But this does not mean all data must be public:

- **identities** can be pseudonymous;
- **evidence** can be encrypted;
- **reputation** can be proven without revealing contributions;
- **votes** can be secret;
- **contexts** can be private;
- **metadata** can be minimized.

**This file defines:**

- The threat model (Section 3).
- What data is public, private, or sensitive (Section 4).
- How data is minimized (Section 5).
- Selective disclosure (Section 6).
- Zero-knowledge proofs (Section 7).
- Private contexts (Section 8).
- Anonymous identities (Section 9).
- Metadata privacy (Section 10).
- Encrypted evidence (Section 11).
- Right to be forgotten (Section 12).
- Cross-context privacy (Section 13).
- GDPR and legal compliance (Section 14).
- Threats and defenses (Section 15).
- Validation rules (Section 16).

Privacy is not a feature added later. It is a design constraint from the start.

---

## 2. Design Principles

### 2.1. Pseudonymity by default

Identities are keys, not names. Real-world identity is optional, added via attestations.

### 2.2. Data minimization

CL stores the minimum necessary:

- no names, emails, passports;
- no biometrics;
- no private messages;
- no IP addresses (unless required for sync).

### 2.3. Selective disclosure

A user can prove statements about themselves without revealing everything:

- "I have reputation > 1000 in context X."
- "I am a member of organization Y."
- "I voted in this election."

### 2.4. Opt-in transparency

Public by default, but users can choose:

- encrypted evidence;
- private contexts;
- anonymous participation.

### 2.5. No global identity

There is no "one person, one DID" requirement. Users may have multiple DIDs, unlinked.

### 2.6. Right to exit

Users can leave a context, revoke attestations, and start fresh.

### 2.7. Privacy is not anonymity

CL does not promise full anonymity. It promises **control**. Users choose what to reveal.

### 2.8. Forward secrecy

Where encryption is used, it supports forward secrecy:

- compromised keys do not reveal past messages;
- key rotation limits exposure.

### 2.9. Metadata matters

Even without content, metadata leaks information:

- who talks to whom;
- when;
- how often.

CL minimizes metadata where possible and allows privacy modes.

### 2.10. Compliance without surveillance

CL can support legal compliance (e.g., GDPR) without building surveillance into the protocol.

---

## 3. Threat Model

### 3.1. Adversaries

| Adversary | Capability |
|---|---|
| **Passive observer** | Reads the public ledger. |
| **Network observer** | Sees traffic between peers. |
| **Malicious peer** | Connects to nodes, sends/receives messages. |
| **Malicious validator** | Signs checkpoints, can censor. |
| **Malicious issuer** | Posts tasks, controls escrow. |
| **Malicious verifier** | Approves or rejects contributions. |
| **State actor** | Subpoenas nodes, monitors network. |
| **Insider** | Has access to a node's storage. |

### 3.2. What we protect against

- **Linkability.** Linking multiple DIDs to one person.
- **Content leakage.** Revealing private data (names, messages).
- **Metadata leakage.** Revealing who talks to whom.
- **Censorship.** Preventing participation.
- **Coercion.** Forcing a user to reveal a vote.

### 3.3. What we do not protect against

- **Full anonymity.** CL is not Tor, not Monero. It does not hide network traffic by default.
- **Quantum adversaries.** Current crypto is not quantum-resistant.
- **Physical coercion.** If someone forces you to reveal your key, the protocol cannot help.
- **Global adversaries.** A state actor with total network control can see everything on the public ledger.

### 3.4. Trust assumptions

- Users control their private keys.
- Cryptographic primitives (Ed25519, BLAKE3, etc.) are secure.
- Validators do not collude to de-anonymize.
- Nodes do not log more than required.

### 3.5. Out of scope

- Protecting against a user voluntarily publishing their identity.
- Protecting against a user leaking their own data.
- Protecting against bugs in client software.

---

## 4. Data Classification

### 4.1. Categories

| Category | Examples | Storage | Visibility |
|---|---|---|---|
| **Public** | Event IDs, signatures, DIDs, timestamps | On-ledger | Everyone |
| **Pseudonymous** | Contribution records, reputation | On-ledger | Everyone (linked to DID) |
| **Sensitive** | Evidence (hashes), attestation claims | On-ledger (hashes) | Everyone (opaque) |
| **Private** | Names, emails, biometrics | Off-ledger | Only authorized |
| **Ephemeral** | Session tokens, IP addresses | Off-ledger | Only node |

### 4.2. What is always on-ledger

- Event ID.
- Event type.
- Author DID.
- Timestamp.
- Parents.
- Signature.
- Payload (structure).

### 4.3. What may be on-ledger (opaque)

- Evidence hashes (not the evidence itself).
- Attestation claims (e.g., "verified_human", not the passport).
- Reputation values.
- Vote commitments (not the vote).

### 4.4. What is never on-ledger

- Names.
- Emails.
- Phone numbers.
- Passports.
- Biometrics.
- Private messages.
- IP addresses.
- Bank details.
- Medical data.
- Passwords.

### 4.5. What is optionally on-ledger

- Display names (metadata field).
- Links to external profiles.
- Evidence links (if not encrypted).

### 4.6. Off-ledger storage

Private data **MAY** be stored:

- on the user's device;
- in encrypted cloud storage;
- in the context's private storage;
- in external services (with user consent).

Off-ledger storage is not controlled by the protocol. It is the user's responsibility.

---

## 5. Data Minimization

### 5.1. Principle

Store only what is necessary for the protocol to function.

### 5.2. Event payload minimization

- No personal data in `payload`.
- No free-form text with PII.
- Use `metadata` sparingly.
- Prefer hashes over inline data.

### 5.3. Evidence minimization

- Store evidence hashes, not evidence.
- If evidence must be public, warn users.
- Allow encrypted evidence.

### 5.4. Metadata minimization

- Display names are optional.
- Links to external profiles are optional.
- Avatar URLs are optional.

### 5.5. Attestation minimization

- Attest only the claim, not the underlying data.
- Example: "verified_human" not "passport number 12345".
- Proof of claim **MAY** be stored off-ledger.

### 5.6. Reputation minimization

- Reputation values are public (needed for consensus).
- The contributions that produce reputation are public.
- Users who want privacy can use anonymous DIDs.

### 5.7. Log minimization

Nodes **SHOULD** minimize logs:

- no full event payloads in logs;
- no IP addresses in long-term logs;
- log rotation;
- deletion after retention period.

### 5.8. Analytics minimization

Nodes **MUST NOT** collect analytics beyond what is needed for operation.

### 5.9. Telemetry opt-in

If a node sends telemetry to developers:

- it **MUST** be opt-in;
- it **MUST NOT** include PII;
- it **MUST** be documented.

### 5.10. No tracking

CL **MUST NOT** include tracking pixels, cookies, or fingerprinting.

---

## 6. Selective Disclosure

### 6.1. Purpose

A user can prove a statement without revealing the full data behind it.

### 6.2. Example statements

- "I have reputation > 100 in context X."
- "I am a member of organization Y."
- "I have completed at least 10 bounties."
- "I voted in this election."
- "I have not been banned in context Z."

### 6.3. How it works

Selective disclosure uses **zero-knowledge proofs** (Section 7):

1. The user constructs a proof of the statement.
2. The proof is verifiable against public data (or a commitment).
3. The verifier learns only that the statement is true.

### 6.4. Use cases

| Use case | Disclosure |
|---|---|
| Job application | "reputation > 500" |
| Grant application | "10+ contributions in context X" |
| Voting eligibility | "member of community Y" |
| Access control | "not banned in context Z" |
| Anonymous bounty claim | "reputation > threshold" without revealing DID |

### 6.5. Selective disclosure event

```json
{
  "type": "identity.disclose",
  "author": "did:cl:main:alice",
  "payload": {
    "statement": "reputation_above",
    "context": "repo:x/y",
    "threshold": 500,
    "proof": "zkp:...",
    "verifier": "did:cl:org:employer"
  }
}
```

### 6.6. Verification

The verifier checks the proof against the public state:

- reputation root (from checkpoint);
- proof of membership in the Merkle tree;
- ZK proof of the statement.

### 6.7. Ephemeral proofs

Selective disclosure proofs **MAY** be ephemeral:

- not stored on-ledger;
- used only for a specific verification;
- discarded after.

### 6.8. Persistent proofs

Some proofs **MAY** be stored on-ledger (e.g., for compliance):

- hash of the proof;
- statement;
- verifier.

The proof itself is stored off-ledger or only its hash.

### 6.9. Non-transferability

Selective disclosure proofs **MUST NOT** be transferable:

- they are bound to the user's DID;
- they cannot be replayed by another user;
- they include a nonce to prevent replay.

### 6.10. Revocation

If the underlying state changes (e.g., reputation drops), the proof becomes invalid.

Verifiers **MUST** check the proof against the current state (or a recent checkpoint).

---

## 7. Zero-Knowledge Proofs

### 7.1. Purpose

ZK proofs allow proving a statement without revealing the underlying data.

### 7.2. Types of proofs used in CL

| Proof | Purpose |
|---|---|
| **Reputation proof** | Prove reputation ≥ threshold without revealing exact value. |
| **Membership proof** | Prove membership in a set (e.g., context members). |
| **Vote proof** | Prove a valid vote without revealing the choice. |
| **Nullifier proof** | Prove uniqueness (e.g., "I haven't voted twice"). |
| **Range proof** | Prove a value is within a range. |
| **Set membership** | Prove a DID is in an allowed set. |

### 7.3. Cryptographic primitives

| Primitive | Use |
|---|---|
| **Pedersen commitments** | Hiding values (votes, reputation). |
| **Bulletproofs** | Range proofs, efficient. |
| **zk-SNARKs** | Succinct proofs, requires trusted setup (or transparent). |
| **zk-STARKs** | Transparent setup, larger proofs. |
| **PLONK** | Universal SNARK, transparent setup. |
| **Halo2** | Recursive proofs, no trusted setup. |

CL **MAY** use any of these. Implementations **MUST** agree on the variant.

### 7.4. Recommended stack

For a first implementation:

- **Pedersen commitments** for votes.
- **Bulletproofs** for range proofs.
- **PLONK** or **Halo2** for general statements.

### 7.5. Reputation proof

**Statement:** "Alice's reputation in context X is ≥ 100."

**Public:**
- reputation Merkle root (from checkpoint);
- threshold (100);
- context.

**Private:**
- Alice's reputation value;
- Alice's DID;
- Merkle path.

**Proof:**
- Alice's DID is in the tree.
- The value at that leaf is ≥ 100.
- The Merkle path is valid.

**Verify:** verifier checks the proof against the root.

### 7.6. Vote proof

**Statement:** "Alice cast a valid vote in election X."

**Public:**
- election ID;
- options;
- commitment to Alice's vote.

**Private:**
- the option Alice chose;
- randomness.

**Proof:**
- the commitment is valid;
- the option is one of the allowed options;
- Alice is eligible;
- Alice has not voted twice (nullifier).

**Verify:** verifier checks the proof. The option remains hidden.

### 7.7. Nullifier

A **nullifier** is a unique value derived from the voter's secret and the election ID.

- It is published with the vote.
- It is used to detect double voting.
- It cannot be linked to the voter's DID.

```
nullifier = BLAKE3(voter_secret || election_id)
```

The voter proves (in ZK) that:

- they know the secret;
- the nullifier is correct;
- they have not revealed the secret before.

### 7.8. Membership proof

**Statement:** "Alice is a member of context X."

**Public:**
- context X;
- membership root.

**Private:**
- Alice's DID;
- membership path.

**Proof:** Alice's DID is in the tree.

### 7.9. Set membership

**Statement:** "Alice's DID is in the allowed set."

**Public:**
- set commitment.

**Private:**
- Alice's DID;
- membership path.

**Proof:** Alice's DID is in the set.

### 7.10. Performance

ZK proofs are computationally expensive:

| Proof | Generate | Verify | Size |
|---|---|---|---|
| Pedersen commit | μs | μs | 32 bytes |
| Bulletproof range | ms | ms | ~700 bytes |
| PLONK | 100 ms – 1 s | ms | ~1 KB |
| Halo2 | 1–10 s | ms | ~1 KB |
| zk-STARK | 1–10 s | ms | ~100 KB |

Nodes **SHOULD** cache proofs where possible.

### 7.11. Trusted setup

Some ZK systems (zk-SNARKs) require a trusted setup:

- a ceremony generates public parameters;
- if the ceremony is compromised, proofs can be forged.

CL **RECOMMENDS** transparent systems (PLONK, Halo2, zk-STARK) to avoid this risk.

### 7.12. Quantum resistance

ZK systems based on elliptic curves are not quantum-resistant.

Future versions **MAY** add post-quantum ZK (e.g., zk-STARKs with hash-based commitments).

### 7.13. Implementation

ZK proofs **MUST** be:

- deterministic (for reproducibility in test vectors);
- verifiable by any node;
- bound to the context (no cross-context replay).

### 7.14. Fallback

If ZK proofs are not feasible (bugs, performance), contexts **MAY** fall back to public voting or other mechanisms.

### 7.15. No home-grown crypto

Implementations **MUST** use audited libraries:

- `arkworks` (Rust);
- `bellman` (Rust);
- `circom` + `snarkjs` (JS);
- `libsnark` (C++).

Never implement ZK primitives from scratch.

---

## 8. Private Contexts

### 8.1. Purpose

Some communities require privacy:

- closed organizations;
- confidential projects;
- sensitive discussions.

Private contexts restrict visibility of events.

### 8.2. Definition

A **private context** is a context where:

- events are encrypted;
- access is gated by membership;
- non-members cannot read.

### 8.3. Encryption model

Events in a private context are encrypted with a **context key**:

```
context_key = symmetric key shared among members
encrypted_event = AEAD(context_key, event_payload)
```

The event envelope (ID, author, timestamp) remains public. Only the payload is encrypted.

### 8.4. Key distribution

The context key is distributed to members via:

- invite (encrypted with the invitee's public key);
- key rotation (new key on membership change).

### 8.5. Membership

Membership is proven via:

- an attestation ("member of private context X");
- a token (e.g., a secret);
- a ZK proof (member without revealing identity).

### 8.6. Read access

Only members can decrypt events.

Non-members see:

- event IDs;
- author DIDs;
- timestamps;
- parents;
- signatures.

They cannot see the payload.

### 8.7. Write access

Only members can create events in the private context.

Non-members attempting to create events are rejected.

### 8.8. Reputation in private contexts

Reputation in a private context is:

- stored encrypted;
- visible only to members;
- provable via ZK proofs (e.g., "reputation > 100" without revealing the value).

### 8.9. Checkpoints for private contexts

Checkpoints **MUST NOT** include private context state in plaintext.

Options:

- omit private contexts from public checkpoints;
- include encrypted state (only members can decrypt);
- use ZK proofs for public verification.

### 8.10. Federation

Private contexts **MUST NOT** be federated with public contexts unless explicitly agreed.

### 8.11. Exit

A member leaving a private context:

- loses access to future events;
- retains access to past events (already decrypted);
- cannot prevent others from accessing past events.

### 8.12. Key rotation

On membership change:

- the context key is rotated;
- new key distributed to current members;
- past events remain encrypted with old key (members who left retain access to past).

### 8.13. Compliance

Private contexts **MUST** comply with applicable laws:

- no illegal content;
- no unlicensed financial activity;
- no evasion of legal obligations.

The protocol does not enforce compliance. Communities are responsible.

### 8.14. Discovery

Private contexts **MAY** be:

- listed publicly (name, description, membership rules);
- hidden (only reachable via invite).

Default: hidden.

### 8.15. Private context event types

| Event | Purpose |
|---|---|
| `context.create_private` | Create a private context. |
| `context.invite` | Invite a member. |
| `context.remove_member` | Remove a member. |
| `context.rotate_key` | Rotate the context key. |

### 8.16. Event structure

```json
{
  "type": "context.create_private",
  "author": "did:cl:main:founder",
  "payload": {
    "id": "private:myproject",
    "name": "My Project",
    "encrypted_rules": "base64:...",
    "public_metadata": {
      "description": "A private project."
    }
  }
}
```

`encrypted_rules` contains the context rules encrypted with the context key.

### 8.17. Verification

Non-members **MUST NOT** be able to:

- decrypt events;
- forge valid events;
- prove membership without a valid proof.

### 8.18. Limitations

Private contexts are **not fully anonymous**:

- event IDs, authors, timestamps are public;
- traffic analysis can reveal patterns;
- validators can see events (but not decrypt).

Users who need full anonymity **SHOULD** use anonymous DIDs (Section 9).

---

## 9. Anonymous Identities

### 9.1. Purpose

For maximum privacy, users can use anonymous DIDs.

### 9.2. Definition

An **anonymous DID** is a DID that:

- is not linked to any real-world identity;
- has no attestations;
- is used only in specific contexts.

### 9.3. Level 0

Anonymous DIDs are Level 0 (see [identity.md](./identity.md#62-level-0--anonymous)).

Limits:

- cannot vote (unless context allows);
- cannot confirm contributions;
- cannot claim bounties;
- cannot be validators.

### 9.4. Use cases

- Reading without identity.
- Small contributions in open contexts.
- Testing.
- Whistleblowing (in contexts that allow it).

### 9.5. Not fully anonymous

Even anonymous DIDs leak:

- network traffic (who connects from where);
- timing (when events are submitted);
- patterns (how the DID behaves).

For stronger anonymity, use:

- Tor/I2P (see [sync.md](./sync.md#16-privacy-considerations));
- mix networks;
- zero-knowledge proofs.

### 9.6. Unlinking

If a user has multiple DIDs:

- they **MUST NOT** link them unless they choose to;
- attestations **MUST NOT** be shared between unlinked DIDs;
- reputation **MUST NOT** transfer automatically.

### 9.7. Sybil resistance

Anonymous DIDs have limited rights, which prevents:

- vote farming;
- reputation farming;
- bounty farming.

### 9.8. Attestation without identity

Users **MAY** obtain attestations without revealing real identity:

- "verified_human" via ZK proof of personhood;
- "member of organization" via anonymous credential.

These attestations are bound to the DID but do not reveal who the user is.

### 9.9. Revocation

Anonymous DIDs can be revoked only by:

- the user (deactivation);
- the context (ban).

The user cannot be compelled to reveal their real identity.

### 9.10. Exit

Users can abandon an anonymous DID and start fresh:

- history remains in the ledger (attributed to the old DID);
- reputation is lost;
- new DID starts at zero.

---

## 10. Metadata Privacy

### 10.1. What is metadata

Metadata is data about data:

- who sent a message;
- when;
- to whom;
- how often.

### 10.2. Metadata on-ledger

On-ledger metadata includes:

- author DIDs;
- timestamps;
- parents;
- event types;
- contexts.

This metadata is public. It cannot be hidden without breaking the protocol.

### 10.3. Metadata off-ledger

Off-ledger metadata includes:

- IP addresses;
- connection patterns;
- subscription topics.

This metadata **MAY** be hidden via privacy modes.

### 10.4. Network privacy modes

| Mode | Description |
|---|---|
| **Clearnet** | Default; IP visible to peers. |
| **Tor** | Traffic routed through Tor; IP hidden. |
| **I2P** | Routed through I2P. |
| **Relay** | Via trusted relay. |
| **Mixnet** | High-latency, strong anonymity. |

### 10.5. Tor support

Nodes **MAY** support Tor:

- `.onion` addresses;
- Tor transport;
- no IP logging.

### 10.6. Relay mode

Nodes **MAY** support relay mode:

- events forwarded without revealing the sender;
- relay does not store events;
- relay may be paid (optional).

### 10.7. Dummy traffic

Clients **MAY** send dummy requests to obscure real interests.

### 10.8. Blinded subscriptions

Clients **MAY** subscribe to filters without revealing the filter:

- Bloom filters;
- prefix filters;
- multiple filters combined.

### 10.9. Timing obfuscation

Clients **MAY** delay event submission to obscure timing patterns.

Trade-off: latency vs. privacy.

### 10.10. Metadata minimization

Nodes **SHOULD** minimize metadata:

- no IP logging by default;
- short log retention;
- no cross-session tracking.

### 10.11. Peer privacy

Peers **MUST NOT** be required to reveal their identity.

Peer IDs are random public keys.

### 10.12. Validator visibility

Validators **MUST** be public (see [consensus.md](./consensus.md#49-validator-visibility)).

This is a trade-off: validator accountability vs. privacy.

### 10.13. Legal disclosure

Nodes **MAY** be required by law to disclose metadata.

The protocol does not prevent this, but it minimizes what is collected.

---

## 11. Encrypted Evidence

### 11.1. Purpose

Evidence may contain sensitive data:

- medical records;
- financial documents;
- personal communications.

Encrypting evidence protects it from unauthorized readers.

### 11.2. Encryption model

Evidence **MAY** be:

- **plaintext** (public);
- **encrypted** (visible only to authorized readers);
- **hashed** (only the hash is public).

### 11.3. Encrypted evidence event

```json
{
  "type": "contribution.create",
  "payload": {
    "subject": "did:cl:main:alice",
    "action": "medical_data_analysis",
    "context": "health:research",
    "weight_class": "analysis",
    "evidence": [
      {
        "type": "encrypted_link",
        "value": "ipfs://Qm...",
        "encryption": "x25519-chacha20poly1305",
        "recipients": ["did:cl:org:reviewer1", "did:cl:org:reviewer2"]
      }
    ]
  }
}
```

### 11.4. Recipients

Evidence can be encrypted for:

- specific verifiers;
- the context's members;
- the verifier role;
- the subject themselves.

### 11.5. Decryption

Authorized readers decrypt using:

- their private key;
- a shared context key;
- a threshold key (M of N).

### 11.6. Verification

Verifiers decrypt the evidence to check it.

If a verifier cannot decrypt, they **MUST NOT** approve the contribution.

### 11.7. Hashing

Even if evidence is encrypted, its hash is public:

```
evidence_hash = BLAKE3(plaintext_evidence)
```

The hash allows:

- proving the evidence has not changed;
- verifying the evidence matches the claim.

### 11.8. Partial disclosure

Evidence **MAY** be partially disclosed:

- some fields public;
- some encrypted;
- some hashed only.

### 11.9. Zero-knowledge evidence

For maximum privacy, evidence can be verified via ZK proofs:

- the verifier learns that the evidence meets the criteria;
- without seeing the evidence.

Example: "blood test shows X" without revealing the test results.

### 11.10. Retention

Encrypted evidence **MUST** be:

- stored encrypted;
- decryptable only by authorized parties;
- deletable by the subject (if applicable).

### 11.11. GDPR compliance

Encrypted evidence supports GDPR:

- right of access (decrypt and share);
- right to erasure (delete key);
- data minimization (only necessary fields).

### 11.12. Forward secrecy

Evidence encryption **SHOULD** use:

- ephemeral keys;
- ratcheting;
- forward secrecy.

### 11.13. Backup

Evidence **MAY** be backed up:

- encrypted backups;
- key escrow (with user consent);
- no plaintext backups.

### 11.14. Loss

If the decryption key is lost:

- the evidence cannot be decrypted;
- verification is impossible;
- the contribution may be invalidated.

Users **MUST** back up keys or use key recovery.

---

## 12. Right to Be Forgotten

### 12.1. The problem

CL is append-only. Events cannot be deleted. This conflicts with GDPR's right to erasure.

### 12.2. What can be deleted

- **Off-ledger data**: names, emails, evidence, private keys.
- **Links**: evidence links can be revoked.
- **Attestations**: can be revoked.
- **DIDs**: can be deactivated.

### 12.3. What cannot be deleted

- Event IDs.
- Event structure (type, author, timestamp).
- Signatures.
- Parents.
- Hashes.

### 12.4. Strategy

The protocol minimizes on-ledger personal data. What remains is:

- pseudonymous (DIDs);
- non-personal (hashes, signatures);
- required for consensus.

### 12.5. Right to erasure

Users can request erasure of:

- off-ledger data (evidence, profiles);
- attestations about them;
- their DID (deactivation).

They cannot delete:

- their contribution history (needed for consensus);
- their reputation history.

### 12.6. Anonymization

Users can anonymize:

- by using an anonymous DID;
- by not linking DIDs;
- by not attaching personal data.

### 12.7. Compliance claims

CL **does not claim** full GDPR compliance. It claims **data minimization** and **pseudonymity**.

Communities that operate in GDPR jurisdictions **MUST**:

- obtain consent for data collection;
- provide privacy notices;
- honor erasure requests for off-ledger data;
- document their data processing.

### 12.8. Data subject requests

For on-ledger data, the response is:

- the data is pseudonymous;
- the data is necessary for consensus;
- deletion would break the ledger.

This is a legitimate interest argument under GDPR.

### 12.9. Revocation of links

Evidence links **MAY** be revoked:

```json
{
  "type": "contribution.revoke_evidence",
  "payload": {
    "contribution_id": "blake3:...",
    "evidence_index": 0
  }
}
```

The link is marked as revoked. The hash remains (for verification of what was there).

### 12.10. Context-level erasure

If an entire context is deleted (rare):

- events remain on-ledger;
- but the context is marked inactive;
- no new events are accepted.

### 12.11. Fork-based erasure

A community **MAY** fork to remove data:

- fork the ledger;
- exclude problematic events in the new ledger;
- old ledger remains as a historical artifact.

### 12.12. Legal basis

For GDPR, the legal basis for on-ledger data is:

- **legitimate interest** (running the protocol);
- **consent** (for optional data).

Users **MUST** be informed of what is on-ledger.

---

## 13. Cross-Context Privacy

### 13.1. The problem

A user in multiple contexts may want to prevent:

- linking their identities across contexts;
- leaking reputation across contexts;
- unintended cross-context visibility.

### 13.2. Default behavior

Contexts are isolated. Reputation does not transfer automatically.

### 13.3. Explicit recognition

If context A recognizes context B, then:

- reputation from B counts in A;
- the link is public (in A's rules);
- users **MUST** be informed.

### 13.4. Anonymous cross-context

Users **MAY** participate in different contexts with different DIDs:

- no link between DIDs;
- no reputation transfer;
- full isolation.

### 13.5. Linked cross-context

Users **MAY** link DIDs:

- via `identity.link` events;
- with attestations;
- for convenience.

Linking is optional. Once linked, it is public.

### 13.6. Selective linking

Users **MAY** link DIDs for specific purposes:

- link A and B for context X;
- keep them separate elsewhere.

### 13.7. Unlinking

Linking **MUST NOT** be reversible on-ledger.

To unlink, users **MUST** start fresh:

- new DIDs;
- no transfer of reputation.

### 13.8. Privacy considerations

Before linking, users **MUST** consider:

- all future events in linked DIDs are correlated;
- attestations leak;
- behavior patterns leak.

### 13.9. Cross-context attestations

Attestations from context A **MAY** be valid in context B, if B recognizes them.

Users **MAY** choose which attestations to disclose.

### 13.10. Cross-context proofs

ZK proofs allow:

- proving reputation from context A without revealing context A;
- proving membership without revealing which context.

Example: "reputation > 100 in some recognized context" without naming it.

### 13.11. Recommended practice

For most users:

- use one DID per context;
- link DIDs only when necessary;
- document the implications.

---

## 14. GDPR and Legal Compliance

### 14.1. Overview

CL is designed to be **compatible** with GDPR, but full compliance depends on:

- how communities operate;
- what data is stored off-ledger;
- what legal basis is claimed.

### 14.2. Roles

Under GDPR:

- **Data controller**: the community or node operator.
- **Data processor**: the node operator (if separate).
- **Data subject**: the user.

CL **does not** act as a data controller. Communities do.

### 14.3. Data minimization

CL stores minimal personal data:

- no names, emails, passports;
- only DIDs, contributions, attestations.

### 14.4. Lawful basis

For on-ledger data:

- **legitimate interest**: running the protocol;
- **consent**: for optional data.

For off-ledger data:

- **consent**: explicit.

### 14.5. Rights

| Right | How CL handles it |
|---|---|
| Access | Users can export their data. |
| Rectification | Users can add new events (corrections). |
| Erasure | Off-ledger data can be deleted; on-ledger is pseudonymous. |
| Portability | Data can be exported in standard formats. |
| Objection | Users can leave contexts. |
| Automated decisions | Reputation is algorithmic; users can dispute. |

### 14.6. Pseudonymization

DIDs are pseudonymous identifiers. They are:

- unique per user;
- not directly identifiable;
- linkable to personal data only by the user.

### 14.7. Data protection impact assessment

Communities operating in GDPR jurisdictions **SHOULD** conduct a DPIA.

### 14.8. Cross-border transfers

On-ledger data is global. Users **MUST** be informed that their pseudonymous data will be accessible globally.

### 14.9. Children

CL is not intended for children under 16 (or the applicable age in the jurisdiction).

Communities **MUST** enforce age requirements.

### 14.10. Data breaches

If a node is breached:

- off-ledger data may leak;
- on-ledger data is already public;
- affected users **MUST** be notified.

### 14.11. Compliance is local

GDPR applies only to users in the EU. Other jurisdictions have other rules.

Communities **MUST** comply with local laws.

### 14.12. No legal advice

This section is **not** legal advice. Communities **MUST** consult lawyers.

---

## 15. Threats and Defenses

### 15.1. De-anonymization

**Threat:** Linking a DID to a real identity.

**Defense:**

- pseudonymous DIDs;
- no mandatory identity disclosure;
- anonymous DIDs for sensitive use;
- ZK proofs of claims.

### 15.2. Correlation attacks

**Threat:** Linking multiple DIDs to one user.

**Defense:**

- separate DIDs per context;
- no automatic linking;
- no cross-context reputation transfer by default.

### 15.3. Metadata leakage

**Threat:** Inferring information from metadata.

**Defense:**

- minimal metadata on-ledger;
- privacy modes (Tor, relays);
- dummy traffic.

### 15.4. Timing attacks

**Threat:** Inferring information from timing.

**Defense:**

- timing obfuscation (delays);
- mix networks;
- batching.

### 15.5. Censorship

**Threat:** A validator censors a user's events.

**Defense:**

- multiple validators;
- federation;
- fork.

### 15.6. Coercion

**Threat:** Forcing a user to reveal their vote.

**Defense:**

- secret voting (ZK);
- plausible deniability (multiple votes with nullifiers).

### 15.7. State surveillance

**Threat:** A state actor compels nodes to reveal data.

**Defense:**

- data minimization;
- no IP logging;
- encryption;
- jurisdiction diversity.

### 15.8. Quantum attacks

**Threat:** Quantum computers break Ed25519.

**Defense:**

- future migration to post-quantum crypto;
- hybrid signatures (Ed25519 + PQ).

### 15.9. Sybil attacks

**Threat:** Many fake identities manipulate reputation.

**Defense:**

- attestations;
- reputation thresholds;
- quadratic voting;
- graph analysis.

### 15.10. Data exfiltration

**Threat:** A malicious node exfiltrates data.

**Defense:**

- no central storage;
- minimal on-ledger data;
- off-ledger data encrypted.

### 15.11. Replay attacks

**Threat:** Replaying a signed event or proof.

**Defense:**

- nonces in proofs;
- event IDs include content (unique);
- binding to context.

### 15.12. Side channels

**Threat:** Inferring secrets from timing, power, etc.

**Defense:**

- constant-time crypto libraries;
- hardware security modules (HSMs) for validators;
- no side-channel-prone implementations.

### 15.13. Social engineering

**Threat:** Tricking users into revealing keys.

**Defense:**

- user education;
- hardware wallets;
- multi-factor auth.

### 15.14. Legal attacks

**Threat:** Subpoenas, gag orders.

**Defense:**

- data minimization;
- jurisdiction diversity;
- transparency reports.

### 15.15. Insider threats

**Threat:** A node operator misuses data.

**Defense:**

- no access to user keys;
- minimal off-ledger data;
- audit logs.

---

## 16. Validation Rules

Nodes **MUST** enforce these rules for privacy-related operations.

### 16.1. Data minimization

- Events **MUST NOT** include PII in `payload` (best-effort; not enforceable).
- Evidence **SHOULD** be hashed or encrypted.

### 16.2. Selective disclosure

- ZK proofs **MUST** verify against the stated public data.
- Proofs **MUST NOT** be replayable.
- Proofs **MUST** be bound to the context.

### 16.3. ZK proofs

- **MUST** use audited libraries.
- **MUST** be deterministic.
- **MUST** be verifiable by any node.

### 16.4. Private contexts

- Events in private contexts **MUST** be encrypted.
- Non-members **MUST NOT** be able to decrypt.
- Membership **MUST** be verifiable.

### 16.5. Anonymous DIDs

- Anonymous DIDs **MUST** be Level 0.
- They **MUST NOT** have attestations.
- They **MUST NOT** vote or claim bounties.

### 16.6. Metadata

- Nodes **SHOULD** minimize logging.
- IP addresses **MUST NOT** be logged by default.
- Logs **MUST** be rotated and deleted after retention.

### 16.7. Evidence

- Encrypted evidence **MUST** be decryptable by authorized verifiers.
- Hashes **MUST** match.
- Revoked evidence links **MUST** be marked as revoked.

### 16.8. Right to erasure

- Off-ledger data **MUST** be deletable.
- On-ledger data **MUST** be pseudonymous.
- Users **MUST** be informed of what is on-ledger.

### 16.9. Cross-context

- Reputation **MUST NOT** transfer automatically.
- Recognition **MUST** be explicit.
- Linked DIDs **MUST** be documented.

### 16.10. GDPR

- Communities in GDPR jurisdictions **MUST** comply.
- Data protection notices **MUST** be provided.
- DPIAs **SHOULD** be conducted.

### 16.11. Security

- Private keys **MUST NOT** be transmitted or stored by nodes.
- Side-channel resistance **SHOULD** be implemented.
- Constant-time libraries **SHOULD** be used.

### 16.12. No silent tracking

- Nodes **MUST NOT** track users beyond what is required for operation.
- Tracking **MUST** be documented and opt-in.

---

## 17. Examples

### 17.1. Selective disclosure of reputation

**Alice wants to prove to an employer:** "reputation ≥ 500 in context repo:x/y."

**Step 1:** Alice fetches the latest checkpoint's reputation root.

**Step 2:** Alice constructs a ZK proof:

- her DID is in the tree;
- her reputation value is ≥ 500;
- the Merkle path is valid.

**Step 3:** Alice sends the proof to the employer.

**Step 4:** Employer verifies against the checkpoint root.

**Result:** Employer learns "reputation ≥ 500" without learning the exact value or her other contributions.

### 17.2. Secret vote

**Step 1:** Alice commits: `commitment = PedersenCommit("yes", r1)`.

**Step 2:** Alice publishes the commitment + ZK proof.

**Step 3:** Other voters do the same.

**Step 4:** Homomorphic sum of commitments = commitment of sum.

**Step 5:** After deadline, decryption parties reveal shares.

**Step 6:** Sum decrypted: {yes: 150.5, no: 50.0}.

**Result:** Nobody knows how Alice voted.

### 17.3. Private context

**Step 1:** Founder creates `private:myproject`.

**Step 2:** Founder invites Alice, Bob, Carol.

**Step 3:** Each invite is encrypted with the invitee's public key.

**Step 4:** Members publish encrypted events.

**Step 5:** Non-members see event IDs, authors, timestamps, but not payloads.

**Step 6:** Members decrypt and read.

### 17.4. Anonymous DID

**Alice wants to contribute to an open-source project without linking to her main identity.**

**Step 1:** Alice generates a new keypair.

**Step 2:** Alice creates `identity.create` with no metadata.

**Step 3:** Alice contributes.

**Result:** Contributions are attributed to the anonymous DID. Alice's main identity is not linked.

### 17.5. Encrypted evidence

**Bob submits medical data analysis.**

**Step 1:** Bob encrypts the analysis with verifiers' public keys.

**Step 2:** Bob publishes the encrypted evidence link + hash.

**Step 3:** Verifiers decrypt with their private keys.

**Step 4:** Verifiers check the evidence.

**Step 5:** Non-verifiers see only the hash.

### 17.6. Cross-context ZK proof

**Alice wants to prove "I am a member of some recognized context" without revealing which one.**

**Step 1:** Alice constructs a ZK proof:

- her DID is in the union of recognized contexts;
- she does not reveal which context.

**Step 2:** Verifier checks the proof.

**Result:** Verifier learns membership without learning which context.

### 17.7. GDPR erasure

**Alice requests erasure.**

**What can be erased:**
- her profile metadata (display name);
- her evidence links (revoked);
- her attestations (revoked by issuers).

**What cannot be erased:**
- her contribution history (needed for consensus);
- her DIDs (pseudonymous).

**Alice is informed of this at signup.**

### 17.8. Tor-routed sync

**Bob runs a node and wants to hide his IP.**

**Step 1:** Bob configures his node to use Tor.

**Step 2:** Bob connects to peers via `.onion` addresses.

**Step 3:** Bob's IP is hidden.

**Result:** Bob participates without revealing his location.

### 17.9. Metadata minimization

**A node operator logs events.**

**Policy:**
- no IP logging;
- no full payloads in logs;
- logs rotated every 24 hours;
- logs deleted after 7 days.

**Result:** Even if the node is breached, little metadata is exposed.

---

## 18. Test Vectors

Test vectors for privacy live in `spec/test-vectors/privacy.json`.

### 18.1. Coverage

- Selective disclosure proofs.
- ZK reputation proofs.
- Secret vote commitments and proofs.
- Nullifier generation.
- Private context encryption/decryption.
- Anonymous DID creation.
- Evidence encryption.
- Cross-context ZK proofs.
- GDPR erasure flows.

### 18.2. Format

```json
{
  "description": "ZK reputation proof",
  "public": {
    "root": "blake3:...",
    "context": "repo:x/y",
    "threshold": 500
  },
  "private": {
    "did": "did:cl:main:alice",
    "reputation": 750,
    "merkle_path": ["blake3:...", "blake3:..."]
  },
  "expected": {
    "proof": "zkp:...",
    "verify": true
  }
}
```

### 18.3. ZK test vectors

ZK proofs require a specific library. Implementations **MUST** agree on:

- the curve (e.g., BLS12-381);
- the proof system (e.g., PLONK);
- the commitment scheme (e.g., Pedersen).

### 18.4. Determinism

All proofs **MUST** be deterministic given the same inputs (for reproducibility).

### 18.5. Cross-implementation

Test vectors **MUST** pass on at least two implementations before v1.0.

### 18.6. Security tests

Test vectors **MUST** include:

- invalid proofs (rejected);
- forged proofs (rejected);
- replay attempts (rejected);
- wrong context (rejected).

---

## 19. Open Questions

- How to make ZK proofs **practical** at scale?
- Should **all** votes be secret by default?
- How to handle **private contexts** without a trusted key manager?
- Should there be a **minimum anonymity set** for private contexts?
- How to handle **post-quantum** ZK proofs?
- Should **metadata** be minimized at the protocol level or implementation level?
- How to balance **accountability** (for validators) with **privacy**?
- Should **anonymous DIDs** be able to vote in some contexts?
- How to handle **attestations** without revealing identity?
- Should there be a **privacy budget** for reputation (e.g., max proofs per day)?
- How to handle **GDPR erasure** without breaking consensus?
- Should there be a **standard** for ZK proofs across contexts?
- How to handle **cross-context privacy** when DIDs are linked?
- Should **private contexts** be discoverable?
- How to prevent **deanonymization** via graph analysis?

These will be resolved through RFCs and community discussion.

---

## Summary

**Privacy in CL is:**

- Pseudonymous by default.
- Data-minimized.
- Selective (disclosure on demand).
- Optional (private contexts, anonymous DIDs).
- Verifiable (ZK proofs).
- Compliant (GDPR-aware).

**Key mechanisms:**

- **Data minimization** — only necessary data on-ledger.
- **Selective disclosure** — prove statements without revealing data.
- **ZK proofs** — reputation, votes, membership.
- **Private contexts** — encrypted events, gated membership.
- **Anonymous DIDs** — no real-world link.
- **Metadata privacy** — Tor, relays, dummy traffic.
- **Encrypted evidence** — sensitive data protected.
- **Right to be forgotten** — off-ledger data deletable.
- **Cross-context privacy** — isolated by default.

**Threats:**

- De-anonymization.
- Correlation.
- Metadata leakage.
- Timing attacks.
- Censorship.
- Coercion.
- State surveillance.
- Quantum.

**Defenses:**

- Pseudonymity.
- ZK proofs.
- Encryption.
- Privacy modes.
- Data minimization.
- Multiple jurisdictions.

**Key insight:**

Privacy is not the absence of transparency. It is the **control** over what is revealed. CL is public by design — but only for what must be public. Everything else is under the user's control.

**The protocol provides tools. Users choose how much to reveal.**

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [identity.md](./identity.md) — identity model.
- [contribution.md](./contribution.md) — contribution records.
- [reputation.md](./reputation.md) — reputation calculation.
- [vote.md](./vote.md) — secret voting.
- [ledger.md](./ledger.md) — checkpoints and proofs.
- [consensus.md](./consensus.md) — validator visibility.
- [sync.md](./sync.md) — network privacy.
- [api.md](./api.md) — API and privacy.
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
