# Ledger

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md) · [identity.md](./identity.md) · [contribution.md](./contribution.md) · [reputation.md](./reputation.md)  
**Related:** [consensus.md](./consensus.md) · [sync.md](./sync.md) · [api.md](./api.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [DAG Structure](#3-dag-structure)
4. [Merkle Trees](#4-merkle-trees)
5. [Checkpoints](#5-checkpoints)
6. [Storage Schema](#6-storage-schema)
7. [Indexes](#7-indexes)
8. [State Derivation](#8-state-derivation)
9. [Compression](#9-compression)
10. [Pruning and Archiving](#10-pruning-and-archiving)
11. [Snapshots](#11-snapshots)
12. [Light Nodes](#12-light-nodes)
13. [Validation Rules](#13-validation-rules)
14. [Examples](#14-examples)
15. [Test Vectors](#15-test-vectors)
16. [Open Questions](#16-open-questions)

---

## 1. Overview

The **ledger** is the persistent, append-only record of all events in Contribution Ledger. It is structured as a **directed acyclic graph (DAG)**, not a linear chain of blocks.

The ledger provides:

- **Immutability** — events are never deleted or modified.
- **Verifiability** — every event can be proven to exist via Merkle proofs.
- **Efficient sync** — nodes synchronize by exchanging headers and proofs.
- **Compact storage** — old events can be compressed into checkpoints.
- **Fast queries** — indexes support common lookups.

**This file defines:**

- The DAG structure (Section 3).
- Merkle trees for event and state commitments (Section 4).
- Checkpoints for compact verification (Section 5).
- Storage schema and indexes (Sections 6–7).
- How state is derived from events (Section 8).
- Compression strategies (Section 9).
- Pruning and archiving (Section 10).
- Snapshots for historical queries (Section 11).
- Light node support (Section 12).
- Validation rules (Section 13).

Consensus (how events become final) is defined in [consensus.md](./consensus.md). Synchronization (how nodes exchange events) is defined in [sync.md](./sync.md).

---

## 2. Design Principles

### 2.1. Events are the source of truth

The ledger stores **events**, not state. All state (reputation, balances, roles) is derived by applying events in order.

### 2.2. Append-only

Events are never deleted or modified. Any change (revocation, rotation, update) is expressed as a new event.

**Exception:** pruning (Section 10) removes old events from a node's storage, but this is a local optimization, not a protocol change. Pruned nodes can re-fetch events from archive nodes.

### 2.3. DAG, not chain

Events form a **DAG** with hash links. There is no "next block" and no global ordering imposed by a single chain.

Topological order is sufficient for state derivation.

### 2.4. Deterministic state

Given the same set of events, every node computes the same state. This requires:

- deterministic ordering (Section 3.6);
- deterministic computation (see [reputation.md](./reputation.md#12-determinism-requirements));
- no reliance on local time or randomness.

### 2.5. Merkle-verifiable

Every event can be verified via a Merkle proof against a checkpoint. This allows light nodes to trust the ledger without downloading everything.

### 2.6. Checkpoint-friendly

The ledger supports **checkpoints** — signed commitments to the state at a point in time. Checkpoints allow:

- fast bootstrap (download checkpoint, verify, sync from there);
- light client verification;
- historical queries.

### 2.7. Storage-agnostic

The protocol defines the logical structure. Implementations **MAY** use any storage backend:

- SQLite (small nodes);
- PostgreSQL (large nodes);
- RocksDB (performance);
- custom (specialized).

### 2.8. Compressible

Old events **MAY** be compressed into checkpoints. Full history **MAY** be retained by archive nodes.

### 2.9. Prunable

Nodes **MAY** prune events they no longer need. Pruning does not affect the protocol; it is a local storage optimization.

### 2.10. Federated

Different communities **MAY** run separate ledgers that interoperate. The protocol supports this via cross-ledger references and shared checkpoints.

---

## 3. DAG Structure

### 3.1. Definition

A **DAG** (directed acyclic graph) is a graph where:

- edges have direction (from child to parent);
- there are no cycles.

In CL:

- **Nodes** are events.
- **Edges** are parent references (`parents` field in each event).
- **Direction** is from child to parent (each event points to its parents).

### 3.2. Why a DAG

A linear chain (like Bitcoin) requires global ordering. This has costs:

- one writer at a time (the miner);
- blocks are serial;
- forks are wasteful.

A DAG allows:

- parallel writes (multiple authors simultaneously);
- no block time;
- natural fork handling (branches can coexist until merged).

The trade-off: more complex state derivation and consensus.

### 3.3. Parents

Every event (except genesis) references one or more parents:

```json
"parents": ["blake3:abc...", "blake3:def..."]
```

Rules:

- Parents **MUST** exist in the ledger (or be pending).
- Parents **MUST NOT** create cycles.
- Parents **MAY** be from any author.

### 3.4. Heads and tips

**Heads** (or tips) are events with no children yet. They represent the "frontier" of the DAG.

When a new event is created:

- it references at least one current head;
- its own ID becomes a new head;
- the referenced head is no longer a head (it has a child now).

The set of heads is dynamic. It grows when branches are created, shrinks when they are merged.

### 3.5. Genesis

The **genesis event** is the root of the DAG. It has empty parents.

Genesis is defined by the community that starts the ledger. It typically includes:

- a `community.create` event;
- the founding identity;
- initial rules.

Example:

```json
{
  "version": 1,
  "type": "community.create",
  "author": "did:cl:main:founder",
  "created_at": 1730000000,
  "parents": [],
  "payload": {
    "id": "community:mycommunity",
    "name": "My Community",
    "rules": { ... }
  },
  "signature": "ed25519:..."
}
```

### 3.6. Topological order

Events are processed in **topological order**: an event is processed after all its ancestors.

**Partial order:** if event A is an ancestor of event B, then A < B.

**Incomparable events:** if neither is an ancestor of the other, they may be processed in either order. **State derivation MUST produce the same result regardless.**

To ensure this, some computations **MUST** sort incomparable events deterministically. The canonical order is:

1. By `created_at` (ascending).
2. If equal, by event ID (lexicographic).

This order is used for:

- summation in reputation (see [reputation.md](./reputation.md#123-summation-order));
- vote tallies;
- any cumulative computation.

### 3.7. Cycle prevention

A cycle would mean an event is its own ancestor. This is impossible by construction:

- An event's ID is derived from its content (including parents).
- Parents must exist before the event.
- Therefore, an event cannot be its own ancestor.

Implementations **MUST** verify this when accepting events. If a cycle is detected, the event is invalid.

### 3.8. Reachability

Two events are **connected** if there is a path between them (in either direction).

The DAG **SHOULD** be connected: every event **SHOULD** be reachable from the genesis.

If a node receives an event not connected to genesis, it **MUST** reject it (or hold it until the missing ancestors arrive).

### 3.9. Depth

The **depth** of an event is the length of the longest path from genesis to it.

Depth is used for:

- ordering (deeper events come later in the causal sense);
- checkpoints (commit to events up to a depth);
- sync (peers exchange depths to find common ancestors).

### 3.10. Width

The **width** (or branching factor) is the number of concurrent heads.

A wide DAG indicates parallel activity. A narrow DAG indicates one writer at a time.

### 3.11. Merging

When two branches exist, a new event **MAY** reference heads from both, merging them.

Merging events are common in CL: any event that references multiple heads (e.g., a confirmation that references both the contribution and the confirmer's own last event) acts as a merge.

### 3.12. Orphan events

An **orphan** is an event whose parents are unknown to the node.

Orphans **MUST NOT** be finalized until their ancestors are received.

Nodes **SHOULD** hold orphans in a temporary pool and request missing ancestors from peers.

If ancestors do not arrive within a timeout, orphans **MAY** be dropped.

### 3.13. Reorgs

Unlike blockchains, CL does not have "reorganizations" in the traditional sense.

Because the DAG allows multiple branches, a "reorg" would mean rejecting events that were previously accepted. This **MUST NOT** happen in CL.

Once an event is finalized (has enough validator signatures — see [consensus.md](./consensus.md)), it is permanent.

Unfinalized events **MAY** be discarded if they conflict with finalized events.

### 3.14. Conflicting events

Two events are **conflicting** if they cannot both be part of a consistent state.

Examples:

- Two `identity.create` events for the same DID.
- Two `contribution.revoke` and `contribution.unrevoke` for the same contribution (in the same branch).
- Two `vote.cast` events from the same identity for the same vote.

Conflicts are resolved by:

1. **DAG order:** the earlier event (in topological + canonical order) wins.
2. **Validator decision:** if validators disagree, the finalization threshold resolves it.
3. **Explicit resolution:** a new event (`*.resolve`) may override, if rules allow.

---

## 4. Merkle Trees

### 4.1. Purpose

Merkle trees provide:

- **Compact commitments** — a single hash represents a set of events.
- **Efficient proofs** — prove an event is in a set without downloading the set.
- **Light client support** — verify state without full history.

### 4.2. Types of Merkle trees in CL

| Tree | Purpose |
|---|---|
| **Event tree** | Commits to a set of events (used in checkpoints). |
| **State tree** | Commits to the derived state (reputation, roles). |
| **Per-context tree** | Commits to events in a specific context. |
| **Parent tree** | Commits to the parents of an event (for header verification). |

### 4.3. Hash function

All Merkle trees use **BLAKE3**.

Leaf hashes: `BLAKE3(0x00 || leaf_data)`  
Internal hashes: `BLAKE3(0x01 || left || right)`

The domain separation bytes (`0x00` for leaves, `0x01` for internal) prevent second-preimage attacks.

### 4.4. Event tree

A canonical Merkle tree over a set of events.

- **Leaves:** event IDs (32-byte BLAKE3 hashes).
- **Order:** events sorted by canonical order (Section 3.6).
- **Construction:** standard binary Merkle tree, left-to-right.

If the number of leaves is not a power of 2, the tree is unbalanced (left-heavy).

**Empty tree:** hash of empty string: `BLAKE3("")`.

**Single leaf:** the leaf hash itself.

### 4.5. Merkle proofs

A **Merkle proof** for leaf `L` is the set of sibling hashes from `L` to the root.

To verify:

1. Start with `h = leaf_hash(L)`.
2. For each sibling `s` in the proof (in order):
   - If `s` is a left sibling: `h = BLAKE3(0x01 || s || h)`.
   - If `s` is a right sibling: `h = BLAKE3(0x01 || h || s)`.
3. Compare the final `h` with the expected root.

Proof size: `O(log n)` where `n` is the number of leaves.

### 4.6. State tree

A Merkle tree over the derived state.

- **Leaves:** state entries, e.g., `(context, did) → reputation`.
- **Key hashing:** `BLAKE3(0x00 || context || did)` for key, `BLAKE3(0x01 || reputation_value)` for value.
- **Order:** entries sorted by key hash.

The **state root** is the root of this tree.

### 4.7. Per-context tree

A Merkle tree over events in a specific context.

Used for:

- checkpointing individual contexts;
- light clients interested in one context;
- cross-context proofs.

### 4.8. Parent tree

For each event, a Merkle tree over its parent IDs.

The **parent root** is included in the event header (optional).

This allows verifying the parent set without downloading each parent ID individually.

### 4.9. Sparse Merkle trees

For state trees with many possible keys (e.g., all DIDs), a **sparse Merkle tree** (SMT) is more efficient.

- Keys are hashed to a fixed-size space (e.g., 256 bits).
- Empty subtrees are represented by a single hash.
- Proofs are `O(log N)` where `N` is the key space size (256 for 2^256 keys).

CL **MAY** use SMTs for state commitments. Implementations **MUST** agree on the variant used.

### 4.10. Canonical form

For determinism, Merkle trees **MUST** be constructed in canonical form:

- leaves in canonical order;
- no duplicate leaves;
- no empty subtrees (except in SMTs);
- fixed domain separation.

### 4.11. Verification

To verify a Merkle proof:

1. Compute the leaf hash.
2. Apply the proof path.
3. Compare with the expected root.

If they match, the leaf is in the tree.

### 4.12. Proof size limits

For large trees, proofs can be large. Mitigations:

- **SMTs** — fixed-size proofs (256 bits).
- **Batched proofs** — prove multiple leaves in one proof.
- **Compressed proofs** — omit redundant siblings.

CL **MAY** use any of these, but implementations **MUST** agree.

---

## 5. Checkpoints

### 5.1. Purpose

A **checkpoint** is a signed commitment to the state of the ledger at a point in time. It provides:

- **Fast bootstrap** — new nodes can start from a checkpoint instead of genesis.
- **Light verification** — light clients can verify state against a checkpoint.
- **Historical queries** — snapshots of state at specific times.

### 5.2. Structure

```json
{
  "version": 1,
  "type": "checkpoint",
  "author": "did:cl:main:validator1",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "height": 100000,
    "depth": 50000,
    "event_root": "blake3:...",
    "state_root": "blake3:...",
    "context_roots": {
      "repo:x/y": "blake3:...",
      "org:mycompany": "blake3:..."
    },
    "rules_versions": {
      "repo:x/y": "blake3:...",
      "org:mycompany": "blake3:..."
    },
    "signatures": [
      {"signer": "did:cl:main:validator1", "signature": "ed25519:..."},
      {"signer": "did:cl:main:validator2", "signature": "ed25519:..."},
      {"signer": "did:cl:main:validator3", "signature": "ed25519:..."}
    ]
  },
  "signature": "ed25519:..."
}
```

### 5.3. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `height` | integer | MUST | Number of events included. |
| `depth` | integer | MAY | Maximum depth of events included. |
| `event_root` | string | MUST | Merkle root of all events up to this point. |
| `state_root` | string | MUST | Merkle root of the derived state. |
| `context_roots` | object | MAY | Per-context event roots. |
| `rules_versions` | object | MAY | Hashes of context rules at snapshot. |
| `signatures` | array | MUST | Validator signatures. |

### 5.4. Height

`height` is the number of events included in the checkpoint.

It serves as a monotonic counter: checkpoints **MUST** have strictly increasing height.

### 5.5. Depth

`depth` is the maximum DAG depth of events included.

Unlike height, depth is a measure of causal ordering, not count.

### 5.6. Event root

The `event_root` is a Merkle root over all events up to and including this checkpoint.

Events are sorted by canonical order (Section 3.6).

### 5.7. State root

The `state_root` is a Merkle root over the derived state at this checkpoint.

State includes:

- reputations per (context, DID);
- roles per (context, DID);
- active bounties;
- open votes;
- compute tasks;
- validator sets.

Implementations **MUST** agree on the exact state schema for the root to be verifiable.

### 5.8. Context roots

For federation and light clients, per-context roots allow verifying one context without downloading others.

A context root is a Merkle root over events in that context.

### 5.9. Rules versions

For historical queries, the checkpoint includes hashes of the context rules at the snapshot time.

This allows any node to reconstruct the exact rules used for reputation at that checkpoint.

### 5.10. Signatures

A checkpoint **MUST** be signed by at least the finalization threshold of validators (see [consensus.md](./consensus.md)).

For a 2/3 threshold with N validators, at least ⌈2N/3⌉ signatures are required.

Signatures are stored inside the payload, and the entire event is also signed by the author (the checkpoint creator).

### 5.11. Creation

A checkpoint is created periodically (e.g., every 10 000 events or every 24 hours).

Anyone **MAY** propose a checkpoint. It becomes valid when signed by enough validators.

### 5.12. Verification

To verify a checkpoint:

1. Verify the event's signature.
2. Verify each validator signature against the current validator set.
3. Verify the threshold is met.
4. Recompute `event_root` from events (if full history is available).
5. Recompute `state_root` from events (if full history is available).
6. Compare with the checkpoint's roots.

Light clients **MAY** skip steps 4–5 and trust the validator signatures (with the usual trust assumptions).

### 5.13. Bootstrap from checkpoint

A new node **MAY** bootstrap from a recent checkpoint:

1. Download the checkpoint.
2. Verify signatures.
3. Download the state (or recompute it from events, if available).
4. Sync events from the checkpoint forward.

This is much faster than syncing from genesis.

### 5.14. Checkpoint chain

Checkpoints form a chain: each checkpoint includes all events up to its height, so later checkpoints include earlier ones.

A checkpoint at height `H_1` is a prefix of a checkpoint at height `H_2 > H_1`.

### 5.15. Disputes

If two checkpoints at the same height have different roots, this indicates a **fork** in the ledger.

Resolution:

- Communities **MUST** define a fork resolution rule (e.g., the chain with more validator signatures wins).
- Alternatively, the fork is permanent, and communities choose a side.

See [consensus.md](./consensus.md) for details.

### 5.16. Storage of checkpoints

Checkpoints **MAY** be:

- stored as events in the ledger (with type `checkpoint`);
- stored separately (e.g., in a dedicated table);
- published to external storage (IPFS, Arweave).

The protocol does not require a specific storage.

### 5.17. Frequency

The frequency of checkpoints is a community decision.

Typical:

- every 10 000 events;
- every 24 hours;
- every 1 000 events for small communities.

More frequent checkpoints mean faster bootstrap but more overhead.

### 5.18. Checkpoint size

Checkpoints are small (a few KB), except:

- large per-context roots (for many contexts);
- large signature lists (for many validators).

For communities with many contexts, per-context roots **MAY** be omitted or sampled.

---

## 6. Storage Schema

### 6.1. Overview

The storage schema defines the tables (or collections) used by a node.

Implementations **MAY** use different schemas, but **MUST** support the same queries.

Recommended schema (SQL):

```sql
-- Events (the primary data)
CREATE TABLE events (
    id BLOB PRIMARY KEY,          -- 32-byte BLAKE3 hash
    version INTEGER NOT NULL,
    type TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    payload BLOB NOT NULL,        -- canonical CBOR
    signature BLOB NOT NULL,
    height INTEGER NOT NULL,      -- sequence number (local)
    depth INTEGER,                -- DAG depth (computed)
    finalized BOOLEAN DEFAULT FALSE,
    timestamp_received INTEGER
);

-- Parent references (DAG edges)
CREATE TABLE event_parents (
    event_id BLOB NOT NULL,
    parent_id BLOB NOT NULL,
    PRIMARY KEY (event_id, parent_id),
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (parent_id) REFERENCES events(id)
);

-- Derived state: identities
CREATE TABLE identities (
    did TEXT PRIMARY KEY,
    pubkey BLOB NOT NULL,
    created_at INTEGER NOT NULL,
    deactivated BOOLEAN DEFAULT FALSE,
    metadata BLOB,
    recovery_commitment BLOB,
    current_key_rotation_event BLOB
);

-- Derived state: attestations
CREATE TABLE attestations (
    id BLOB PRIMARY KEY,
    issuer TEXT NOT NULL,
    subject TEXT NOT NULL,
    claim TEXT NOT NULL,
    value BLOB,
    valid_until INTEGER,
    revoked BOOLEAN DEFAULT FALSE,
    created_at INTEGER NOT NULL
);

-- Derived state: contributions
CREATE TABLE contributions (
    id BLOB PRIMARY KEY,
    subject TEXT NOT NULL,
    issuer TEXT,
    action TEXT NOT NULL,
    context TEXT NOT NULL,
    weight_class TEXT NOT NULL,
    weight REAL,
    timestamp INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    confirmed BOOLEAN DEFAULT FALSE,
    revoked BOOLEAN DEFAULT FALSE,
    cu REAL DEFAULT 0,
    quality REAL DEFAULT 1.0
);

-- Contribution confirmations
CREATE TABLE confirmations (
    contribution_id BLOB NOT NULL,
    confirmer TEXT NOT NULL,
    quality REAL DEFAULT 1.0,
    comment TEXT,
    created_at INTEGER NOT NULL,
    PRIMARY KEY (contribution_id, confirmer)
);

-- Derived state: reputation
CREATE TABLE reputations (
    context TEXT NOT NULL,
    did TEXT NOT NULL,
    value REAL NOT NULL,
    computed_at INTEGER NOT NULL,
    PRIMARY KEY (context, did)
);

-- Contexts (communities)
CREATE TABLE contexts (
    id TEXT PRIMARY KEY,
    name TEXT,
    rules BLOB NOT NULL,           -- canonical CBOR
    rules_version BLOB NOT NULL,   -- BLAKE3 of rules
    created_at INTEGER NOT NULL,
    updated_at INTEGER
);

-- Roles
CREATE TABLE roles (
    context TEXT NOT NULL,
    did TEXT NOT NULL,
    role TEXT NOT NULL,
    granted_at INTEGER NOT NULL,
    revoked_at INTEGER,
    PRIMARY KEY (context, did, role)
);

-- Validators
CREATE TABLE validators (
    did TEXT NOT NULL,
    context TEXT,
    added_at INTEGER NOT NULL,
    removed_at INTEGER,
    PRIMARY KEY (did, context)
);

-- Checkpoints
CREATE TABLE checkpoints (
    id BLOB PRIMARY KEY,
    height INTEGER NOT NULL,
    depth INTEGER,
    event_root BLOB NOT NULL,
    state_root BLOB NOT NULL,
    context_roots BLOB,
    signatures BLOB NOT NULL,
    created_at INTEGER NOT NULL
);

-- Bounties
CREATE TABLE bounties (
    id BLOB PRIMARY KEY,
    issuer TEXT NOT NULL,
    context TEXT NOT NULL,
    task TEXT NOT NULL,
    reward_amount REAL NOT NULL,
    reward_currency TEXT NOT NULL,
    escrow_id TEXT,
    deadline INTEGER,
    status TEXT NOT NULL,          -- open, claimed, submitted, completed, cancelled
    created_at INTEGER NOT NULL
);

-- Votes
CREATE TABLE votes (
    id BLOB PRIMARY KEY,
    creator TEXT NOT NULL,
    context TEXT NOT NULL,
    proposal TEXT NOT NULL,
    options BLOB NOT NULL,
    deadline INTEGER NOT NULL,
    threshold TEXT NOT NULL,
    weighting TEXT NOT NULL,
    snapshot BLOB NOT NULL,
    status TEXT NOT NULL,          -- open, closed
    created_at INTEGER NOT NULL
);

-- Vote casts
CREATE TABLE vote_casts (
    vote_id BLOB NOT NULL,
    voter TEXT NOT NULL,
    option TEXT NOT NULL,
    weight REAL NOT NULL,
    created_at INTEGER NOT NULL,
    PRIMARY KEY (vote_id, voter)
);

-- Compute tasks
CREATE TABLE compute_tasks (
    id BLOB PRIMARY KEY,
    issuer TEXT NOT NULL,
    kind TEXT NOT NULL,
    task BLOB NOT NULL,
    reward_amount REAL,
    reward_currency TEXT,
    redundancy INTEGER,
    verification TEXT,
    deadline INTEGER,
    status TEXT NOT NULL,          -- open, claimed, submitted, verified, completed, disputed
    created_at INTEGER NOT NULL
);
```

### 6.2. Field encoding

- **Event IDs, hashes:** 32-byte BLOB (BLAKE3).
- **Signatures:** 64-byte BLOB (Ed25519).
- **DIDs:** TEXT (UTF-8).
- **Timestamps:** INTEGER (Unix seconds).
- **Payloads:** BLOB (canonical CBOR).
- **Real values:** REAL (double precision, rounded to 6 decimals).

### 6.3. Immutability

The `events` and `event_parents` tables are **append-only**. Rows are never updated or deleted (except via pruning, Section 10).

The derived state tables (`identities`, `contributions`, etc.) **MAY** be updated as new events are processed.

### 6.4. Consistency

Derived state **MUST** be consistent with events. If state and events disagree, events are authoritative.

A node **MAY** rebuild derived state from scratch by replaying all events.

### 6.5. Atomicity

When processing an event:

1. Verify the event.
2. Insert into `events`.
3. Insert parents into `event_parents`.
4. Update derived state tables.
5. Commit the transaction.

If any step fails, the entire transaction **MUST** roll back.

### 6.6. Concurrency

Multiple events **MAY** be processed concurrently, as long as they are independent (no parent-child relationship).

Events in a parent-child chain **MUST** be processed in order.

### 6.7. Backups

Nodes **SHOULD** back up:

- the event log (essential);
- checkpoints (for fast recovery);
- derived state (optional — can be recomputed).

### 6.8. Portability

The event log **MUST** be exportable in a portable format:

- newline-delimited JSON (one event per line);
- or a length-prefixed binary stream.

This allows migration between implementations.

---

## 7. Indexes

### 7.1. Purpose

Indexes speed up common queries:

- find events by author;
- find contributions by subject;
- find confirmations for a contribution;
- find votes by context;
- find bounties by status.

### 7.2. Recommended indexes

```sql
CREATE INDEX idx_events_author ON events(author);
CREATE INDEX idx_events_type ON events(type);
CREATE INDEX idx_events_created_at ON events(created_at);
CREATE INDEX idx_events_finalized ON events(finalized);

CREATE INDEX idx_event_parents_parent ON event_parents(parent_id);

CREATE INDEX idx_contributions_subject ON contributions(subject);
CREATE INDEX idx_contributions_context ON contributions(context);
CREATE INDEX idx_contributions_timestamp ON contributions(timestamp);

CREATE INDEX idx_confirmations_contribution ON confirmations(contribution_id);

CREATE INDEX idx_attestations_subject ON attestations(subject);
CREATE INDEX idx_attestations_issuer ON attestations(issuer);

CREATE INDEX idx_reputations_context ON reputations(context);

CREATE INDEX idx_roles_context ON roles(context);
CREATE INDEX idx_roles_did ON roles(did);

CREATE INDEX idx_bounties_context ON bounties(context);
CREATE INDEX idx_bounties_status ON bounties(status);

CREATE INDEX idx_votes_context ON votes(context);
CREATE INDEX idx_votes_status ON votes(status);

CREATE INDEX idx_checkpoints_height ON checkpoints(height);
```

### 7.3. Secondary indexes

For large ledgers, additional indexes **MAY** be added:

- full-text search on metadata;
- context-specific indexes;
- time-bucketed indexes.

### 7.4. Index maintenance

Indexes **MUST** be updated atomically with the underlying tables.

### 7.5. Index size

Indexes add storage overhead (typically 20–50% of the data).

Nodes **MAY** disable indexes they do not need (e.g., a full node that only serves sync).

---

## 8. State Derivation

### 8.1. Determinism

Given the same set of finalized events, all nodes **MUST** derive the same state.

### 8.2. Order of application

Events are applied in **canonical order**:

1. By `depth` (ascending).
2. If equal, by `created_at` (ascending).
3. If equal, by event ID (lexicographic).

Depth is the DAG depth (longest path from genesis).

### 8.3. State variables

Derived state includes:

- **identities** — active, deactivated, current key.
- **attestations** — active, revoked, expired.
- **contributions** — pending, confirmed, revoked.
- **reputation** — per (context, DID).
- **roles** — per (context, DID).
- **validators** — per context.
- **bounties** — status, escrow, escrow balance.
- **votes** — open, closed, tallies.
- **compute tasks** — status, results.
- **checkpoints** — latest height.

### 8.4. Incremental derivation

When a new event is added, state is updated incrementally:

1. Parse the event.
2. Determine its effect on state.
3. Apply the effect.
4. Update indexes.

If the event is invalid, it **MUST** be rejected before state changes.

### 8.5. State conflicts

If two events conflict (e.g., two validators added for the same context in parallel), state derivation **MUST** handle it deterministically:

- by canonical order (earlier wins);
- or by rules (context-specific);
- or by flagging the conflict for resolution.

### 8.6. Rebuild

A node **MAY** rebuild state from scratch by:

1. Deleting all derived state.
2. Replaying all events in canonical order.
3. Rebuilding indexes.

This is used for:

- recovering from corruption;
- verifying state against events;
- bootstrapping.

### 8.7. State root computation

For checkpoints, the state root is computed by:

1. Collecting all state entries (e.g., all (context, DID) → reputation).
2. Serializing each entry canonically.
3. Hashing each entry (leaf).
4. Building a Merkle tree.
5. Taking the root.

Implementations **MUST** agree on:

- entry serialization format;
- Merkle tree construction (Section 4);
- ordering of entries.

### 8.8. State size

State size grows with:

- number of identities;
- number of contributions;
- number of contexts;
- number of roles.

For large ledgers, state **MAY** be sharded:

- per context;
- per time period;
- per identity prefix.

Sharding is an implementation detail, not a protocol requirement.

### 8.9. State pruning

Old state **MAY** be pruned if:

- it is committed in a checkpoint;
- it is not needed for current queries.

Example: contributions from 10 years ago with zero decayed CU may be omitted from current state.

Pruning **MUST NOT** affect the ability to verify checkpoints.

### 8.10. State queries

Common queries:

- `reputation(did, context)` — current reputation.
- `reputation_at(did, context, time)` — historical reputation.
- `contributions(subject)` — all contributions by an identity.
- `level(did, context)` — current level.
- `roles(did, context)` — current roles.

These are served via API (see [api.md](./api.md)) and backed by indexes.

---

## 9. Compression

### 9.1. Purpose

The ledger grows unboundedly. Compression reduces storage and bandwidth.

### 9.2. Types of compression

| Type | Description |
|---|---|
| **Event compression** | Compress individual event payloads. |
| **Checkpoint compression** | Replace old events with checkpoints. |
| **Delta compression** | Store only differences between versions. |
| **Dictionary compression** | Reuse common strings (DIDs, contexts). |

### 9.3. Event compression

Event payloads **MAY** be compressed using:

- zstd;
- gzip;
- brotli.

Compression is **transparent** — the event ID is computed over the **uncompressed** canonical CBOR.

Implementations **MUST** decompress before validating.

Compressed events **MUST** be marked with a compression flag in storage (not in the event itself).

### 9.4. Checkpoint compression

Old events **MAY** be replaced by checkpoints:

- keep events up to height `H`;
- keep checkpoint at height `H`;
- delete events below `H - Δ` (retention window).

The retention window Δ is a local policy (e.g., 30 days of history).

Archive nodes keep full history.

### 9.5. Delta compression

For related events (e.g., consecutive confirmations of the same contribution), delta encoding **MAY** be used.

Delta encoding is an implementation detail, not a protocol requirement.

### 9.6. Dictionary compression

Common strings (DIDs, contexts, action names) **MAY** be stored in a dictionary, with events referencing dictionary entries.

This is a storage optimization. It does not affect event IDs.

### 9.7. Network compression

During sync (see [sync.md](./sync.md)), events **MAY** be compressed in transit.

Peers negotiate compression via protocol handshake.

### 9.8. Compression and determinism

Compression **MUST NOT** affect:

- event IDs;
- signatures;
- state derivation.

Compressed and uncompressed representations **MUST** produce the same results.

### 9.9. Recommended compression

For storage: **zstd** (level 3–6).  
For network: **zstd** (level 1–3) or **brotli** (quality 4–6).

### 9.10. Decompression cost

Decompression adds CPU overhead. Nodes **MAY** choose not to compress if CPU is the bottleneck.

---

## 10. Pruning and Archiving

### 10.1. Purpose

Pruning removes data a node no longer needs. Archiving preserves full history.

Different nodes have different needs:

- **Light nodes:** store headers and checkpoints only.
- **Full nodes:** store all events.
- **Archive nodes:** store all events, including pruned ones.
- **Pruned nodes:** store recent events and checkpoints, delete old ones.

### 10.2. Pruning rules

A node **MAY** prune events if:

- the event is included in a finalized checkpoint;
- the event is older than the retention window;
- the event is not needed for any open dispute, vote, or bounty.

### 10.3. Retention window

The retention window is a local policy. Typical: 30–90 days.

Events within the window are retained for:

- responding to disputes;
- serving light clients;
- recomputing state if needed.

### 10.4. What cannot be pruned

- the latest checkpoint;
- events referenced by open disputes, votes, or bounties;
- events that affect current state (reputation, roles, etc.).

### 10.5. Archiving

An **archive node** retains all events, including pruned ones.

Archive nodes serve:

- historical queries;
- syncing new nodes from genesis;
- dispute resolution.

Communities **SHOULD** maintain at least one archive node.

### 10.6. Pruning and consensus

Pruning does not affect consensus. A pruned node still validates new events.

But a pruned node **MUST** be able to:

- verify checkpoints;
- serve light clients;
- participate in consensus (if validator).

If pruning would prevent any of these, it **MUST NOT** be done.

### 10.7. Pruning procedure

1. Identify events outside the retention window.
2. Verify they are included in a checkpoint.
3. Delete from `events` and `event_parents`.
4. Keep `checkpoints` intact.

### 10.8. Pruning and reprocessing

If a node later needs pruned events (e.g., for a dispute), it **MUST** re-fetch them from archive nodes.

### 10.9. Storage estimates

For a ledger with 1 million events (average 1 KB each):

- Full storage: ~1 GB.
- With compression: ~300 MB.
- With pruning (retain 10%): ~100 MB.

For 100 million events:

- Full storage: ~100 GB.
- With compression: ~30 GB.
- With pruning: ~3 GB.

### 10.10. Archiving to external storage

Archive nodes **MAY** store events in external storage:

- IPFS (content-addressed);
- Arweave (permanent);
- S3-compatible (cost-effective).

Events **MUST** be retrievable by ID.

---

## 11. Snapshots

### 11.1. Purpose

A **snapshot** is a frozen state at a specific time. Used for:

- historical queries;
- votes (frozen reputation);
- audits;
- light client verification.

### 11.2. Snapshot structure

```json
{
  "context": "repo:x/y",
  "time": 1730000000,
  "event_count": 50000,
  "state_root": "blake3:...",
  "reputations": {
    "did:cl:main:alice": 150.500000,
    "did:cl:main:bob": 320.750000
  },
  "rules_version": "blake3:..."
}
```

### 11.3. Snapshot time

The snapshot time is the **maximum event timestamp** included.

Events with `created_at > snapshot_time` are excluded.

### 11.4. Snapshot root

The `state_root` is a Merkle root over the reputations map.

This allows verification without recomputation.

### 11.5. Snapshot creation

Snapshots **MAY** be created:

- by validators, as part of a checkpoint;
- on demand by any node;
- by users, for specific queries.

### 11.6. Snapshot verification

To verify a snapshot:

1. Recompute the reputations from events up to `time`.
2. Compute the `state_root`.
3. Compare.

If they differ, the snapshot is invalid.

### 11.7. Snapshot storage

Snapshots **MAY** be:

- stored in the ledger as `checkpoint` events;
- stored off-chain (e.g., in files);
- computed on demand.

### 11.8. Snapshot expiry

Snapshots do not expire. They are historical facts.

However, nodes **MAY** garbage-collect old snapshots if they can be recomputed.

### 11.9. Snapshot size

For a context with 1 million identities:

- Full snapshot: ~50 MB.
- Compressed: ~10 MB.
- Merkle root only: 32 bytes.

For most contexts, snapshots are small.

---

## 12. Light Nodes

### 12.1. Purpose

A **light node** does not store the full ledger. It stores:

- checkpoints;
- block headers (event headers);
- Merkle proofs on demand.

Light nodes can:

- verify events without full history;
- query state via proofs;
- participate in some operations (e.g., voting, if allowed).

### 12.2. Light node storage

| Component | Size |
|---|---|
| Checkpoints | ~1 MB per 10 000 events |
| Headers | ~200 bytes per event |
| Proofs | On demand |

For a 1 million event ledger: ~200 MB of headers + checkpoints.

### 12.3. Header structure

A **header** is a compact representation of an event:

```json
{
  "id": "blake3:...",
  "type": "contribution.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:...", "blake3:..."],
  "payload_root": "blake3:..."
}
```

The `payload_root` is a hash of the payload, allowing verification without the full payload.

### 12.4. Proof requests

A light node requests proofs from full nodes:

- "Prove that event X exists."
- "Prove that event X has these parents."
- "Prove that identity Y has reputation Z."

Full nodes respond with Merkle proofs, which the light node verifies against a checkpoint.

### 12.5. Trust assumptions

Light nodes trust:

- the checkpoint signatures (validators are honest);
- the Merkle proofs (cryptographic).

They do not trust individual full nodes (a malicious full node cannot forge proofs).

### 12.6. Light node operations

Light nodes **MAY**:

- read state;
- verify events;
- vote (if they can prove reputation);
- create events (by submitting to full nodes).

They **MUST NOT**:

- serve as validators (they lack full state);
- serve proofs to others (they lack the data).

### 12.7. Mobile clients

Light nodes are the natural fit for mobile clients:

- small storage footprint;
- fast sync;
- low bandwidth.

See [api.md](./api.md) for the light client API.

---

## 13. Validation Rules

Validators **MUST** enforce these rules for ledger operations.

### 13.1. Event insertion

- The event **MUST** be valid per [events.md](./events.md#10-validation-rules).
- All parents **MUST** exist.
- No cycle is created.
- The event **MUST** be connected to genesis.

### 13.2. DAG integrity

- The DAG **MUST** remain acyclic.
- Every event **MUST** be reachable from genesis.
- No duplicate parent references.

### 13.3. Checkpoint validation

- `height` **MUST** be strictly greater than the previous checkpoint.
- `event_root` **MUST** match the recomputed root.
- `state_root` **MUST** match the recomputed root.
- Signatures **MUST** meet the finalization threshold.

### 13.4. State derivation

- State **MUST** be derived deterministically from events.
- Any non-determinism is a bug.
- State root **MUST** match the recomputed value.

### 13.5. Snapshot validation

- Snapshot time **MUST** be ≤ current time.
- Snapshot **MUST** include all events up to that time.
- Snapshot root **MUST** match recomputed value.

### 13.6. Pruning

- Pruned events **MUST** be included in a checkpoint.
- Pruning **MUST NOT** break validation or consensus.

### 13.7. Compression

- Decompressed events **MUST** match the original.
- Event IDs **MUST** be computed over uncompressed data.

### 13.8. Merkle proofs

- Proofs **MUST** verify against the expected root.
- Proof size **MUST** be `O(log n)`.

### 13.9. Light node support

- Light nodes **MUST** be able to verify checkpoints.
- Proofs **MUST** be available for common queries.

---

## 14. Examples

### 14.1. Minimal DAG

```
genesis (event 1)
    │
    ├── event 2
    │      │
    │      └── event 4
    │
    └── event 3
           │
           └── event 5 (merge of 4 and 3)
```

### 14.2. Merkle tree

Events: `[E1, E2, E3, E4]`

```
        root
       /    \
      H12    H34
      / \    / \
    H1  H2  H3  H4
```

Where:

- `H1 = BLAKE3(0x00 || E1)`
- `H12 = BLAKE3(0x01 || H1 || H2)`
- `root = BLAKE3(0x01 || H12 || H34)`

### 14.3. Merkle proof

Prove `E2` exists:

- Proof: `[H1, H34]`
- Verify:
  - `H2 = BLAKE3(0x00 || E2)`
  - `H12 = BLAKE3(0x01 || H1 || H2)`
  - `root = BLAKE3(0x01 || H12 || H34)`
  - Compare with expected root.

### 14.4. Checkpoint

```json
{
  "version": 1,
  "type": "checkpoint",
  "author": "did:cl:main:validator1",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "height": 100000,
    "depth": 50000,
    "event_root": "blake3:abc...",
    "state_root": "blake3:def...",
    "context_roots": {
      "repo:x/y": "blake3:ghi..."
    },
    "rules_versions": {
      "repo:x/y": "blake3:jkl..."
    },
    "signatures": [
      {"signer": "did:cl:main:validator1", "signature": "ed25519:..."},
      {"signer": "did:cl:main:validator2", "signature": "ed25519:..."}
    ]
  },
  "signature": "ed25519:..."
}
```

### 14.5. Bootstrap from checkpoint

1. New node downloads checkpoint at height 100000.
2. Verifies signatures.
3. Downloads state root (or state).
4. Syncs events from height 100000 forward.
5. Node is operational.

### 14.6. Pruning

Node retains:

- events from the last 30 days;
- checkpoints;
- all state.

Events older than 30 days that are in a checkpoint are pruned.

### 14.7. Light node query

"Prove that event `blake3:abc` exists."

1. Light node requests proof from full node.
2. Full node returns `[H1, H34, ...]` (Merkle path).
3. Light node verifies against its latest checkpoint.

---

## 15. Test Vectors

Test vectors for the ledger live in `spec/test-vectors/ledger.json`.

### 15.1. Coverage

- DAG construction with multiple branches.
- Topological order.
- Canonical order (ties broken by ID).
- Merkle tree construction (various sizes).
- Merkle proofs (valid and invalid).
- Sparse Merkle tree (if used).
- Checkpoint creation and verification.
- Snapshot creation and verification.
- Pruning logic.
- Light node proofs.

### 15.2. Format

```json
{
  "description": "Merkle tree with 4 leaves",
  "input": {
    "leaves": ["E1", "E2", "E3", "E4"]
  },
  "expected": {
    "root": "blake3:...",
    "tree": {
      "H1": "blake3:...",
      "H2": "blake3:...",
      "H12": "blake3:...",
      "H34": "blake3:..."
    }
  }
}
```

### 15.3. Determinism

Every implementation **MUST** produce the same:

- Merkle roots;
- event IDs;
- state roots;
- checkpoint IDs.

### 15.4. Cross-implementation

Test vectors **MUST** pass on at least two implementations before protocol v1.0.

---

## 16. Open Questions

- Should the ledger use **sparse Merkle trees** for state, or regular Merkle trees?
- How to handle **very large state** (millions of identities)?
- Should there be a **protocol-level pruning** rule, or is it purely local?
- How to handle **checkpoint disputes** (two checkpoints at the same height)?
- Should checkpoints be **mandatory** or optional?
- How to handle **cross-ledger** checkpoints (federation)?
- Should there be a **canonical bootstrap** sequence?
- How to handle **state sharding** at the protocol level?
- Should there be a **maximum DAG width**?
- How to prevent **parent spam** (referencing many parents to slow down validation)?
- Should there be a **minimum checkpoint frequency**?
- How to handle **orphan events** that never connect to genesis?
- Should there be a **fee for large events** (to prevent spam)?
- How to handle **storage backends** for very large ledgers?
- Should the protocol define **backup and restore** procedures?

These will be resolved through RFCs and community discussion.

---

## Summary

**The ledger is:**

- A DAG of events.
- Append-only.
- Deterministic.
- Merkle-verifiable.
- Checkpoint-friendly.
- Compressible.
- Prunable.

**Key structures:**

- **Events** — atomic units, hash-linked.
- **DAG** — parents, heads, depth.
- **Merkle trees** — event roots, state roots, proofs.
- **Checkpoints** — signed commitments to state.
- **Snapshots** — frozen reputation at a time.

**Storage:**

- Events (primary).
- Parents (DAG edges).
- Derived state (identities, contributions, reputation, roles).
- Indexes (for queries).
- Checkpoints.

**Compression:**

- Event-level (zstd, gzip).
- Checkpoint-level (replace old events).
- Delta, dictionary.

**Pruning:**

- Local policy.
- Retain retention window + checkpoints.
- Archive nodes keep full history.

**Light nodes:**

- Headers + checkpoints + proofs.
- Fast sync, small storage.
- Suitable for mobile.

**Validation:**

- DAG integrity, checkpoint signatures, state determinism.

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [identity.md](./identity.md) — identity model.
- [contribution.md](./contribution.md) — contribution records.
- [reputation.md](./reputation.md) — reputation calculation.
- [consensus.md](./consensus.md) — finalization and validators.
- [sync.md](./sync.md) — P2P synchronization.
- [api.md](./api.md) — API endpoints.
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
