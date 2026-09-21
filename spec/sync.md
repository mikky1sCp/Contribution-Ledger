# Synchronization

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md) · [ledger.md](./ledger.md) · [consensus.md](./consensus.md)  
**Related:** [api.md](./api.md) · [privacy.md](./privacy.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [Network Topology](#3-network-topology)
4. [Peer Discovery](#4-peer-discovery)
5. [Connection Handshake](#5-connection-handshake)
6. [Message Types](#6-message-types)
7. [Gossip Protocol](#7-gossip-protocol)
8. [Header Exchange](#8-header-exchange)
9. [Event Propagation](#9-event-propagation)
10. [Sync Strategies](#10-sync-strategies)
11. [Orphan Handling](#11-orphan-handling)
12. [Conflict Resolution](#12-conflict-resolution)
13. [Checkpoint Sync](#13-checkpoint-sync)
14. [Light Client Sync](#14-light-client-sync)
15. [Anti-Spam and Rate Limiting](#15-anti-spam-and-rate-limiting)
16. [Privacy Considerations](#16-privacy-considerations)
17. [Validation Rules](#17-validation-rules)
18. [Examples](#18-examples)
19. [Test Vectors](#19-test-vectors)
20. [Open Questions](#20-open-questions)

---

## 1. Overview

**Synchronization** is how nodes in CL exchange events, headers, and checkpoints to maintain a consistent view of the ledger.

Without sync, each node would be isolated. With sync, thousands of nodes form a single logical ledger — even though no central server exists.

**This file defines:**

- The network topology (Section 3).
- How nodes find each other (Section 4).
- The handshake between peers (Section 5).
- The message types (Section 6).
- How events propagate via gossip (Section 7).
- How headers are exchanged (Section 8).
- How new events are announced and fetched (Section 9).
- The full sync strategies (Section 10).
- How orphans are handled (Section 11).
- How conflicts are resolved (Section 12).
- Checkpoint-based sync (Section 13).
- Light client sync (Section 14).
- Anti-spam and rate limits (Section 15).
- Privacy considerations (Section 16).
- Validation rules (Section 17).

Sync is the nervous system of CL. Without it, there is no network — only isolated nodes.

---

## 2. Design Principles

### 2.1. Peer-to-peer, not client-server

There is no central server. Every node **MAY** connect to any other node. Any node **MAY** serve events to any other node.

This means:

- no single point of failure;
- no single point of censorship;
- no central trust.

### 2.2. Push + pull

Events are **pushed** via gossip (proactive) and **pulled** via sync requests (reactive).

Push ensures fast propagation. Pull ensures consistency when messages are lost.

### 2.3. Header-first sync

Nodes sync **headers** first (small), then **events** (large).

This allows:

- fast initial sync (verify chain of headers);
- selective event fetching (only what is needed);
- light client support.

### 2.4. Deterministic reconciliation

Given the same set of events, all nodes **MUST** compute the same state. Sync is a mechanism to converge on the same set of events, not to negotiate state.

### 2.5. Idempotent messages

Every message **MUST** be idempotent: receiving the same message twice has no additional effect.

This allows safe retransmission.

### 2.6. Bounded resources

A node **MUST** bound:

- number of peers (e.g., 8–50);
- bandwidth per peer (e.g., 1 MB/s);
- orphans held (e.g., 1000);
- pending requests (e.g., 100).

This prevents resource exhaustion.

### 2.7. Privacy-aware

Sync **SHOULD** minimize metadata leakage:

- no broadcasting of interest profiles;
- optional privacy mode (relay through intermediaries);
- encrypted transport.

### 2.8. Federated

Different ledgers **MAY** have different sync networks. Nodes **MAY** participate in multiple ledgers.

Cross-ledger sync is possible (see [consensus.md](./consensus.md#11-federation)) but not required.

---

## 3. Network Topology

### 3.1. Overlay network

CL runs on top of an **overlay network**:

- transport: TCP, QUIC, WebSocket;
- discovery: bootstrap nodes, DHT, gossip;
- addressing: peer IDs (derived from public keys).

The overlay is independent of the physical network.

### 3.2. Peer types

| Type | Description |
|---|---|
| **Full node** | Stores all events, serves sync. |
| **Archive node** | Stores full history, serves historical queries. |
| **Light node** | Stores headers + checkpoints, requests proofs. |
| **Validator** | Full node + signs checkpoints. |
| **Relay** | Forwards messages without storing full ledger. |

A node **MAY** be multiple types.

### 3.3. Connection model

Each node maintains:

- **outbound connections** (to peers it chose);
- **inbound connections** (from peers that chose it).

Typical: 8–12 outbound, up to 50 inbound.

### 3.4. Peer ID

A peer is identified by its **peer ID**, derived from its public key:

```
peer_id = base58(SHA-256(pubkey))
```

The peer ID is stable across connections. A node **MUST** use the same peer ID for all connections.

### 3.5. Ledger ID

Each ledger has a **ledger ID**:

```
ledger_id = BLAKE3(genesis_event_id)
```

Nodes **MUST NOT** connect to peers on a different ledger (unless explicitly configured for federation).

The ledger ID is exchanged during handshake (Section 5).

### 3.6. Multi-ledger nodes

A node **MAY** participate in multiple ledgers:

- separate connections per ledger;
- separate ledgers stored separately;
- separate peer sets.

This is common for federated setups.

### 3.7. Bootstrap network

A new node needs at least one peer to join the network.

**Bootstrap nodes** are well-known, long-running nodes that:

- accept inbound connections from new nodes;
- provide an initial peer list;
- serve the initial sync.

Bootstrap nodes **MUST** be publicly listed (in the community's rules, or a well-known configuration file).

Communities **SHOULD** run multiple bootstrap nodes to avoid a single point of failure.

### 3.8. Topology goals

- **Resilience.** No single node is critical.
- **Low latency.** Event propagation within seconds.
- **Bandwidth efficiency.** Do not send the same event to a node twice.
- **Sybil resistance.** Do not let an attacker dominate the peer set.

### 3.9. Not a full mesh

Connections are **not** all-to-all. Full mesh does not scale.

Instead, the network forms a **random graph** with high connectivity.

Typical: each node connects to 8–12 peers, forming a small-world network.

---

## 4. Peer Discovery

### 4.1. Discovery methods

Nodes discover peers via:

1. **Bootstrap nodes.** Static list of well-known addresses.
2. **Peer exchange (PEX).** Peers share lists of known peers.
3. **Distributed hash table (DHT).** Kademlia-based lookup.
4. **Gossip discovery.** Peers announce themselves via gossip.
5. **Manual configuration.** User-configured peers.

CL **SHOULD** support at least bootstrap + PEX + DHT.

### 4.2. Bootstrap

At startup, a node:

1. Loads the bootstrap list.
2. Connects to 2–4 bootstrap nodes.
3. Performs handshake (Section 5).
4. Requests a peer list.
5. Connects to additional peers.
6. Begins sync.

### 4.3. Peer exchange (PEX)

After handshake, peers **MAY** exchange lists of known peers.

**Message:**

```json
{
  "type": "pex",
  "peers": [
    {"addr": "/ip4/1.2.3.4/tcp/4001/p2p/Qm...", "last_seen": 1730000000},
    ...
  ]
}
```

**Rules:**

- PEX messages **MUST NOT** contain more than 100 peers.
- PEX **MUST NOT** be sent more than once per hour per peer.
- A node **MUST NOT** blindly trust PEX; it **SHOULD** verify peers before connecting.

### 4.4. DHT

For large networks, a DHT (Kademlia) provides peer lookup by key.

Keys are derived from peer IDs. A node stores pointers to peers whose IDs are "close" to its own.

CL **MAY** use an existing DHT (e.g., libp2p Kademlia) or implement a simple one.

### 4.5. Gossip discovery

Peers **MAY** announce themselves via gossip:

```json
{
  "type": "peer.announce",
  "addr": "/ip4/1.2.3.4/tcp/4001/p2p/Qm...",
  "capabilities": ["full", "validator"]
}
```

Announcements are rate-limited (e.g., 1 per minute per peer).

### 4.6. Manual peers

Users **MAY** configure peers manually:

```toml
[[peers]]
addr = "/ip4/1.2.3.4/tcp/4001/p2p/Qm..."
```

Manual peers are always connected, regardless of discovery.

### 4.7. Peer scoring

To avoid connecting to misbehaving peers, nodes **SHOULD** score peers:

| Metric | Effect |
|---|---|
| Uptime | + |
| Valid events served | + |
| Invalid events served | − |
| Rate limit violations | − |
| Timeouts | − |
| Duplicate messages | − |

Peers with low scores are disconnected.

### 4.8. Ban list

A node **MAY** maintain a ban list for peers that:

- repeatedly send invalid events;
- violate rate limits;
- attempt Sybil attacks;
- are flagged by the community.

Bans **MAY** be permanent or temporary.

### 4.9. Sybil resistance

Peer discovery **SHOULD** resist Sybil attacks:

- limit inbound connections per IP;
- require proof of work for new connections (optional);
- use reputation-based peer selection.

### 4.10. Privacy

For privacy, nodes **MAY**:

- use Tor or I2P for transport;
- connect through relays;
- disable peer discovery.

This trades convenience for privacy.

---

## 5. Connection Handshake

### 5.1. Purpose

The handshake:

- establishes the connection;
- authenticates peers (via public keys);
- exchanges capabilities;
- verifies ledger ID;
- negotiates protocol version.

### 5.2. Handshake phases

```
Initiator                    Responder
   |                              |
   |------ HELLO ---------------->|
   |<----- HELLO ----------------|
   |------ AUTH ----------------->|
   |<----- AUTH -----------------|
   |------ READY ---------------->|
   |<----- READY ----------------|
   |                              |
   |<===== SESSION ==============>|
```

### 5.3. HELLO

The initiator sends:

```json
{
  "type": "hello",
  "protocol_version": 1,
  "ledger_id": "blake3:...",
  "peer_id": "Qm...",
  "capabilities": ["full", "gossip"],
  "listen_addr": "/ip4/1.2.3.4/tcp/4001",
  "nonce": "random-32-bytes-base58",
  "timestamp": 1730000000
}
```

The responder replies with its own HELLO.

### 5.4. Nonce

The `nonce` is a random 32-byte value. It is used in AUTH to prevent replay attacks.

### 5.5. AUTH

Both sides sign a challenge derived from both nonces:

```
challenge = BLAKE3(initiator_nonce || responder_nonce)
signature = Ed25519_sign(privkey, challenge)
```

The AUTH message contains:

```json
{
  "type": "auth",
  "peer_id": "Qm...",
  "signature": "ed25519:...",
  "timestamp": 1730000000
}
```

### 5.6. AUTH verification

Each side:

1. Reconstructs the challenge.
2. Verifies the signature against the peer's public key (derived from peer_id).
3. Checks that the peer_id matches the claimed identity.

If verification fails, the connection is closed.

### 5.7. READY

After AUTH, both sides send READY:

```json
{
  "type": "ready",
  "head": "blake3:...",
  "height": 100000,
  "checkpoint_height": 90000,
  "checkpoint_id": "blake3:...",
  "timestamp": 1730000000
}
```

This tells the peer:

- the current head event ID;
- the current height (number of events);
- the latest checkpoint the node has.

### 5.8. Session established

After READY, the session is established:

- peers can send gossip messages;
- peers can request sync;
- peers can request events.

### 5.9. Handshake timeouts

- HELLO timeout: 10 seconds.
- AUTH timeout: 10 seconds.
- READY timeout: 10 seconds.

If any phase times out, the connection is closed.

### 5.10. Version negotiation

If the peer's protocol version differs:

- if compatible (same MAJOR), proceed;
- if incompatible (different MAJOR), close.

Versions are defined in [events.md](./events.md#6-versioning).

### 5.11. Ledger ID check

If the peer's `ledger_id` differs from ours:

- close the connection (different ledgers);
- unless the node is configured for federation (see [consensus.md](./consensus.md#11-federation)).

### 5.12. Capability negotiation

Capabilities are exchanged as a list of strings:

| Capability | Meaning |
|---|---|
| `full` | Full node, stores all events. |
| `archive` | Archive node, stores full history. |
| `light` | Light node, headers only. |
| `validator` | Validator, signs checkpoints. |
| `gossip` | Participates in gossip. |
| `pex` | Supports peer exchange. |
| `dht` | Participates in DHT. |
| `privacy` | Supports privacy mode. |
| `compute` | Serves compute tasks. |

A node **MUST** only request services the peer supports.

### 5.13. Duplicate connections

If two nodes connect to each other simultaneously, one connection **MUST** be closed.

Rule: the connection with the **higher peer ID** is kept.

This prevents duplicate connections.

### 5.14. Reconnection

If a connection is lost, the node **SHOULD** attempt to reconnect with exponential backoff:

- 1s, 2s, 4s, 8s, ..., up to 60s.
- After 10 failed attempts, stop for 1 hour.

### 5.15. Persistent peers

Nodes **MAY** mark certain peers as "persistent":

- always reconnect;
- never disconnect voluntarily.

Useful for bootstrap nodes, validators, and trusted peers.

---

## 6. Message Types

### 6.1. Message categories

| Category | Purpose | Direction |
|---|---|---|
| **Control** | Handshake, keepalive, disconnect | Bidirectional |
| **Gossip** | Event propagation | Bidirectional |
| **Sync** | Historical event fetch | Request/response |
| **Checkpoint** | Checkpoint propagation | Bidirectional |
| **PEX** | Peer discovery | Bidirectional |
| **Compute** | Compute task exchange | Bidirectional |

### 6.2. Control messages

| Message | Purpose |
|---|---|
| `hello` | Initiate connection |
| `auth` | Authenticate |
| `ready` | Confirm session |
| `ping` | Keepalive |
| `pong` | Keepalive response |
| `disconnect` | Graceful disconnect |
| `error` | Error report |

### 6.3. Gossip messages

| Message | Purpose |
|---|---|
| `gossip.event` | Announce a new event |
| `gossip.checkpoint` | Announce a new checkpoint |
| `gossip.attestation` | Announce a new attestation (priority) |

### 6.4. Sync messages

| Message | Purpose |
|---|---|
| `sync.headers.request` | Request headers |
| `sync.headers.response` | Provide headers |
| `sync.events.request` | Request events by ID |
| `sync.events.response` | Provide events |
| `sync.checkpoint.request` | Request a checkpoint |
| `sync.checkpoint.response` | Provide a checkpoint |
| `sync.state.request` | Request state proof (light clients) |
| `sync.state.response` | Provide state proof |

### 6.5. PEX messages

| Message | Purpose |
|---|---|
| `pex.request` | Request peer list |
| `pex.response` | Provide peer list |
| `peer.announce` | Announce self |

### 6.6. Compute messages

Compute messages are defined in [compute.md](./compute.md).

### 6.7. Message envelope

All messages have a common envelope:

```json
{
  "type": "gossip.event",
  "id": "blake3:...",
  "timestamp": 1730000000,
  "payload": { ... }
}
```

The `id` is unique per message, used for deduplication.

### 6.8. Message size

- Control messages: < 1 KB.
- Gossip messages: < 100 KB (event-sized).
- Sync responses: < 1 MB (batched).
- PEX messages: < 10 KB.

Messages exceeding the limit **MUST** be rejected.

### 6.9. Message encoding

Messages **MUST** be encoded in:

- **CBOR** for binary efficiency; or
- **JSON** for debugging (optional).

The encoding is negotiated in the handshake. Default: CBOR.

### 6.10. Message framing

For stream transports (TCP):

- 4-byte length prefix (big-endian);
- then the encoded message.

For message transports (QUIC, WebSocket):

- native framing.

---

## 7. Gossip Protocol

### 7.1. Purpose

Gossip propagates new events to the network quickly, without central coordination.

### 7.2. Push model

When a node receives a new event (from a peer, from a user, from a validator), it:

1. Validates the event.
2. Stores it in the ledger.
3. Announces it to its peers via `gossip.event`.

Peers that have not seen the event:

1. Validate it.
2. Store it.
3. Announce it to their peers.

This is the **push** phase.

### 7.3. Gossip announcement

```json
{
  "type": "gossip.event",
  "event_id": "blake3:...",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "type_hint": "contribution.create",
  "payload_size": 512
}
```

The announcement contains:

- the event ID;
- the author (for routing);
- the timestamp;
- a type hint;
- the payload size.

It does **not** contain the full event (to avoid sending large payloads to uninterested peers).

### 7.4. Fetching the event

A peer that does not have the event requests it via `sync.events.request`:

```json
{
  "type": "sync.events.request",
  "ids": ["blake3:...", "blake3:..."]
}
```

The responding peer sends the events:

```json
{
  "type": "sync.events.response",
  "events": [
    {"id": "blake3:...", "envelope": {...}, "signature": "..."},
    ...
  ]
}
```

### 7.5. Push vs. pull trade-off

- **Push (announcement):** fast, low bandwidth, but requires pull for the actual event.
- **Full push:** sends the event immediately, faster but more bandwidth.
- **Hybrid:** send small events inline, announce large events.

CL uses **hybrid**:

- events < 1 KB: sent inline in the gossip message;
- events ≥ 1 KB: announced, then pulled.

### 7.6. Gossip fanout

A node **MUST NOT** send the same event to all peers at once. Instead:

- send to a random subset (fanout = 3–6);
- each peer, in turn, sends to its own subset.

This is **epidemic** propagation.

### 7.7. Deduplication

A node **MUST** track which events it has already gossiped (per event ID) to avoid resending.

Cache size: 10 000 recent IDs (LRU).

### 7.8. Gossip intervals

- **Push interval:** 100 ms–1 s.
- **Batching:** multiple events per gossip message.

Nodes **MAY** batch up to 100 events per message.

### 7.9. Priority gossip

Some events are high priority:

- checkpoints;
- validator changes;
- rule changes;
- attestations for Level 2+ identities.

These **SHOULD** be gossiped immediately (not batched).

### 7.10. Gossip for checkpoints

Checkpoints are gossiped via `gossip.checkpoint`:

```json
{
  "type": "gossip.checkpoint",
  "checkpoint_id": "blake3:...",
  "height": 100000,
  "signatures_count": 5
}
```

Peers request the full checkpoint if needed.

### 7.11. Anti-entropy

Gossip alone is not sufficient: messages can be lost. **Anti-entropy** ensures consistency:

- periodically, nodes exchange **Merkle roots** of their event sets;
- differences are identified;
- missing events are fetched.

Anti-entropy runs every 5 minutes (or configurable).

### 7.12. Anti-entropy protocol

```
Node A                    Node B
   |                         |
   |--- MERKLE_ROOT ------->|
   |<-- MERKLE_ROOT --------|
   |                         |
   |  (if different)         |
   |                         |
   |--- REQUEST_KEYS ------>|
   |<-- KEYS ---------------|
   |                         |
   |  (find differences)     |
   |                         |
   |--- REQUEST_EVENTS ---->|
   |<-- EVENTS -------------|
```

### 7.13. Merkle root exchange

Each node computes a Merkle root over its event IDs (see [ledger.md](./ledger.md#44-event-tree)).

If roots differ, the nodes exchange **key ranges** (via a Merkle tree traversal) to find missing events.

This is similar to:

- Bitcoin's `getblocks`;
- Cassandra's Merkle tree repair;
- IPFS's bitswap.

### 7.14. Orphan gossip

If a node receives an event whose parents are missing, it:

1. Holds the event in the orphan pool.
2. Requests parents via `sync.events.request`.
3. Once parents arrive, processes the orphan.

Orphans are propagated via gossip like normal events.

### 7.15. Gossip for federated ledgers

For federated ledgers, gossip **MAY** span ledgers:

- events are tagged with a `ledger_id`;
- peers filter by ledger;
- cross-ledger events are gossiped only to peers interested in both ledgers.

---

## 8. Header Exchange

### 8.1. Purpose

Headers are compact representations of events. Header exchange allows:

- fast sync (verify chain of headers before fetching events);
- light client support;
- peer comparison (who has what).

### 8.2. Header structure

A header is a compact event representation:

```json
{
  "id": "blake3:...",
  "type": "contribution.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:...", "blake3:..."],
  "payload_size": 512,
  "payload_root": "blake3:..."
}
```

The `payload_root` is a BLAKE3 hash of the canonical CBOR payload. This allows verifying the payload separately.

### 8.3. Header size

Typical: 100–200 bytes per header.

For 1 million events: ~150 MB of headers.

### 8.4. Header request

```json
{
  "type": "sync.headers.request",
  "from_height": 90000,
  "to_height": 100000,
  "max_count": 2000
}
```

- `from_height`: start of the range (inclusive).
- `to_height`: end of the range (inclusive).
- `max_count`: max headers to return.

### 8.5. Header response

```json
{
  "type": "sync.headers.response",
  "headers": [
    {"id": "blake3:...", "type": "...", "author": "...", "created_at": ..., "parents": [...], "payload_root": "..."},
    ...
  ],
  "has_more": true
}
```

If `has_more` is true, the requester sends another request for the next range.

### 8.6. Header verification

A node **MUST** verify:

- each header's `id` matches the hash of its canonical form;
- the parent references are valid;
- the headers are connected (no gaps).

If a gap is found, the node requests the missing headers.

### 8.7. Header-first sync

To sync from scratch:

1. Request headers from height 0 to latest.
2. Verify the chain of headers.
3. Identify which events are missing (by comparing `payload_root`).
4. Request missing events in batches.

This is much faster than fetching all events.

### 8.8. Headers in gossip

Headers **MAY** be gossiped instead of full events for large payloads. The receiver then fetches the event if interested.

### 8.9. Header storage

Light nodes store **only** headers + checkpoints. Full nodes store everything.

A light node's storage: ~150 MB per 1M events.

### 8.10. Header compression

Headers **MAY** be compressed (zstd) for transmission. Typical compression: 3–5×.

---

## 9. Event Propagation

### 9.1. Flow

When an event is created:

1. **Local node** validates and stores it.
2. **Local node** gossips it to peers (fanout).
3. **Peers** validate, store, and gossip it.
4. **Anti-entropy** ensures consistency.

### 9.2. Latency

Target: propagation to 90% of nodes within 5 seconds.

Achieved by:

- fanout of 3–6;
- fast gossip intervals;
- priority for critical events.

### 9.3. Bandwidth

For a network of N nodes, each event is transmitted:

- ~O(log N) times (epidemic propagation);
- ~O(1) times per node.

For 1000 nodes, ~10 transmissions per event.

### 9.4. Event creation

A user creates an event via a node's API (see [api.md](./api.md)).

The node:

1. Validates the event.
2. Stores it locally.
3. Gossips it to peers.
4. If the node is a validator, it may sign a checkpoint.

### 9.5. Event submission

A user **MAY** submit an event to any node. The node **MAY** reject it if:

- the event is invalid;
- the node is at capacity;
- the user is rate-limited.

### 9.6. Event finality

An event is **final** when included in a finalized checkpoint.

Until then, it is **pending**.

Pending events are gossiped and stored but **MAY** be reverted if they conflict with finalized events.

### 9.7. Event gossip priorities

| Event type | Priority |
|---|---|
| `checkpoint` | Critical |
| `validator.add/remove` | Critical |
| `rule.change` | Critical |
| `identity.create` | High |
| `contribution.create` | Normal |
| `contribution.confirm` | Normal |
| `vote.cast` | High |
| `bounty.*` | Normal |
| `compute.task.*` | Normal |

Critical events are gossiped immediately. Normal events are batched.

### 9.8. Event filtering

Nodes **MAY** filter events:

- by context (only interested in some);
- by author (subscriptions);
- by type (e.g., only checkpoints).

Filtering reduces bandwidth but can cause inconsistency.

### 9.9. Event relay

A node **MUST** relay events it accepts, even if it is not interested in them.

This ensures network-wide propagation.

### 9.10. Event drop

If a node cannot process an event (e.g., orphan with missing parents), it:

1. Holds it in a temporary pool.
2. Requests missing parents.
3. If parents do not arrive within timeout (e.g., 5 minutes), drops the event.

---

## 10. Sync Strategies

### 10.1. Overview

A node can sync via:

1. **From genesis** — fetch all events from the beginning.
2. **From checkpoint** — bootstrap from a checkpoint, then sync forward.
3. **Incremental** — fetch only events after the last known height.
4. **Light sync** — fetch headers + checkpoints only.
5. **Selective sync** — fetch only events in a specific context.

### 10.2. Sync from genesis

Slowest but most secure:

1. Request headers from height 0.
2. Verify the chain.
3. Request events in batches.
4. Verify each event.
5. Compute state.

Time: hours to days for large ledgers.

### 10.3. Sync from checkpoint

Fastest for new nodes:

1. Request the latest finalized checkpoint.
2. Verify its signatures.
3. Optionally fetch the state (or recompute).
4. Request events after the checkpoint height.
5. Verify and apply.

Time: minutes for large ledgers.

**Trade-off:** trust in the checkpoint signatures (assumes honest validators).

### 10.4. Incremental sync

For nodes that are online but behind:

1. Request headers from local height to peer's height.
2. Request missing events.
3. Apply.

Time: seconds to minutes.

### 10.5. Light sync

For light nodes:

1. Request headers from height 0 (or checkpoint).
2. Request the latest checkpoint.
3. Store headers + checkpoint.
4. Request proofs on demand.

Time: minutes.

### 10.6. Selective sync

For nodes interested in one context:

1. Request events in that context.
2. Skip other events.
3. Store only relevant events + headers.

**Warning:** selective sync may cause the node to miss parent events. Fallback to full sync for parents.

### 10.7. Sync negotiation

When two peers connect, they compare:

- their heights;
- their checkpoint heights;
- their heads.

The peer with the higher height serves the peer with the lower.

### 10.8. Sync protocol

```
Node A (behind)           Node B (ahead)
   |                         |
   |--- READY (height=90000) ->|
   |<-- READY (height=100000)-|
   |                         |
   |--- HEADERS_REQ (90000-100000) ->|
   |<-- HEADERS_RESP -------|
   |                         |
   |--- EVENTS_REQ (ids) -->|
   |<-- EVENTS_RESP --------|
   |                         |
   |  (apply, verify)        |
```

### 10.9. Sync batching

Requests are batched:

- headers: 2000 per request;
- events: 100 per request.

Larger batches = faster sync but more memory.

### 10.10. Sync parallelization

A node **MAY** sync from multiple peers in parallel:

- different ranges from different peers;
- verify all;
- detect discrepancies.

Parallel sync is faster but more complex.

### 10.11. Sync verification

Every event received **MUST** be verified before storing:

- signature;
- parents;
- type-specific rules;
- connection to genesis.

Invalid events **MUST** be dropped and the peer penalized.

### 10.12. Sync progress

A node **SHOULD** report sync progress:

```json
{
  "syncing": true,
  "current_height": 95000,
  "target_height": 100000,
  "eta_seconds": 120
}
```

### 10.13. Sync failure

If sync fails (peer disconnects, invalid events), the node:

- retries with another peer;
- reduces peer score for the failing peer;
- falls back to a slower but more reliable strategy.

### 10.14. Bootstrap sequence

A new node:

1. Loads bootstrap nodes.
2. Connects to 2–4.
3. Handshake.
4. Requests latest checkpoint.
5. Verifies checkpoint.
6. Requests headers from checkpoint height.
7. Requests events after checkpoint.
8. Applies events.
9. Joins gossip.

This is the standard bootstrap sequence.

---

## 11. Orphan Handling

### 11.1. Definition

An **orphan** is an event whose parents are not yet known to the node.

### 11.2. Orphan pool

A node **MUST** maintain an orphan pool:

- max size: 1000 events (configurable);
- eviction: LRU;
- timeout: 5 minutes.

### 11.3. Orphan detection

When a node receives an event:

1. Verify the signature.
2. Check that all parents exist.
3. If any parent is missing, the event is an orphan.

### 11.4. Orphan request

When a node detects an orphan:

1. Add it to the orphan pool.
2. Request the missing parents via `sync.events.request`.

### 11.5. Orphan resolution

When the missing parents arrive:

1. Remove the orphan from the pool.
2. Process it normally.
3. Gossip it (if valid).

### 11.6. Orphan cascade

If a missing parent is itself an orphan (its parents are missing), the node recursively requests.

This creates a cascade of requests, eventually resolving to genesis or to known events.

### 11.7. Orphan timeout

If parents do not arrive within 5 minutes, the orphan is dropped.

If the parents arrive later, the event is re-requested.

### 11.8. Orphan flooding

An attacker **MAY** flood the network with orphans (events whose parents do not exist).

Mitigations:

- limit orphan pool size;
- rate limit orphan requests per peer;
- validate signatures before adding to pool;
- score peers who send many orphans.

### 11.9. Orphan gossip

Orphans **MAY** be gossiped, but with lower priority than normal events.

This helps other nodes that may have the parents.

### 11.10. Orphan state

Orphans **MUST NOT** affect state until their parents arrive and they are processed.

---

## 12. Conflict Resolution

### 12.1. Conflicts

A **conflict** is when two events are incompatible:

- two `identity.create` for the same DID;
- two `contribution.revoke` and `contribution.unrevoke` in parallel branches;
- two `vote.cast` from the same identity.

### 12.2. Detection

A node detects a conflict when:

- it receives an event that contradicts an existing event;
- both events are in the DAG (possibly in different branches).

### 12.3. Resolution rules

Conflicts are resolved by:

1. **DAG order.** The event that appears earlier in topological order wins.
2. **Canonical order.** If events are incomparable, the one with the smaller `created_at` wins. If equal, the smaller ID wins.
3. **Validator decision.** If events are finalized in conflicting checkpoints, the community decides.

### 12.4. Example: conflicting contributions

Alice creates two `contribution.create` events for the same work (double-counting).

Resolution:

- both are stored;
- both are visible in the ledger;
- but only one counts for CU (the first by canonical order);
- the second is flagged as a duplicate.

### 12.5. Example: conflicting votes

Alice casts two votes in the same vote.

Resolution:

- both are stored;
- only the first (by canonical order) counts;
- the second is ignored.

### 12.6. Example: conflicting checkpoints

Two checkpoints at the same height have different roots.

Resolution:

- it's a fork;
- see [consensus.md](./consensus.md#10-forks);
- nodes follow the fork with more signatures.

### 12.7. Conflict propagation

Conflicts are propagated via gossip like normal events. Nodes process them and apply resolution rules.

### 12.8. Conflict logging

A node **SHOULD** log conflicts for debugging:

- event IDs;
- resolution applied;
- peer that sent the conflicting event.

### 12.9. Conflict and finality

Once an event is finalized (in a checkpoint), it cannot be reverted. If a conflicting event appears after finalization, it is rejected.

### 12.10. Conflict prevention

Clients **SHOULD** prevent conflicts:

- check the ledger before creating an event;
- use unique IDs for one-time events;
- follow the DAG head.

### 12.11. Conflict and network partition

If the network is partitioned:

- each partition may create conflicting events;
- on reconnection, conflicts are detected and resolved;
- if finality was reached in both partitions, it's a fork.

### 12.12. Conflict resolution and reputation

If a conflict involves a contribution:

- the valid contribution earns CU;
- the invalid one is ignored (or flagged as spam, resulting in reputation penalty).

---

## 13. Checkpoint Sync

### 13.1. Purpose

Checkpoints allow fast sync without fetching all events.

### 13.2. Checkpoint sync protocol

```
Node A (new)              Node B (full)
   |                         |
   |--- CHECKPOINT_REQ ---->|
   |<-- CHECKPOINT_RESP ----|
   |                         |
   |  (verify signatures)    |
   |                         |
   |--- HEADERS_REQ (from checkpoint) ->|
   |<-- HEADERS_RESP -------|
   |                         |
   |--- EVENTS_REQ -------->|
   |<-- EVENTS_RESP --------|
```

### 13.3. Checkpoint request

```json
{
  "type": "sync.checkpoint.request",
  "latest": true
}
```

Or with a specific height:

```json
{
  "type": "sync.checkpoint.request",
  "height": 100000
}
```

### 13.4. Checkpoint response

```json
{
  "type": "sync.checkpoint.response",
  "checkpoint": {
    "id": "blake3:...",
    "height": 100000,
    "event_root": "blake3:...",
    "state_root": "blake3:...",
    "signatures": [...]
  }
}
```

### 13.5. Checkpoint verification

The receiving node **MUST**:

1. Verify the checkpoint ID matches the canonical form.
2. Verify the validator signatures against the known validator set.
3. Verify the threshold is met.
4. Optionally, verify the roots (if the node has the events).

### 13.6. State fetch

After verifying the checkpoint, the node **MAY** fetch the state:

```json
{
  "type": "sync.state.request",
  "height": 100000
}
```

The response contains the state (or a proof).

**Note:** fetching state is optional. The node can recompute it from events.

### 13.7. State proof

For light nodes, the response contains a **Merkle proof** for specific state entries:

```json
{
  "type": "sync.state.response",
  "height": 100000,
  "proof": [...],
  "root": "blake3:..."
}
```

### 13.8. Checkpoint sync from multiple peers

A node **MAY** fetch the same checkpoint from multiple peers to detect discrepancies.

If two peers provide different checkpoints at the same height, it's a fork.

### 13.9. Trust in checkpoints

Syncing from a checkpoint means trusting:

- the validator set (that it was honest);
- the checkpoint signatures (that they are valid).

This is the standard trust model for light clients.

### 13.10. Checkpoint and privacy

Fetching checkpoints leaks less metadata than fetching all events.

This is beneficial for privacy-focused nodes.

---

## 14. Light Client Sync

### 14.1. Purpose

Light clients sync with minimal storage and bandwidth.

### 14.2. Storage

A light client stores:

- headers (all or recent);
- latest checkpoint;
- peer list;
- (optional) state proofs for subscribed queries.

### 14.3. Sync protocol

1. Connect to peers.
2. Fetch latest checkpoint.
3. Verify.
4. Fetch headers from checkpoint height to latest.
5. Verify headers.
6. Join gossip (receive `gossip.event` for new events).
7. On demand, request proofs for specific queries.

### 14.4. Proof requests

A light client requests proofs from full nodes:

```json
{
  "type": "sync.state.request",
  "context": "repo:x/y",
  "did": "did:cl:main:alice",
  "height": 100000
}
```

The full node responds with a Merkle proof.

### 14.5. Proof verification

The light client verifies the proof against its latest checkpoint's `state_root`.

If the proof is valid, the client trusts the value.

### 14.6. Trust assumptions

Light clients trust:

- the checkpoint signatures (validators);
- the state proofs (cryptographic).

They do **not** trust individual full nodes.

### 14.7. Light client for mobile

Light client sync is ideal for mobile:

- small storage;
- low bandwidth;
- fast sync.

### 14.8. Light client for embedded devices

For very constrained devices, even light sync may be too heavy.

A "nano client" **MAY** store:

- only the latest checkpoint;
- no headers.

Query proofs are then against a single checkpoint.

### 14.9. Light client limitations

Light clients **cannot**:

- serve as validators;
- serve proofs to others;
- fully verify historical state.

They **can**:

- verify current state;
- submit events (via full nodes);
- vote (if they can prove reputation).

---

## 15. Anti-Spam and Rate Limiting

### 15.1. Purpose

Prevent abuse:

- spam events;
- message flooding;
- resource exhaustion.

### 15.2. Rate limits

Per peer:

| Resource | Limit |
|---|---|
| Messages/sec | 100 |
| Events/sec | 50 |
| Headers/sec | 500 |
| Bandwidth | 1 MB/s |
| Orphan events | 100 |

Limits are configurable but **MUST** have defaults.

### 15.3. Rate limit enforcement

A node **MUST** track per-peer message rates. If a peer exceeds the limit:

1. Drop the excess messages.
2. Warn the peer (optional).
3. Disconnect after repeated violations.

### 15.4. Peer scoring for spam

Spam violations reduce peer score. Low-score peers are disconnected and banned.

### 15.5. Event validation cost

Some events are expensive to validate (e.g., large payloads, complex signatures).

Nodes **MAY**:

- limit the size of events accepted from a peer;
- require a small proof-of-work for large events (optional);
- prioritize small events.

### 15.6. Sybil resistance

Rate limits per IP **MAY** be enforced to prevent Sybil attacks:

- max 5 connections per IP;
- max 10 messages/sec per IP.

### 15.7. Ban list

A node **SHOULD** maintain a ban list of peers that:

- repeatedly violate rate limits;
- send invalid events;
- attempt Sybil attacks.

Bans **MAY** be shared via PEX (opt-in).

### 15.8. Denial of service

If a node is under DoS:

- reduce peer count;
- increase rate limits;
- use a proxy or CDN;
- switch to privacy mode (Tor).

### 15.9. Invalid event penalty

Sending invalid events reduces peer score. Repeated invalid events lead to disconnection.

### 15.10. Orphan penalty

Sending many orphans (events with missing parents) reduces peer score.

---

## 16. Privacy Considerations

### 16.1. Metadata leakage

Sync leaks metadata:

- which events a node requests;
- which peers it connects to;
- which contexts it is interested in.

### 16.2. Privacy modes

Nodes **MAY** enable privacy modes:

- **Tor/I2P** transport;
- **relay** through intermediaries;
- **dummy traffic** (random requests);
- **blinded subscriptions**.

### 16.3. Tor/I2P

Sync over Tor:

- connect to peers via `.onion` addresses;
- use Tor circuits;
- hide IP addresses.

Latency: 2–5× slower than clearnet.

### 16.4. Relays

Privacy-preserving relays:

- forward messages without knowing the sender;
- use mixing or onion routing.

Relays are an optional feature.

### 16.5. Dummy traffic

A node **MAY** send dummy requests to obscure its real interests.

Dummy traffic must be indistinguishable from real traffic.

### 16.6. Blinded subscriptions

A node **MAY** subscribe to a filter (e.g., "all events in context X") without revealing X:

- use Bloom filters or prefix filters;
- combine multiple filters to hide individual interests.

### 16.7. Sync privacy trade-offs

Privacy sync is slower and more complex. Most nodes use default sync.

### 16.8. Peer anonymity

Peers **MAY** be anonymous:

- no requirement to reveal identity;
- peer ID is a random public key.

But: validators **MUST** be identifiable (see [consensus.md](./consensus.md#4-validator-model)).

### 16.9. Privacy for validators

Validators are public. Their sync traffic is visible.

To reduce risk:

- use dedicated infrastructure;
- separate sync from validator signing;
- use relays.

---

## 17. Validation Rules

Nodes **MUST** enforce these rules for sync.

### 17.1. Handshake

- HELLO **MUST** include protocol version, ledger ID, peer ID.
- AUTH **MUST** verify the peer's signature.
- READY **MUST** include the current head.

### 17.2. Messages

- Every message **MUST** have a `type` and `id`.
- Messages **MUST** be under the size limit.
- Messages **MUST** be encoded in the negotiated format.

### 17.3. Gossip

- Gossip announcements **MUST** have a valid event ID.
- Events received via gossip **MUST** be verified.
- The same event **MUST NOT** be gossiped twice by the same node.

### 17.4. Headers

- Headers **MUST** match the corresponding event's canonical form.
- Header ranges **MUST** be contiguous (no gaps).

### 17.5. Sync

- Sync requests **MUST** specify a valid range.
- Sync responses **MUST** contain valid events.
- Invalid events in a response **MUST** cause the peer to be penalized.

### 17.6. Orphans

- Orphans **MUST** have valid signatures.
- Orphan pool **MUST** be bounded.
- Orphans **MUST** be dropped after timeout.

### 17.7. Conflicts

- Conflicts **MUST** be resolved deterministically.
- Conflicting events **MUST NOT** both count for state.

### 17.8. Rate limits

- Rate limits **MUST** be enforced per peer.
- Violations **MUST** reduce peer score.

### 17.9. Privacy

- Privacy modes **MUST NOT** compromise sync correctness.
- Dummy traffic **MUST NOT** overwhelm the network.

---

## 18. Examples

### 18.1. New node bootstrap

**Step 1: Connect to bootstrap.**

```
new node → bootstrap1: HELLO
bootstrap1 → new node: HELLO
new node → bootstrap1: AUTH
bootstrap1 → new node: AUTH
new node → bootstrap1: READY (height=0)
bootstrap1 → new node: READY (height=100000)
```

**Step 2: Fetch checkpoint.**

```
new node → bootstrap1: sync.checkpoint.request {latest: true}
bootstrap1 → new node: sync.checkpoint.response {height: 90000, ...}
```

**Step 3: Fetch headers.**

```
new node → bootstrap1: sync.headers.request {from: 90000, to: 100000}
bootstrap1 → new node: sync.headers.response {headers: [...], has_more: false}
```

**Step 4: Fetch events.**

```
new node → bootstrap1: sync.events.request {ids: [...]}
bootstrap1 → new node: sync.events.response {events: [...]}
```

**Step 5: Join gossip.**

```
new node → peers: peer.announce {addr: ..., capabilities: [...]}
peers → new node: gossip.event {event_id: ..., ...}
```

### 18.2. Event propagation

Alice creates a `contribution.create` event on Node A.

1. Node A validates and stores.
2. Node A gossips to peers B, C, D.
3. B gossips to E, F, G.
4. C gossips to H, I.
5. Within seconds, all nodes have the event.

### 18.3. Anti-entropy

Nodes A and B have diverged.

1. A sends MERKLE_ROOT.
2. B sends its MERKLE_ROOT.
3. Roots differ.
4. A and B exchange key ranges.
5. A requests missing events from B.
6. B requests missing events from A.
7. Both converge.

### 18.4. Orphan resolution

Node A receives event E whose parent P is unknown.

1. A adds E to orphan pool.
2. A requests P from peers.
3. Peer B sends P.
4. A processes P.
5. A processes E.

### 18.5. Conflict resolution

Node A receives two `vote.cast` events from Alice for the same vote.

1. A detects the conflict.
2. A applies canonical order: the earlier event wins.
3. A marks the second as ignored.

### 18.6. Checkpoint sync

Node A (new) connects to Node B (full).

1. A requests latest checkpoint.
2. B sends checkpoint at height 100000.
3. A verifies the checkpoint signatures.
4. A fetches headers from 100000 forward.
5. A fetches events.
6. A is operational.

### 18.7. Light client

Mobile node M connects to full node F.

1. M requests checkpoint.
2. F sends checkpoint.
3. M verifies.
4. M requests headers.
5. M requests proof for "Alice's reputation in context X".
6. F sends Merkle proof.
7. M verifies against checkpoint.

### 18.8. Privacy mode

Node P connects to peers via Tor.

1. P connects to `.onion` addresses.
2. P sends/receives via Tor circuits.
3. IP is hidden.

Latency: 2–5× slower.

---

## 19. Test Vectors

Test vectors for sync live in `spec/test-vectors/sync.json`.

### 19.1. Coverage

- Handshake (valid and invalid).
- Gossip message construction.
- Header construction and verification.
- Merkle root exchange.
- Orphan resolution.
- Conflict resolution.
- Checkpoint sync.
- Light client proofs.
- Rate limit enforcement.

### 19.2. Format

```json
{
  "description": "Valid handshake",
  "messages": [
    {"type": "hello", "protocol_version": 1, "ledger_id": "...", ...},
    {"type": "hello", "protocol_version": 1, "ledger_id": "...", ...},
    {"type": "auth", "peer_id": "...", "signature": "...", ...},
    ...
  ],
  "expected": "session_established"
}
```

### 19.3. Determinism

All messages **MUST** be deterministic given the same inputs.

Test vectors verify:

- handshake signatures;
- event IDs;
- header hashes;
- Merkle roots.

### 19.4. Cross-implementation

Test vectors **MUST** pass on at least two implementations before v1.0.

---

## 20. Open Questions

- What is the optimal **peer count** for different node types?
- How to handle **NAT traversal** without a central STUN server?
- Should sync use **libp2p** or a custom protocol?
- How to handle **very large events** (e.g., datasets)?
- Should there be a **sync fee** (to prevent leeching)?
- How to balance **privacy** and **performance**?
- Should there be a **relay incentive** (payment for relays)?
- How to handle **cross-ledger sync** efficiently?
- Should light clients **trust checkpoints** by default?
- How to prevent **eclipse attacks** (isolating a node from honest peers)?
- What is the **maximum message size**?
- Should there be **compression** for gossip?
- How to handle **mobile/roaming peers**?
- Should there be **fast sync from multiple peers** by default?
- How to handle **network partitions** without central coordination?

These will be resolved through RFCs and community discussion.

---

## Summary

**Sync is:**

- Peer-to-peer.
- Push + pull.
- Header-first.
- Idempotent.
- Privacy-aware.
- Federated.

**Peer discovery:**

- Bootstrap nodes.
- PEX.
- DHT.
- Gossip announcements.
- Manual configuration.

**Handshake:**

- HELLO → AUTH → READY → SESSION.
- Verifies peer ID, ledger ID, version.

**Message types:**

- Control (hello, auth, ping).
- Gossip (event, checkpoint).
- Sync (headers, events, state).
- PEX.
- Compute.

**Gossip:**

- Push announcements.
- Fanout 3–6.
- Deduplication cache.
- Anti-entropy every 5 min.

**Sync strategies:**

- From genesis.
- From checkpoint.
- Incremental.
- Light.
- Selective.

**Orphans:**

- Held in pool.
- Parents requested.
- Dropped after timeout.

**Conflicts:**

- Resolved by canonical order.
- Or by fork (checkpoints).

**Light clients:**

- Headers + checkpoints.
- Proofs on demand.
- Ideal for mobile.

**Anti-spam:**

- Rate limits per peer.
- Peer scoring.
- Ban list.
- Sybil resistance.

**Privacy:**

- Tor/I2P.
- Relays.
- Dummy traffic.
- Blinded subscriptions.

**Key insight:**

Sync is **epidemic**, not coordinated. The network converges on the same set of events through simple local rules. No central scheduler, no global clock. Just peers talking to peers.

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [ledger.md](./ledger.md) — DAG, Merkle, checkpoints.
- [consensus.md](./consensus.md) — finalization, federation.
- [api.md](./api.md) — REST, WebSocket, gRPC.
- [compute.md](./compute.md) — compute messages.
- [privacy.md](./privacy.md) — privacy modes.
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
