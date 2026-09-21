# API

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md) · [identity.md](./identity.md) · [contribution.md](./contribution.md) · [reputation.md](./reputation.md) · [ledger.md](./ledger.md) · [consensus.md](./consensus.md) · [sync.md](./sync.md) · [bounty.md](./bounty.md) · [vote.md](./vote.md) · [compute.md](./compute.md)  
**Related:** [privacy.md](./privacy.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [Transport and Encoding](#3-transport-and-encoding)
4. [Authentication](#4-authentication)
5. [Error Model](#5-error-model)
6. [Rate Limiting](#6-rate-limiting)
7. [REST API](#7-rest-api)
8. [WebSocket API](#8-websocket-api)
9. [gRPC API](#9-grpc-api)
10. [Event Submission](#10-event-submission)
11. [Queries](#11-queries)
12. [Subscriptions](#12-subscriptions)
13. [Bounty and Compute Endpoints](#13-bounty-and-compute-endpoints)
14. [Vote Endpoints](#14-vote-endpoints)
15. [Light Client API](#15-light-client-api)
16. [Node Management API](#16-node-management-api)
17. [Versioning](#17-versioning)
18. [Validation Rules](#18-validation-rules)
19. [Examples](#19-examples)
20. [Test Vectors](#20-test-vectors)
21. [Open Questions](#21-open-questions)

---

## 1. Overview

The **API** is how clients interact with CL nodes. It exposes three interfaces:

- **REST** — synchronous request/response, for simple queries and event submission.
- **WebSocket** — real-time subscriptions, for live updates.
- **gRPC** — high-performance, typed interface, for node-to-node and advanced clients.

The API is **read-mostly**: the ledger is the source of truth, and clients read from it. Writes happen via event submission.

**This file defines:**

- The transport and encoding (Section 3).
- Authentication (Section 4).
- The error model (Section 5).
- Rate limits (Section 6).
- REST endpoints (Section 7).
- WebSocket subscriptions (Section 8).
- gRPC services (Section 9).
- Event submission (Section 10).
- Queries (Section 11).
- Subscriptions (Section 12).
- Bounty, compute, and vote endpoints (Sections 13–14).
- Light client API (Section 15).
- Node management (Section 16).
- Versioning (Section 17).
- Validation rules (Section 18).

The API is the contract between node implementations and clients. Any implementation that follows this spec is compatible.

---

## 2. Design Principles

### 2.1. Events are the API

The API's primary function is to submit events and read state derived from events. There is no "state mutation" endpoint — clients submit events, and state is derived.

### 2.2. Signed by the client

Events are signed by the client's key. The node does not hold private keys on behalf of users (unless the user explicitly delegates to a custodial service).

### 2.3. Read-free, write-signed

- **Reads** (queries) are free and unauthenticated by default.
- **Writes** (event submission) require a valid signature.

This means anyone can read the ledger; only authorized identities can write.

### 2.4. Idempotent writes

Event submission is idempotent by event ID. Submitting the same event twice has no additional effect.

### 2.5. Cursor-based pagination

Queries that return lists **MUST** support cursor-based pagination. Offset-based pagination is not allowed (it breaks under concurrent writes).

### 2.6. Deterministic ordering

All list endpoints return items in a deterministic order (by `created_at`, then by event ID).

### 2.7. Versioned

The API is versioned. Breaking changes require a new version.

### 2.8. Transport-agnostic

REST, WebSocket, and gRPC expose the same logical operations. Clients choose based on their needs.

### 2.9. Privacy-aware

Queries **MUST NOT** require revealing the client's identity. Reads are anonymous by default.

### 2.10. Backpressure

Nodes **MUST** signal backpressure when overloaded:

- HTTP `429 Too Many Requests`;
- WebSocket: `slow_down` message;
- gRPC: `RESOURCE_EXHAUSTED`.

---

## 3. Transport and Encoding

### 3.1. Transports

| Protocol | Default port | Use case |
|---|---|---|
| HTTPS | 443 | REST |
| WSS | 443 | WebSocket |
| gRPC (HTTP/2) | 443 | gRPC |

All transports **MUST** use TLS. Plaintext HTTP is allowed only on localhost for development.

### 3.2. Content types

| Content type | Description |
|---|---|
| `application/json` | JSON (default for REST) |
| `application/cbor` | CBOR (compact, recommended for events) |
| `application/grpc+proto` | gRPC protobuf |

Clients **MAY** negotiate content type via `Accept` header.

### 3.3. JSON encoding

When JSON is used:

- Keys **MUST** be strings.
- Integers **MUST** be JSON numbers (not strings).
- Byte strings **MUST** be Base64-encoded strings with prefix (e.g., `base64:...`).
- DIDs **MUST** be strings.
- Timestamps **MUST** be Unix seconds (integer).

### 3.4. CBOR encoding

For events, CBOR is **RECOMMENDED**:

- smaller payloads;
- deterministic;
- matches the canonical form used for hashing.

When CBOR is used, the media type is `application/cbor`.

### 3.5. Character encoding

All text **MUST** be UTF-8.

### 3.6. Compression

Clients **MAY** request compression via `Accept-Encoding: gzip, zstd`.

Nodes **SHOULD** support at least gzip.

### 3.7. HTTP methods

| Method | Use |
|---|---|
| `GET` | Read-only queries |
| `POST` | Event submission, complex queries |
| `PUT` | Idempotent updates (rare) |
| `DELETE` | Not used (events are append-only) |

### 3.8. Status codes

Standard HTTP status codes:

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created (event accepted) |
| 204 | No content |
| 400 | Bad request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not found |
| 409 | Conflict (duplicate) |
| 422 | Unprocessable entity |
| 429 | Too many requests |
| 500 | Internal error |
| 503 | Service unavailable |

### 3.9. CORS

Nodes serving web clients **MUST** support CORS:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

Configurable by the node operator.

---

## 4. Authentication

### 4.1. Read authentication

Reads **MAY** be anonymous. Nodes **MAY** require authentication for rate-limited reads.

### 4.2. Write authentication

Writes **MUST** be authenticated via event signatures.

The node verifies the event's signature before accepting it. The client does not need a session; the signature is sufficient.

### 4.3. Optional bearer tokens

For convenience (e.g., rate limit attribution), clients **MAY** use bearer tokens:

```
Authorization: Bearer <token>
```

Tokens are issued by the node after a challenge-response with the client's key.

### 4.4. Challenge-response

To obtain a bearer token:

**Step 1:** Client requests a challenge.

```
POST /auth/challenge
{
  "did": "did:cl:main:alice"
}
```

Response:

```
{
  "challenge": "base64:...",
  "expires_at": 1730000600
}
```

**Step 2:** Client signs the challenge.

```
POST /auth/verify
{
  "did": "did:cl:main:alice",
  "challenge": "base64:...",
  "signature": "ed25519:..."
}
```

Response:

```
{
  "token": "base64:...",
  "expires_at": 1730003600
}
```

**Step 3:** Client uses the token in subsequent requests.

### 4.5. Token scope

Tokens **MUST** be scoped:

- read-only;
- write (submit events as the DID);
- admin (node management, if authorized).

### 4.6. Token expiry

Tokens expire (e.g., 1 hour). Clients refresh by repeating challenge-response.

### 4.7. No passwords

CL has no passwords. Authentication is always cryptographic.

### 4.8. Key storage

Clients **MUST** store private keys securely:

- hardware wallets;
- OS keychains;
- encrypted files.

Never in plain text, never in browser localStorage (unless encrypted).

### 4.9. Rate limit attribution

Authenticated clients are rate-limited per DID. Anonymous clients are rate-limited per IP.

### 4.10. Delegated keys

A client **MAY** use a delegated key (see [identity.md](./identity.md)) to sign events on behalf of another identity, if the delegation is recorded on-ledger.

---

## 5. Error Model

### 5.1. Error response

All errors follow the same structure:

```json
{
  "error": {
    "code": "invalid_signature",
    "message": "The signature does not verify.",
    "details": {
      "event_id": "blake3:..."
    },
    "request_id": "req_abc123"
  }
}
```

### 5.2. Fields

| Field | Type | Description |
|---|---|---|
| `code` | string | Machine-readable error code. |
| `message` | string | Human-readable message. |
| `details` | object | Optional context. |
| `request_id` | string | For tracing. |

### 5.3. Error codes

| Code | HTTP | Meaning |
|---|---|---|
| `bad_request` | 400 | Malformed request. |
| `invalid_signature` | 400 | Signature verification failed. |
| `invalid_event` | 400 | Event schema violation. |
| `unknown_type` | 400 | Unknown event type. |
| `unsupported_version` | 400 | Unsupported protocol version. |
| `missing_parent` | 400 | Parent event not found. |
| `unauthorized` | 401 | Authentication required. |
| `forbidden` | 403 | Authenticated but not allowed. |
| `not_found` | 404 | Resource not found. |
| `duplicate` | 409 | Event already exists. |
| `conflict` | 409 | Conflicting event. |
| `unprocessable` | 422 | Semantically invalid. |
| `rate_limited` | 429 | Too many requests. |
| `internal_error` | 500 | Unexpected error. |
| `unavailable` | 503 | Node is overloaded or syncing. |

### 5.4. Error details

Errors **SHOULD** include relevant details:

- `event_id` for event-related errors;
- `missing_parents` for parent errors;
- `required_role` for authorization errors;
- `retry_after` for rate limits.

### 5.5. Retry semantics

- `429` and `503` **SHOULD** be retried with exponential backoff.
- `400`, `401`, `403`, `404`, `422` **MUST NOT** be retried (the request is invalid).
- `409` **MAY** be retried if the conflict is temporal.

### 5.6. Request ID

Every response **SHOULD** include a `X-Request-ID` header (or `request_id` field). Clients **SHOULD** log it for debugging.

### 5.7. Error logging

Nodes **SHOULD** log errors with:

- timestamp;
- request ID;
- error code;
- client ID (if authenticated).

### 5.8. No information leakage

Error messages **MUST NOT** leak:

- private keys;
- internal paths;
- stack traces (in production).

### 5.9. Localization

Error messages **MAY** be localized based on `Accept-Language`.

The `code` field is always in English and stable.

### 5.10. Error stability

Error codes are part of the API contract. Changing a code is a breaking change.

---

## 6. Rate Limiting

### 6.1. Defaults

| Endpoint category | Limit |
|---|---|
| Read (anonymous) | 100 req/min per IP |
| Read (authenticated) | 1000 req/min per DID |
| Write (event submission) | 60 req/min per DID |
| Subscriptions | 10 per connection |
| WebSocket messages | 100/min per connection |

Limits are configurable by the node operator.

### 6.2. Rate limit headers

Responses **MUST** include:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1730000600
```

### 6.3. Exceeded response

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30

{
  "error": {
    "code": "rate_limited",
    "message": "Too many requests. Retry after 30 seconds.",
    "details": {"retry_after": 30}
  }
}
```

### 6.4. Per-DID vs. per-IP

- Anonymous: per IP.
- Authenticated: per DID.
- Multiple IPs behind one DID: still per-DID.

### 6.5. Priority

Some clients (e.g., validators, oracles) **MAY** be given higher limits. The policy is set by the node operator.

### 6.6. Abuse

Repeated rate limit violations **MAY** result in:

- longer backoffs;
- temporary bans;
- permanent bans (in extreme cases).

### 6.7. WebSocket rate limiting

WebSocket connections **MUST** enforce:

- max subscriptions per connection;
- max messages per minute;
- max bytes per minute.

Violations result in connection closure.

### 6.8. gRPC rate limiting

gRPC **MUST** return `RESOURCE_EXHAUSTED` when limits are exceeded.

### 6.9. Bulk operations

Bulk reads (e.g., fetching many events) **MAY** be rate-limited separately. Nodes **SHOULD** offer a bulk endpoint with higher limits but requiring authentication.

### 6.10. No hidden limits

Rate limits **MUST** be documented and included in headers. No silent throttling.

---

## 7. REST API

### 7.1. Base URL

```
https://<node>/api/v1/
```

Versioning is part of the path. `v1` is the current version.

### 7.2. Endpoint categories

| Category | Prefix | Purpose |
|---|---|---|
| Auth | `/auth/` | Authentication. |
| Events | `/events/` | Event submission and retrieval. |
| Identity | `/identity/` | Identity queries. |
| Reputation | `/reputation/` | Reputation queries. |
| Contribution | `/contribution/` | Contribution queries. |
| Bounty | `/bounty/` | Bounty operations. |
| Compute | `/compute/` | Compute task operations. |
| Vote | `/vote/` | Vote operations. |
| Context | `/context/` | Context (community) queries. |
| Validator | `/validator/` | Validator queries. |
| Checkpoint | `/checkpoint/` | Checkpoint queries. |
| Sync | `/sync/` | Sync operations. |
| Admin | `/admin/` | Node management (restricted). |

### 7.3. Events

#### `POST /events`

Submit an event.

**Request:**

```json
{
  "event": {
    "version": 1,
    "type": "contribution.create",
    "author": "did:cl:main:alice",
    "created_at": 1730000000,
    "parents": ["blake3:..."],
    "payload": {...},
    "signature": "ed25519:..."
  }
}
```

Or CBOR-encoded event.

**Response (201):**

```json
{
  "event_id": "blake3:...",
  "status": "accepted",
  "finalized": false
}
```

**Errors:**

- `400 invalid_signature`
- `400 invalid_event`
- `409 duplicate`
- `429 rate_limited`

#### `POST /events/batch`

Submit multiple events atomically.

**Request:**

```json
{
  "events": [
    {...},
    {...}
  ]
}
```

**Response (201):**

```json
{
  "accepted": ["blake3:...", "blake3:..."],
  "rejected": []
}
```

Events in a batch are processed in order. If one fails, subsequent events are rejected (atomicity optional).

#### `GET /events/:id`

Retrieve an event by ID.

**Response (200):**

```json
{
  "event": {...},
  "received_at": 1730000100,
  "finalized": true,
  "finalized_at": 1730000600
}
```

#### `GET /events`

List events with filters.

**Query parameters:**

| Parameter | Type | Description |
|---|---|---|
| `type` | string | Filter by event type. |
| `author` | string | Filter by author DID. |
| `context` | string | Filter by context. |
| `from` | integer | From timestamp (inclusive). |
| `to` | integer | To timestamp (inclusive). |
| `cursor` | string | Pagination cursor. |
| `limit` | integer | Max results (default 100, max 1000). |

**Response (200):**

```json
{
  "events": [...],
  "next_cursor": "base64:...",
  "has_more": true
}
```

### 7.4. Identity

#### `GET /identity/:did`

Get identity information.

**Response (200):**

```json
{
  "did": "did:cl:main:alice",
  "pubkey": "base58:...",
  "created_at": 1730000000,
  "level": 2,
  "deactivated": false,
  "metadata": {
    "display_name": "Alice"
  },
  "attestations": [
    {
      "issuer": "did:cl:org:university",
      "claim": "student",
      "valid_until": 1760000000
    }
  ]
}
```

#### `GET /identity/:did/attestations`

List attestations for an identity.

#### `GET /identity/:did/contributions`

List contributions by an identity.

#### `GET /identity/:did/roles`

List roles for an identity.

### 7.5. Reputation

#### `GET /reputation/:did`

Get reputation across all contexts.

**Response (200):**

```json
{
  "did": "did:cl:main:alice",
  "contexts": {
    "repo:x/y": 150.5,
    "org:mycompany": 320.75
  },
  "total": 471.25
}
```

#### `GET /reputation/:did/:context`

Get reputation in a specific context.

**Response (200):**

```json
{
  "did": "did:cl:main:alice",
  "context": "repo:x/y",
  "reputation": 150.5,
  "level": "trusted",
  "computed_at": 1730000000
}
```

**Query parameters:**

| Parameter | Type | Description |
|---|---|---|
| `at` | integer | Compute at a specific time (default: now). |
| `snapshot` | string | Use a specific snapshot. |

#### `GET /reputation/:did/:context/history`

Get reputation history over time.

### 7.6. Contribution

#### `GET /contribution/:id`

Get a contribution by event ID.

#### `GET /contribution`

List contributions with filters.

**Query parameters:**

| Parameter | Type | Description |
|---|---|---|
| `subject` | string | Filter by subject DID. |
| `issuer` | string | Filter by issuer DID. |
| `context` | string | Filter by context. |
| `action` | string | Filter by action. |
| `confirmed` | boolean | Filter by confirmation status. |
| `revoked` | boolean | Filter by revocation status. |
| `cursor` | string | Pagination cursor. |
| `limit` | integer | Max results. |

### 7.7. Context

#### `GET /context/:id`

Get context information.

**Response (200):**

```json
{
  "id": "repo:x/y",
  "name": "Project X",
  "created_at": 1730000000,
  "rules": {...},
  "rules_version": "blake3:...",
  "validator_count": 7,
  "member_count": 250
}
```

#### `GET /context/:id/rules`

Get the context's current rules.

#### `GET /context/:id/members`

List members of the context.

#### `GET /context/:id/validators`

List validators of the context.

### 7.8. Validator

#### `GET /validator/:did`

Get validator information.

#### `GET /validator`

List validators with filters.

### 7.9. Checkpoint

#### `GET /checkpoint/latest`

Get the latest finalized checkpoint.

**Response (200):**

```json
{
  "id": "blake3:...",
  "height": 100000,
  "depth": 50000,
  "event_root": "blake3:...",
  "state_root": "blake3:...",
  "signatures": [...],
  "created_at": 1730000000
}
```

#### `GET /checkpoint/:height`

Get a checkpoint at a specific height.

#### `GET /checkpoint`

List checkpoints.

### 7.10. Sync

#### `GET /sync/status`

Get node sync status.

**Response (200):**

```json
{
  "syncing": true,
  "current_height": 95000,
  "target_height": 100000,
  "eta_seconds": 120,
  "peers": 12
}
```

#### `GET /sync/peers`

List connected peers.

### 7.11. Node info

#### `GET /node/info`

Get node information.

**Response (200):**

```json
{
  "version": "0.1.0",
  "protocol_version": 1,
  "ledger_id": "blake3:...",
  "peer_id": "Qm...",
  "uptime_seconds": 3600,
  "height": 100000,
  "checkpoint_height": 100000,
  "validator": false
}
```

#### `GET /node/health`

Health check.

**Response (200):**

```json
{
  "status": "healthy",
  "syncing": false
}
```

---

## 8. WebSocket API

### 8.1. Connection

```
wss://<node>/api/v1/ws
```

### 8.2. Message format

All messages are JSON:

```json
{
  "id": "msg_abc123",
  "type": "subscribe",
  "payload": {...}
}
```

Responses:

```json
{
  "id": "msg_abc123",
  "type": "subscribed",
  "payload": {...}
}
```

### 8.3. Message types

| Type | Direction | Purpose |
|---|---|---|
| `subscribe` | Client → Node | Subscribe to a topic. |
| `unsubscribe` | Client → Node | Unsubscribe. |
| `subscribed` | Node → Client | Subscription confirmed. |
| `unsubscribed` | Node → Client | Unsubscription confirmed. |
| `event` | Node → Client | New event notification. |
| `checkpoint` | Node → Client | New checkpoint. |
| `ping` | Both | Keepalive. |
| `pong` | Both | Keepalive response. |
| `error` | Node → Client | Error. |
| `slow_down` | Node → Client | Backpressure. |

### 8.4. Subscriptions

#### Subscribe to events

```json
{
  "id": "sub1",
  "type": "subscribe",
  "payload": {
    "topic": "events",
    "filter": {
      "type": "contribution.create",
      "context": "repo:x/y"
    }
  }
}
```

#### Subscribe to a specific identity

```json
{
  "id": "sub2",
  "type": "subscribe",
  "payload": {
    "topic": "identity",
    "did": "did:cl:main:alice"
  }
}
```

#### Subscribe to checkpoints

```json
{
  "id": "sub3",
  "type": "subscribe",
  "payload": {
    "topic": "checkpoints"
  }
}
```

#### Subscribe to a vote

```json
{
  "id": "sub4",
  "type": "subscribe",
  "payload": {
    "topic": "vote",
    "vote_id": "blake3:..."
  }
}
```

### 8.5. Event notification

When a subscribed event occurs:

```json
{
  "type": "event",
  "subscription": "sub1",
  "payload": {
    "event": {...},
    "received_at": 1730000100
  }
}
```

### 8.6. Checkpoint notification

```json
{
  "type": "checkpoint",
  "subscription": "sub3",
  "payload": {
    "checkpoint": {...}
  }
}
```

### 8.7. Keepalive

Clients **MUST** send `ping` every 30 seconds. Nodes **MUST** respond with `pong`.

If no `ping` is received for 60 seconds, the node **MAY** close the connection.

### 8.8. Backpressure

If a client is slow to consume messages, the node **MAY** send:

```json
{
  "type": "slow_down",
  "payload": {
    "queue_size": 1000
  }
}
```

The client **SHOULD** reduce its subscription scope or disconnect.

### 8.9. Reconnection

Clients **SHOULD** reconnect with exponential backoff.

On reconnect, clients **MUST** re-subscribe and request missed events (via REST, using `from` timestamp).

### 8.10. Authentication

WebSocket connections **MAY** be authenticated:

- via query parameter `?token=...`;
- via `Authorization` header (if supported).

Anonymous connections **MAY** be allowed for read-only subscriptions.

### 8.11. Limits

- Max subscriptions per connection: 10.
- Max event rate: 100/sec per connection.
- Max message size: 1 MB.

### 8.12. Filtering

Filters **MAY** be simple (single field) or complex (AND of conditions).

Complex filters:

```json
{
  "filter": {
    "and": [
      {"type": "contribution.create"},
      {"context": "repo:x/y"},
      {"author": {"in": ["did:cl:main:alice", "did:cl:main:bob"]}}
    ]
  }
}
```

### 8.13. No guaranteed delivery

WebSocket is **at-most-once** delivery. Clients **MUST** reconcile with REST for missed events.

### 8.14. Compression

WebSocket connections **MAY** use `permessage-deflate`.

---

## 9. gRPC API

### 9.1. Purpose

gRPC provides:

- typed interface (protobuf);
- streaming;
- high performance.

Used by:

- node-to-node communication (sync);
- advanced clients;
- SDKs.

### 9.2. Services

| Service | Purpose |
|---|---|
| `EventService` | Event submission and retrieval. |
| `IdentityService` | Identity queries. |
| `ReputationService` | Reputation queries. |
| `ContributionService` | Contribution queries. |
| `BountyService` | Bounty operations. |
| `ComputeService` | Compute task operations. |
| `VoteService` | Vote operations. |
| `ContextService` | Context queries. |
| `ValidatorService` | Validator queries. |
| `CheckpointService` | Checkpoint queries. |
| `SyncService` | Node-to-node sync. |
| `AdminService` | Node management. |

### 9.3. Message types

Protobuf messages mirror the JSON schemas:

```protobuf
message Event {
  uint32 version = 1;
  string type = 2;
  string author = 3;
  int64 created_at = 4;
  repeated string parents = 5;
  bytes payload = 6;  // CBOR
  bytes signature = 7;
}

message SubmitEventRequest {
  Event event = 1;
}

message SubmitEventResponse {
  string event_id = 1;
  string status = 2;
  bool finalized = 3;
}
```

### 9.4. Streaming

gRPC supports:

- **Server streaming:** e.g., subscribe to events.
- **Client streaming:** e.g., batch submission.
- **Bidirectional:** e.g., sync.

### 9.5. Sync service

```protobuf
service SyncService {
  rpc GetHeaders(HeadersRequest) returns (stream Header);
  rpc GetEvents(EventsRequest) returns (stream Event);
  rpc Sync(stream SyncMessage) returns (stream SyncMessage);
}
```

### 9.6. Error model

gRPC errors use standard status codes:

| Code | Meaning |
|---|---|
| `INVALID_ARGUMENT` | Bad request. |
| `UNAUTHENTICATED` | Auth required. |
| `PERMISSION_DENIED` | Not allowed. |
| `NOT_FOUND` | Resource not found. |
| `ALREADY_EXISTS` | Duplicate. |
| `RESOURCE_EXHAUSTED` | Rate limit. |
| `INTERNAL` | Server error. |
| `UNAVAILABLE` | Overloaded. |

Error details are in `google.rpc.Status.details`.

### 9.7. Authentication

gRPC uses:

- TLS client certificates;
- or bearer tokens in metadata:

```
authorization: Bearer <token>
```

### 9.8. Compression

gRPC **MUST** support:

- gzip;
- zstd (optional).

### 9.9. Deadlines

Clients **MUST** set deadlines. Long-running operations (sync) use long deadlines.

### 9.10. Reflection

Nodes **SHOULD** enable gRPC reflection for discoverability.

---

## 10. Event Submission

### 10.1. Flow

1. Client constructs event.
2. Client computes event ID (BLAKE3 of canonical CBOR).
3. Client signs event ID with Ed25519.
4. Client submits via `POST /events` or gRPC.
5. Node validates.
6. Node stores and gossips.

### 10.2. Validation

The node checks (see [events.md](./events.md#10-validation-rules)):

- schema;
- version;
- type;
- signature;
- parents;
- semantic rules.

If any check fails, the event is rejected.

### 10.3. Duplicate handling

If the event ID already exists:

- the node returns `409 duplicate`;
- the event is not stored again.

### 10.4. Parent handling

If parents are missing:

- the event is held in the orphan pool;
- the node requests missing parents;
- the client receives `202 Accepted` with `status: "pending_parents"`.

### 10.5. Finality

Newly submitted events are **pending** until included in a finalized checkpoint.

Response indicates:

- `accepted`: the event is valid and stored.
- `pending`: waiting for parents or finalization.
- `finalized`: the event is in a finalized checkpoint.

### 10.6. Batch submission

Batches **MAY** be partial: some events accepted, some rejected. The response indicates which.

For atomicity, use `POST /events/batch?atomic=true`.

### 10.7. Idempotency

Submitting the same event twice is idempotent. The second submission returns `409 duplicate` or `200 OK` (implementation choice).

### 10.8. Size limits

- Max event size: 64 KB.
- Max batch size: 100 events or 1 MB total.

Larger submissions are rejected.

### 10.9. Retry

Clients **SHOULD** retry on `429`, `503`, or network errors. Use exponential backoff.

Clients **MUST NOT** retry on `400`, `401`, `403`, `422`.

### 10.10. Signing helpers

Nodes **MAY** provide signing helpers (e.g., `POST /sign`) that sign events on behalf of the client, if the client delegates. This is **NOT recommended** — clients **SHOULD** sign locally.

---

## 11. Queries

### 11.1. Query patterns

- **Point queries:** get by ID (`/events/:id`).
- **List queries:** get by filter (`/events?author=...`).
- **Time-range queries:** get by time (`/events?from=...&to=...`).
- **Aggregate queries:** get statistics (`/context/:id/stats`).

### 11.2. Pagination

Cursor-based:

- `limit` — max items per page.
- `cursor` — opaque cursor returned by the previous response.

The cursor **MUST NOT** be constructed by clients. It is opaque.

### 11.3. Sorting

Default sort order:

1. `created_at` (ascending).
2. Event ID (lexicographic).

Clients **MAY** request `order=desc` for descending.

### 11.4. Filtering

Filters **MUST** be expressible as query parameters. Complex filters **MAY** use `POST /query` with a JSON body.

### 11.5. Field selection

Clients **MAY** request specific fields via `fields=...`:

```
GET /identity/did:cl:main:alice?fields=did,level,reputation
```

This reduces payload size.

### 11.6. Inclusions

Clients **MAY** request related resources:

```
GET /contribution/blake3:...?include=confirmations,subject
```

### 11.7. Caching

Responses **MUST** include:

- `ETag` — hash of the response.
- `Cache-Control` — max age.

Clients **MAY** use `If-None-Match` for conditional requests.

### 11.8. Reputation queries

Reputation queries support:

- `at` — compute at a specific time.
- `snapshot` — use a specific snapshot.
- `include_history` — return history.

### 11.9. Historical queries

Historical queries **MAY** be expensive. Nodes **SHOULD**:

- cache historical state;
- serve from checkpoints;
- limit the time range.

### 11.10. Aggregates

Aggregate queries:

| Endpoint | Returns |
|---|---|
| `/context/:id/stats` | Member count, contribution count, total CU. |
| `/identity/:did/stats` | Contributions, bounties, votes. |
| `/reputation/:did/:context/history` | Reputation over time. |

### 11.11. Query cost

Some queries are more expensive than others. Nodes **MAY**:

- rate-limit expensive queries;
- require authentication for aggregates;
- offer pre-computed caches.

### 11.12. Full-text search

Nodes **MAY** support full-text search on:

- contribution descriptions;
- bounty tasks;
- vote proposals.

Search is not required by the protocol.

---

## 12. Subscriptions

### 12.1. Subscription types

| Type | Purpose |
|---|---|
| `events` | All events matching a filter. |
| `identity` | Events related to an identity. |
| `context` | Events in a context. |
| `vote` | Events related to a vote. |
| `bounty` | Events related to a bounty. |
| `checkpoints` | New checkpoints. |
| `reputation` | Reputation changes for an identity. |

### 12.2. Filters

Filters are the same as list queries.

### 12.3. Delivery

Events are delivered in real-time, in the order they are received by the node.

Order **MAY** differ from finalized order (due to DAG).

### 12.4. Replay

Clients **MAY** request replay of recent events:

```json
{
  "type": "subscribe",
  "payload": {
    "topic": "events",
    "filter": {...},
    "from": 1730000000
  }
}
```

The node replays events from `from` timestamp.

Replay is **bounded** (e.g., last 1000 events or 24 hours).

### 12.5. Best-effort

Subscriptions are **best-effort**. Clients **MUST** reconcile with REST for correctness.

### 12.6. Subscription limits

- Max 10 subscriptions per connection.
- Max 100 events/sec per subscription.

### 12.7. Unsubscription

Clients **MUST** unsubscribe when no longer interested:

```json
{
  "id": "sub1",
  "type": "unsubscribe"
}
```

Nodes **MAY** auto-unsubscribe inactive subscriptions.

### 12.8. Subscription lifecycle

1. Client subscribes.
2. Node confirms.
3. Events delivered until:
   - client unsubscribes;
   - connection closes;
   - subscription limit reached.

### 12.9. Missing events

If events are dropped (backpressure, network), clients **MUST**:

- detect gaps (missing event IDs);
- re-fetch via REST.

### 12.10. Subscription to reputation

Clients **MAY** subscribe to reputation changes:

```json
{
  "topic": "reputation",
  "did": "did:cl:main:alice",
  "context": "repo:x/y"
}
```

The node sends updates when the identity's reputation changes (due to new contributions, decays, etc.).

---

## 13. Bounty and Compute Endpoints

### 13.1. Bounties

#### `POST /bounty`

Create a bounty (submits a `bounty.create` event).

#### `GET /bounty/:id`

Get bounty details.

#### `GET /bounty`

List bounties with filters.

**Query parameters:**

| Parameter | Description |
|---|---|
| `context` | Filter by context. |
| `issuer` | Filter by issuer. |
| `status` | Filter by status (`open`, `claimed`, etc.). |
| `reward_min` | Min reward. |
| `reward_max` | Max reward. |
| `deadline_before` | Deadline before this time. |

#### `POST /bounty/:id/claim`

Claim a bounty (submits `bounty.claim`).

#### `POST /bounty/:id/submit`

Submit work (submits `bounty.submit`).

#### `POST /bounty/:id/verify`

Verify a submission (submits `bounty.verify`).

#### `POST /bounty/:id/dispute`

Open a dispute.

#### `GET /bounty/:id/history`

Get all events related to a bounty.

### 13.2. Compute tasks

#### `POST /compute/task`

Create a compute task.

#### `GET /compute/task/:id`

Get task details.

#### `GET /compute/task`

List tasks with filters.

#### `POST /compute/task/:id/claim`

Claim a task.

#### `POST /compute/task/:id/submit`

Submit a result.

#### `POST /compute/task/:id/verify`

Verify a result.

#### `POST /compute/task/:id/dispute`

Open a dispute.

#### `GET /compute/executor/:did`

Get executor info.

#### `POST /compute/executor/register`

Register an executor.

### 13.3. Common patterns

All bounty and compute operations:

- submit an event;
- return the event ID;
- return the resulting state.

The state is not mutated directly — events are the source of truth.

---

## 14. Vote Endpoints

### 14.1. Votes

#### `POST /vote`

Create a vote.

#### `GET /vote/:id`

Get vote details, including current tally.

#### `GET /vote`

List votes with filters.

**Query parameters:**

| Parameter | Description |
|---|---|
| `context` | Filter by context. |
| `status` | Filter by status (`open`, `closed`, `finalized`). |
| `deadline_before` | Deadline before this time. |

#### `POST /vote/:id/cast`

Cast a vote.

#### `POST /vote/:id/delegate`

Delegate voting power.

#### `POST /vote/:id/undelegate`

Revoke a delegation.

#### `GET /vote/:id/tally`

Get the current tally (may be provisional if the vote is open).

#### `GET /vote/:id/history`

Get all events related to a vote.

### 14.2. Secret votes

For secret votes:

- `POST /vote/:id/cast` accepts a `commitment` and `proof` instead of an option.
- `GET /vote/:id/tally` returns the decrypted tally after the deadline.

### 14.3. Voting power

#### `GET /vote/:id/power/:did`

Get the voting power of an identity for a specific vote.

**Response:**

```json
{
  "did": "did:cl:main:alice",
  "vote_id": "blake3:...",
  "power": 15.5,
  "own_power": 10.0,
  "delegated_power": 5.5
}
```

---

## 15. Light Client API

### 15.1. Purpose

Light clients (mobile, embedded) require:

- minimal bandwidth;
- minimal storage;
- proofs for verification.

### 15.2. Checkpoint fetch

#### `GET /light/checkpoint`

Get the latest checkpoint.

**Response:**

```json
{
  "checkpoint": {...},
  "signatures": [...]
}
```

### 15.3. Header fetch

#### `GET /light/headers`

Fetch headers in a range.

**Query parameters:**

| Parameter | Description |
|---|---|
| `from` | From height. |
| `to` | To height. |
| `max_count` | Max headers. |

### 15.4. State proof

#### `GET /light/proof`

Request a Merkle proof for a specific state entry.

**Query parameters:**

| Parameter | Description |
|---|---|
| `context` | Context. |
| `did` | Identity. |
| `height` | Height to prove at. |

**Response:**

```json
{
  "proof": ["blake3:...", "blake3:..."],
  "root": "blake3:...",
  "value": 150.5
}
```

### 15.5. Event proof

#### `GET /light/event-proof/:id`

Prove that an event exists.

**Response:**

```json
{
  "event_id": "blake3:...",
  "proof": [...],
  "checkpoint": "blake3:..."
}
```

### 15.6. Filtered subscription

Light clients **MAY** subscribe to a narrow filter:

```json
{
  "topic": "events",
  "filter": {"context": "repo:x/y"},
  "light": true
}
```

The node sends only event IDs and headers (not full payloads). The client fetches full events on demand.

### 15.7. Trust assumptions

Light clients trust:

- checkpoint signatures (validators);
- Merkle proofs (cryptographic).

They do not trust individual nodes.

### 15.8. Rate limits

Light clients are rate-limited less aggressively than full clients, since their requests are small.

### 15.9. Offline caching

Light clients **SHOULD** cache:

- latest checkpoint;
- recent headers;
- proofs for recently queried state.

This allows offline reads.

---

## 16. Node Management API

### 16.1. Purpose

Node operators need to manage their nodes:

- peers;
- configuration;
- status;
- logs.

This API is **restricted** (requires admin auth).

### 16.2. Endpoints

#### `GET /admin/status`

Get node status.

```json
{
  "version": "0.1.0",
  "uptime_seconds": 3600,
  "height": 100000,
  "peers": 12,
  "syncing": false,
  "validator": true,
  "memory_mb": 512,
  "disk_gb": 5.2
}
```

#### `GET /admin/peers`

List connected peers.

#### `POST /admin/peers`

Add a peer manually.

#### `DELETE /admin/peers/:id`

Disconnect a peer.

#### `GET /admin/config`

Get current configuration.

#### `POST /admin/config`

Update configuration (requires admin auth).

#### `POST /admin/shutdown`

Graceful shutdown.

#### `POST /admin/sync`

Trigger a sync.

#### `GET /admin/logs`

Get recent logs.

#### `POST /admin/checkpoint`

Trigger checkpoint creation.

### 16.3. Authentication

Admin API requires:

- TLS client certificate; or
- bearer token with admin scope.

Admin tokens **MUST** be protected. They should never be exposed publicly.

### 16.4. Localhost only

By default, admin API is bound to localhost only.

Remote admin access **MUST** be explicitly enabled and secured.

### 16.5. Audit

All admin actions **SHOULD** be logged:

- timestamp;
- action;
- actor;
- result.

### 16.6. No remote code execution

The admin API **MUST NOT** allow arbitrary code execution. Only predefined actions.

---

## 17. Versioning

### 17.1. API version

The API version is in the path:

```
/api/v1/
```

### 17.2. Breaking changes

Breaking changes require a new version (`v2`).

### 17.3. Non-breaking changes

Non-breaking changes (new fields, new endpoints) **MAY** be added to the current version.

### 17.4. Deprecation

Deprecated endpoints **MUST** be marked:

```
Deprecation: true
Sunset: 2026-01-01
```

### 17.5. Compatibility

Clients **MUST** ignore unknown fields in responses.

Nodes **MUST NOT** remove fields without a version bump.

### 17.6. Protocol vs. API version

The protocol version (in events) is separate from the API version.

An API `v1` node might handle events from protocol version 1.

### 17.7. Version negotiation

Clients **MAY** specify `Accept-Version: v1` in requests.

Nodes **MAY** return `X-Supported-Versions: v1, v2` in responses.

### 17.8. Version sunset

When a version is deprecated:

- a notice is published 6+ months in advance;
- the version remains available for at least 6 months after deprecation;
- clients are encouraged to migrate.

---

## 18. Validation Rules

Nodes **MUST** enforce these rules for API operations.

### 18.1. Request validation

- Content-Type **MUST** be supported.
- Request body **MUST** be valid per schema.
- Required fields **MUST** be present.

### 18.2. Event validation

- Events **MUST** pass all rules in [events.md](./events.md#10-validation-rules).
- Signature **MUST** verify.
- Parents **MUST** exist (or be pending).

### 18.3. Query validation

- Filter parameters **MUST** be valid.
- `limit` **MUST NOT** exceed the max.
- `cursor` **MUST** be valid.

### 18.4. Subscription validation

- Topic **MUST** be supported.
- Filter **MUST** be valid.
- Subscriptions **MUST NOT** exceed limits.

### 18.5. Authentication

- Tokens **MUST** be valid and unexpired.
- Signatures **MUST** verify.
- Scope **MUST** match the operation.

### 18.6. Rate limits

- Limits **MUST** be enforced.
- Violations **MUST** return `429`.
- Headers **MUST** be included.

### 18.7. Error format

- Errors **MUST** follow the standard format.
- Codes **MUST** be from the defined list.

### 18.8. Pagination

- Cursors **MUST** be opaque.
- Order **MUST** be deterministic.

### 18.9. Version compatibility

- Clients using unsupported versions **MUST** receive `400`.
- Version headers **MUST** be respected.

### 18.10. Admin API

- Admin API **MUST** require admin auth.
- Admin API **MUST NOT** be exposed publicly by default.

---

## 19. Examples

### 19.1. Submit a contribution

**Request:**

```http
POST /api/v1/events
Content-Type: application/json
Authorization: Bearer <token>

{
  "event": {
    "version": 1,
    "type": "contribution.create",
    "author": "did:cl:main:alice",
    "created_at": 1730000000,
    "parents": ["blake3:..."],
    "payload": {
      "subject": "did:cl:main:alice",
      "action": "code_commit",
      "context": "repo:x/y",
      "weight_class": "commit",
      "timestamp": 1730000000
    },
    "signature": "ed25519:..."
  }
}
```

**Response:**

```http
HTTP/1.1 201 Created

{
  "event_id": "blake3:7a3b...",
  "status": "accepted",
  "finalized": false
}
```

### 19.2. Query reputation

**Request:**

```http
GET /api/v1/reputation/did:cl:main:alice/repo:x/y
```

**Response:**

```http
HTTP/1.1 200 OK

{
  "did": "did:cl:main:alice",
  "context": "repo:x/y",
  "reputation": 150.5,
  "level": "trusted",
  "computed_at": 1730000000
}
```

### 19.3. Subscribe to events

**Client:**

```json
{
  "id": "sub1",
  "type": "subscribe",
  "payload": {
    "topic": "events",
    "filter": {"context": "repo:x/y"}
  }
}
```

**Node:**

```json
{
  "id": "sub1",
  "type": "subscribed",
  "payload": {"subscription_id": "sub1"}
}
```

**Later, an event arrives:**

```json
{
  "type": "event",
  "subscription": "sub1",
  "payload": {
    "event": {...},
    "received_at": 1730000100
  }
}
```

### 19.4. Claim a bounty

**Request:**

```http
POST /api/v1/bounty/blake3:abc.../claim
Authorization: Bearer <token>

{
  "estimated_completion": 1730050000
}
```

**Response:**

```http
HTTP/1.1 201 Created

{
  "event_id": "blake3:def...",
  "status": "accepted"
}
```

### 19.5. Cast a vote

**Request:**

```http
POST /api/v1/vote/blake3:xyz.../cast
Authorization: Bearer <token>

{
  "option": "yes"
}
```

**Response:**

```http
HTTP/1.1 201 Created

{
  "event_id": "blake3:ghi...",
  "status": "accepted"
}
```

### 19.6. Light client proof

**Request:**

```http
GET /api/v1/light/proof?context=repo:x/y&did=did:cl:main:alice&height=100000
```

**Response:**

```http
HTTP/1.1 200 OK

{
  "proof": ["blake3:...", "blake3:..."],
  "root": "blake3:...",
  "value": 150.5
}
```

### 19.7. Rate limited

**Response:**

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1730000600

{
  "error": {
    "code": "rate_limited",
    "message": "Too many requests.",
    "details": {"retry_after": 30}
  }
}
```

### 19.8. Validation error

**Response:**

```http
HTTP/1.1 400 Bad Request

{
  "error": {
    "code": "invalid_signature",
    "message": "The signature does not verify.",
    "details": {
      "event_id": "blake3:..."
    }
  }
}
```

---

## 20. Test Vectors

Test vectors for the API live in `spec/test-vectors/api.json`.

### 20.1. Coverage

- Event submission (valid, invalid, duplicate).
- Queries with filters, pagination.
- WebSocket subscriptions.
- gRPC calls.
- Authentication flows.
- Error responses.
- Rate limiting.
- Light client proofs.

### 20.2. Format

```json
{
  "description": "Submit a contribution event",
  "request": {
    "method": "POST",
    "path": "/api/v1/events",
    "body": {...}
  },
  "expected_response": {
    "status": 201,
    "body": {"event_id": "blake3:...", "status": "accepted"}
  }
}
```

### 20.3. Determinism

Event IDs, signatures, and hashes **MUST** be deterministic.

### 20.4. Cross-implementation

Test vectors **MUST** pass on at least two implementations before v1.0.

### 20.5. OpenAPI / Protobuf

A complete API specification **SHOULD** be published as:

- OpenAPI 3.1 (for REST);
- AsyncAPI 2.x (for WebSocket);
- Protobuf definitions (for gRPC).

These are generated from the same source as the spec.

---

## 21. Open Questions

- Should the API support **GraphQL** as an alternative to REST?
- How to handle **large queries** (e.g., full history of an identity)?
- Should there be a **query DSL** for complex filters?
- How to handle **cross-context queries** efficiently?
- Should **WebSocket** support **binary messages** (CBOR)?
- How to handle **subscription replay** at scale?
- Should there be a **public API gateway** for the community?
- How to handle **mobile clients** with intermittent connectivity?
- Should **light client proofs** be batched?
- How to handle **anonymous writes** (if allowed at all)?
- Should there be a **write-ahead log** for events?
- How to handle **API keys** vs. DIDs?
- Should **caching headers** be standardized?
- How to handle **timezones** in queries?
- Should there be a **sandbox** API for testing?

These will be resolved through RFCs and community discussion.

---

## Summary

**The API is:**

- REST + WebSocket + gRPC.
- Read-free, write-signed.
- Versioned.
- Rate-limited.
- Idempotent for writes.
- Cursor-paginated for lists.
- Privacy-aware.

**REST endpoints:**

- `/events` — submit, query.
- `/identity` — identity info.
- `/reputation` — reputation queries.
- `/contribution` — contribution queries.
- `/context` — community info.
- `/validator` — validator info.
- `/checkpoint` — checkpoints.
- `/sync` — sync status.
- `/bounty` — bounty operations.
- `/compute` — compute tasks.
- `/vote` — voting.
- `/light` — light client.
- `/admin` — node management.

**WebSocket:**

- Subscriptions to events, identities, contexts, votes, bounties, checkpoints.
- Real-time notifications.
- Best-effort delivery; reconcile with REST.

**gRPC:**

- Typed interface.
- Streaming for sync.
- High performance.

**Authentication:**

- Challenge-response.
- Bearer tokens.
- Event signatures for writes.

**Error model:**

- Standard codes.
- Structured responses.
- Request IDs for tracing.

**Rate limits:**

- Per IP (anonymous).
- Per DID (authenticated).
- Headers on every response.

**Key insight:**

The API is **thin**. It exposes events and derived state. It does not create state. Everything is event-driven. This keeps the API simple and consistent with the protocol.

**Clients can:**

- submit events (signed);
- query state (free);
- subscribe to updates (real-time);
- verify proofs (light clients).

**Nodes can:**

- validate events;
- serve queries;
- propagate events;
- manage peers.

**This is the contract between CL and the world.**

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [identity.md](./identity.md) — identity model.
- [contribution.md](./contribution.md) — contribution records.
- [reputation.md](./reputation.md) — reputation calculation.
- [ledger.md](./ledger.md) — DAG, checkpoints.
- [consensus.md](./consensus.md) — finalization.
- [sync.md](./sync.md) — P2P synchronization.
- [bounty.md](./bounty.md) — bounty operations.
- [vote.md](./vote.md) — voting operations.
- [compute.md](./compute.md) — compute operations.
- [privacy.md](./privacy.md) — privacy features.
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
