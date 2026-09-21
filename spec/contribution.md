# Contribution

**Contribution Ledger — Technical Specification**

**Version:** 0.1 (draft)  
**Status:** Draft  
**Depends on:** [events.md](./events.md) · [identity.md](./identity.md)  
**Related:** [reputation.md](./reputation.md) · [bounty.md](./bounty.md) · [compute.md](./compute.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Design Principles](#2-design-principles)
3. [What Counts as a Contribution](#3-what-counts-as-a-contribution)
4. [Contribution Record](#4-contribution-record)
5. [Weight Classes](#5-weight-classes)
6. [Context Rules](#6-context-rules)
7. [Evidence](#7-evidence)
8. [Confirmation](#8-confirmation)
9. [Decay](#9-decay)
10. [Revocation](#10-revocation)
11. [Disputes](#11-disputes)
12. [Lifecycle](#12-lifecycle)
13. [Validation Rules](#13-validation-rules)
14. [Examples](#14-examples)
15. [Test Vectors](#15-test-vectors)
16. [Open Questions](#16-open-questions)

---

## 1. Overview

A **contribution** is a record of work. It says: "this identity did this action, in this context, at this time, and here is the evidence."

Contributions are the primary source of CU (Contribution Units) and reputation in CL. Everything else — bounties, compute tasks, community help — ultimately resolves into contribution records.

**This file defines:**

- What counts as a contribution (Section 3).
- The structure of a contribution record (Section 4).
- Weight classes and how they determine CU (Section 5).
- How contexts define their own rules (Section 6).
- How evidence is handled (Section 7).
- How contributions are confirmed (Section 8).
- How CU decays over time (Section 9).
- How contributions are revoked (Section 10).
- How disputes are resolved (Section 11).
- The full lifecycle of a contribution (Section 12).
- What validators enforce (Section 13).

Contributions are the core of the economics. Without them, there is no CU, no reputation, no access. This file defines how they work.

---

## 2. Design Principles

### 2.1. Contribution is an action, not a claim

A contribution record is a **claim** of work. It becomes **real** only after confirmation.

Unconfirmed contributions:

- exist in the ledger (immutable);
- earn 0 CU;
- do not affect reputation.

Confirmed contributions:

- earn CU per weight class;
- affect reputation;
- can be revoked later if fraud is found.

### 2.2. Context-scoped

Every contribution is scoped to a **context** (a community, project, or repository). Contexts define their own rules:

- what counts as a contribution;
- what weight classes exist;
- who can confirm;
- how decay works;
- how disputes are resolved.

The protocol provides the framework. Contexts fill in the details.

### 2.3. Evidence-based

Contributions **SHOULD** include evidence:

- hashes of artifacts;
- links to external resources;
- signatures from automated systems (e.g., Git hooks).

Evidence is optional but strongly recommended. Without evidence, confirmation is harder.

### 2.4. Peer-confirmed

Contributions are confirmed by peers, not by a central authority.

The rules for who can confirm what are set by the context. Typically:

- small contributions: 1 confirmation;
- medium: 2–3;
- large: 3+ with reputation thresholds.

### 2.5. Decayable

CU may decay over time. This prevents frozen power and encourages ongoing contribution.

Decay is **optional**. Contexts decide whether to enable it and with what parameters.

### 2.6. Revocable

A contribution that is later found fraudulent, harmful, or erroneous can be revoked.

Revocation:

- does not delete the record (append-only);
- marks it as revoked;
- deducts CU;
- reduces reputation.

### 2.7. No self-confirmation

An identity **MUST NOT** confirm its own contributions.

This is a core rule. Violating it invalidates the contribution.

### 2.8. No double-counting

The same work **MUST NOT** be counted twice. If two contribution records describe the same work, only one is valid.

Detecting duplicates is context-specific. Automated systems **SHOULD** help.

---

## 3. What Counts as a Contribution

A contribution is any action that a context recognizes as valuable. Examples:

### 3.1. Code

- Commits.
- Pull requests.
- Code reviews.
- Refactoring.
- Bug fixes.
- Performance improvements.

### 3.2. Documentation

- Writing docs.
- Translating docs.
- Fixing typos.
- Adding examples.
- Tutorials.

### 3.3. Community

- Answering questions.
- Moderating discussions.
- Mentoring newcomers.
- Organizing events.
- Onboarding members.

### 3.4. Design

- UI/UX design.
- Graphic design.
- Branding.
- Prototyping.

### 3.5. Testing

- Writing tests.
- Running test suites.
- Reporting bugs.
- Reproducing issues.

### 3.6. Operations

- Running infrastructure.
- Maintaining servers.
- CI/CD setup.
- Release management.

### 3.7. Research

- Literature review.
- Experiments.
- Data analysis.
- Writing papers.

### 3.8. Governance

- Reviewing proposals.
- Voting (in some contexts).
- Serving on councils.
- Auditing.

### 3.9. Bounties

- Completing bounties (see [bounty.md](./bounty.md)).
- This creates a contribution record when the bounty is completed.

### 3.10. Compute

- Running compute tasks (see [compute.md](./compute.md)).
- This creates a contribution record when the task is verified.

### 3.11. Community-defined

Contexts **MAY** define their own contribution types.

The protocol does not limit the kinds of contributions. It only defines the structure.

---

## 4. Contribution Record

### 4.1. Event structure

A contribution is expressed as a `contribution.create` event.

```json
{
  "version": 1,
  "type": "contribution.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "subject": "did:cl:main:alice",
    "issuer": "did:cl:org:projectX",
    "action": "code_commit",
    "context": "repo:github.com/x/y",
    "weight_class": "commit",
    "evidence": [
      {"type": "hash", "algo": "sha256", "value": "abc..."},
      {"type": "link", "value": "ipfs://..."}
    ],
    "timestamp": 1730000000,
    "metadata": {
      "commit_hash": "a1b2c3...",
      "lines_added": 42,
      "lines_removed": 8
    }
  },
  "signature": "ed25519:..."
}
```

### 4.2. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `subject` | string (DID) | MUST | The identity that did the work. |
| `issuer` | string (DID) | MAY | The identity attesting the work. |
| `action` | string | MUST | The type of action. |
| `context` | string | MUST | The context (community, project). |
| `weight_class` | string | MUST | The weight class for CU calculation. |
| `evidence` | array | MAY | Evidence supporting the claim. |
| `timestamp` | integer | MUST | When the work was done (Unix time). |
| `metadata` | object | MAY | Action-specific data. |

### 4.3. Field rules

#### `subject`

- **MUST** be a valid DID (see [identity.md](./identity.md)).
- **MUST** be the identity that did the work.
- **MAY** differ from `author` (someone else can record a contribution on behalf of another).

#### `issuer`

- **MAY** be present.
- If present, **MUST** be a valid DID.
- If present, the issuer **MUST** have the right to attest contributions in the context.
- If absent, the contribution is **self-attested** (subject = author).

#### `action`

- **MUST** be a string.
- **SHOULD** be from a known vocabulary (see Section 3).
- Contexts **MAY** define custom actions.

#### `context`

- **MUST** be a string.
- **MUST** refer to a known context (community or project).
- If the context does not exist, the contribution is rejected (unless the context is being created in the same event).

#### `weight_class`

- **MUST** be a string.
- **MUST** be defined in the context's rules.
- If not defined, the contribution is rejected.

#### `evidence`

- **MAY** be present.
- If present, **MUST** be an array of evidence objects (see Section 7).
- Empty arrays **SHOULD** be omitted.

#### `timestamp`

- **MUST** be an integer.
- **MUST** be a Unix timestamp in seconds.
- **SHOULD** be ≤ `created_at` (work done before or at record creation).
- **MAY** be earlier than `created_at` (retroactive recording is allowed).

#### `metadata`

- **MAY** be present.
- **SHOULD** be small (metadata is stored in the ledger).
- Large data **SHOULD** be stored externally and referenced via `evidence`.

### 4.4. Self-attested vs. issued

**Self-attested:** `author = subject`, no `issuer`.

- Used when an identity records its own work.
- Confirmation is required for CU.

**Issued:** `author = issuer`, `subject` is another identity.

- Used when an organization records work done by a member.
- The issuer's signature counts as one confirmation.

**Both:** `author = subject = issuer`.

- Not allowed. An identity **MUST NOT** issue contributions for itself with `issuer = subject`.

### 4.5. Size limits

A contribution event **MUST NOT** exceed a maximum size. Recommended: 64 KB.

Larger data **MUST** be stored externally and referenced via `evidence`.

---

## 5. Weight Classes

A **weight class** determines how many CU a contribution earns.

### 5.1. Definition

Weight classes are defined by the context. Each class has:

- a **name** (e.g., `commit`, `review`, `mentorship_hour`);
- a **weight** (a number, e.g., 1, 2, 5);
- optional **constraints** (e.g., max per day, requires specific role).

### 5.2. Example context rules

```json
{
  "context": "repo:github.com/x/y",
  "weights": {
    "commit": 1,
    "review": 2,
    "mentorship_hour": 5,
    "moderation": 3,
    "event_org": 10,
    "bug_fix": 3,
    "docs_page": 2
  },
  "constraints": {
    "commit": {"max_per_day": 20},
    "review": {"max_per_day": 10},
    "mentorship_hour": {"requires_role": "mentor"}
  }
}
```

### 5.3. Weight range

- **MUST** be a positive number.
- **SHOULD** be ≥ 0.1 and ≤ 1000.
- **MAY** be fractional (e.g., 0.5 for a small contribution).

### 5.4. Constraints

Constraints are optional. They limit:

- **Rate:** max contributions of a type per day/week.
- **Role:** requires a specific role (e.g., mentor).
- **Level:** requires a minimum identity level.
- **Context:** requires membership in a sub-context.

If a constraint is violated, the contribution is rejected.

### 5.5. Default weights

If a context does not define a weight class explicitly, the contribution **SHOULD** be rejected. There is no global default.

This prevents accidental CU farming via undefined classes.

### 5.6. Weight changes

Contexts **MAY** change weights over time. This is done via a `rule.change` event.

**Important:** weight changes are **not retroactive**. A contribution created before the change uses the weight in effect at its `created_at`.

This is enforced by:

- storing the weight class in the contribution record;
- looking up the weight at the time of the event (`created_at`);
- not re-evaluating historical contributions when rules change.

### 5.7. Weight lookup

To compute the CU value of a contribution:

1. Find the context's rules at `contribution.created_at`.
2. Look up the weight class in the rules.
3. Apply any constraints.
4. Multiply by quality coefficient (see Section 8.5).
5. Apply decay (see Section 9).

### 5.8. Weight classes in the ledger

The context's rules are stored as `rule.change` events (or defined at `community.create`).

Validators **MUST** use the rules in effect at the contribution's `created_at`, not the current rules.

---

## 6. Context Rules

A **context** is a scope within which contributions are evaluated. It is defined by a `community.create` event.

### 6.1. Context identifier

A context identifier is a string. Recommended formats:

- `repo:github.com/x/y` — a code repository.
- `org:mycompany` — an organization.
- `community:mycommunity` — a community.
- `coop:mycoop` — a cooperative.

The format is a convention, not enforced by the protocol. Any string works.

### 6.2. Context definition

```json
{
  "type": "community.create",
  "author": "did:cl:main:founder",
  "payload": {
    "id": "repo:github.com/x/y",
    "name": "Project X",
    "rules": {
      "weights": {...},
      "constraints": {...},
      "confirmation": {...},
      "decay": {...},
      "dispute": {...}
    }
  }
}
```

### 6.3. Context rules

| Rule | Purpose |
|---|---|
| `weights` | Weight classes and their values. |
| `constraints` | Rate limits, role requirements. |
| `confirmation` | Who can confirm, thresholds, quality scale. |
| `decay` | Whether CU decays, and with what parameters. |
| `dispute` | How disputes are resolved. |

Each rule is optional. Defaults apply if absent.

### 6.4. Default confirmation rules

If a context does not define confirmation rules, defaults apply:

- small contributions (< 10 CU): 1 confirmation;
- medium (10–100 CU): 2 confirmations;
- large (> 100 CU): 3 confirmations with reputation ≥ 100;
- confirmers **MUST NOT** be the subject;
- confirmers **MUST** have reputation ≥ 10 in the context.

### 6.5. Default decay rules

If a context does not define decay, **no decay** applies.

**Rationale:** decay is a policy choice. Some communities want it; others do not.

### 6.6. Default dispute rules

If a context does not define dispute rules, defaults apply:

- any identity with reputation ≥ 500 in the context can open a dispute;
- disputes are resolved by 3 randomly chosen auditors with reputation ≥ 1000;
- auditors vote;
- majority wins.

### 6.7. Updating rules

Rules are changed via `rule.change` events:

```json
{
  "type": "rule.change",
  "author": "did:cl:main:admin",
  "payload": {
    "context": "repo:github.com/x/y",
    "changes": {
      "weights.commit": 2
    },
    "effective_at": 1730100000
  }
}
```

Changes **MUST** be approved by the context's governance rules (usually a vote).

### 6.8. Sub-contexts

A context **MAY** contain sub-contexts. For example:

- `repo:github.com/x/y` — main repository;
- `repo:github.com/x/y/frontend` — frontend sub-project.

Sub-contexts inherit rules from the parent unless overridden.

Sub-contexts are defined by including the parent in the identifier or by explicit reference in rules.

### 6.9. Cross-context contributions

A single contribution **MUST** belong to exactly one context.

If work spans multiple contexts, separate contribution records are created, one per context.

---

## 7. Evidence

Evidence supports a contribution. It is optional but recommended.

### 7.1. Evidence types

| Type | Description | Fields |
|---|---|---|
| `hash` | A hash of some data. | `algo`, `value` |
| `link` | A URL or URI. | `value` |
| `signature` | A signature from an external system. | `algo`, `value`, `signer` |
| `inline` | Small inline data. | `value` |

### 7.2. Structure

```json
{
  "type": "hash",
  "algo": "sha256",
  "value": "a1b2c3..."
}
```

### 7.3. Rules

- Evidence **MUST** have a `type`.
- `hash` **MUST** have `algo` and `value`.
- `link` **MUST** have `value` (a valid URI).
- `signature` **MUST** have `algo`, `value`, and `signer`.
- `inline` **MUST** have `value` (Base64 for binary, string for text).

### 7.4. Size limits

- Inline evidence **SHOULD** be < 1 KB per entry.
- Total evidence **SHOULD** be < 8 KB per contribution.
- Larger evidence **MUST** be stored externally and referenced via `hash` or `link`.

### 7.5. Privacy

Evidence **MAY** contain sensitive data. Authors **SHOULD**:

- hash sensitive data instead of inlining it;
- use encrypted links (e.g., `ipfs://` with encryption);
- disclose only what is necessary for confirmation.

### 7.6. Availability

Evidence **MAY** become unavailable over time (dead links, deleted files).

If evidence is needed for confirmation but is unavailable:

- the contribution **MAY** be rejected;
- or confirmation **MAY** rely on other factors (reputation, peer attestation).

### 7.7. Verification

Confirmers **SHOULD** verify evidence before confirming:

- hashes match the artifact;
- links resolve;
- signatures verify.

Verification is manual or automated, depending on the evidence type.

### 7.8. Automated evidence

Some contexts **MAY** use automated systems to generate evidence:

- Git hooks produce commit hashes;
- CI systems produce build logs;
- testing frameworks produce test results.

Automated evidence **MUST** be signed by the system's identity (Level 2+).

---

## 8. Confirmation

Confirmation turns a claim into a verified contribution.

### 8.1. Event structure

```json
{
  "version": 1,
  "type": "contribution.confirm",
  "author": "did:cl:main:bob",
  "created_at": 1730000100,
  "parents": ["blake3:..."],
  "payload": {
    "contribution_id": "blake3:abc...",
    "quality": 0.9,
    "comment": "Clean code, good tests."
  },
  "signature": "ed25519:..."
}
```

### 8.2. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `contribution_id` | string | MUST | The ID of the contribution event. |
| `quality` | float | MAY | Quality coefficient (0.0 to 1.0). Default: 1.0. |
| `comment` | string | MAY | Explanation for the confirmation. |

### 8.3. Rules

- `contribution_id` **MUST** reference an existing `contribution.create` event.
- The confirmer **MUST NOT** be the subject of the contribution.
- The confirmer **MUST** have the right to confirm in the context.
- The confirmer **MUST NOT** confirm the same contribution twice.
- `quality` **MUST** be between 0.0 and 1.0 (inclusive) if present.

### 8.4. Confirmation threshold

A contribution is **confirmed** when it has enough confirmations, per the context's rules.

Defaults:

| Contribution size | Confirmations required | Confirmer reputation |
|---|---|---|
| < 10 CU | 1 | ≥ 10 |
| 10–100 CU | 2 | ≥ 50 |
| > 100 CU | 3 | ≥ 100 |

If the threshold is met, the contribution earns CU.

If the threshold is not met within a timeout (default: 30 days), the contribution **MAY** be automatically rejected.

### 8.5. Quality coefficient

Each confirmation includes an optional `quality` value:

- 1.0 — excellent.
- 0.5 — acceptable.
- 0.0 — poor.

The contribution's overall quality is the **average** of all confirmation quality values.

```
quality = sum(confirmations.quality) / count(confirmations)
```

Default quality (if not specified): 1.0.

Final CU:

```
CU = weight × quality × decay
```

Where `decay` is the time-based decay (see Section 9).

### 8.6. Confirmation roles

Different contexts may define different confirmation rules:

- **Open confirmation:** anyone with reputation ≥ threshold can confirm.
- **Role-based:** only specific roles (e.g., maintainers) can confirm.
- **Committee:** a specific set of identities must confirm.
- **Automated:** a specific system (e.g., CI) confirms.

The rules are defined in the context's `confirmation` config.

### 8.7. Confirmation of issued contributions

If a contribution was created by an `issuer` (author ≠ subject):

- The issuer's signature counts as **one** confirmation.
- Additional confirmations are still required per the threshold.

This prevents an issuer from unilaterally awarding CU.

### 8.8. Rejection of confirmation

A confirmer **MUST NOT** confirm a contribution if:

- the contribution is fraudulent;
- the evidence is invalid;
- the contribution violates context rules;
- the confirmer has a conflict of interest (e.g., is the subject's collaborator on the same project and reputation thresholds are not met).

Violation of these rules **MAY** result in the confirmer's own reputation being penalized.

### 8.9. Confirmation window

Contributions **MAY** be confirmed at any time after creation. There is no upper limit.

However, contexts **MAY** define:

- a maximum confirmation window (e.g., 90 days);
- a minimum delay before confirmation (e.g., 1 day, to allow disputes).

Defaults:

- no maximum window;
- minimum delay: 0 seconds.

### 8.10. Bulk confirmation

Multiple confirmations for the same contribution **MAY** be submitted by different identities in parallel.

The order does not matter. The threshold is met when the count reaches the required value.

### 8.11. Automated confirmation

Some contributions **MAY** be confirmed automatically by a trusted system:

- a Git hook confirms commits;
- a CI system confirms test passes;
- a payment system confirms bounty completion.

Automated confirmations **MUST** be signed by the system's identity, which **MUST** have the required role in the context.

---

## 9. Decay

Decay reduces the value of CU over time. It is optional.

### 9.1. Purpose

- Prevent frozen power.
- Encourage ongoing contribution.
- Reflect that old contributions are less relevant than recent ones.

### 9.2. Decay function

Decay is exponential:

```
d(Δt) = 0.5 ^ (Δt / half_life)
```

Where:

- `Δt` = time since contribution (in seconds).
- `half_life` = time for the value to halve (in seconds).

### 9.3. Floor

Decay **MUST NOT** reduce CU below a floor:

```
d(Δt) = max(floor, 0.5 ^ (Δt / half_life))
```

Recommended floor: 0.1 (CU never falls below 10% of original value).

If `floor = 0`, decay continues indefinitely.

### 9.4. Parameters

Contexts define:

```json
{
  "decay": {
    "enabled": true,
    "half_life_days": 730,
    "floor": 0.1
  }
}
```

| Parameter | Default | Description |
|---|---|---|
| `enabled` | false | Whether decay applies. |
| `half_life_days` | 730 (2 years) | Time for value to halve. |
| `floor` | 0.1 | Minimum remaining fraction. |

### 9.5. Calculation

Decayed CU at time `t`:

```
CU_decayed(t) = CU_original × max(floor, 0.5 ^ ((t - t_created) / half_life))
```

Where:

- `t_created` = the contribution's `timestamp` or `created_at`.
- `t` = the current time or the time of evaluation.

### 9.6. Decay and reputation

Reputation is computed from decayed CU. When a contribution decays, reputation decreases accordingly.

**Important:** reputation is recomputed from the current time. It is not frozen.

### 9.7. Decay and snapshots

Votes use snapshots of reputation (see [vote.md](./vote.md)). A snapshot freezes reputation at a specific time. Decay does not apply during a vote — the snapshot value is used.

### 9.8. Decay and revocation

Revoked contributions have CU = 0. Decay does not apply (there is nothing to decay).

### 9.9. Decay and long-term contributions

Some contributions **SHOULD NOT** decay:

- foundational work (e.g., creating a project);
- significant milestones (e.g., v1.0 release);
- long-term commitments (e.g., years of moderation).

Contexts **MAY** define exceptions:

```json
{
  "decay": {
    "enabled": true,
    "half_life_days": 730,
    "floor": 0.1,
    "exempt_classes": ["foundation", "milestone"]
  }
}
```

Exempt classes never decay.

### 9.10. Disabling decay

If `enabled = false`:

- decay does not apply;
- CU remains at original value indefinitely.

Some contexts (e.g., archival projects) may choose this.

### 9.11. Interaction with new contributions

New contributions add to reputation. Decay reduces existing contributions. Net reputation can:

- grow (new contributions exceed decay);
- stay flat (new = decay);
- decline (decay exceeds new).

This is intentional. It encourages ongoing participation.

### 9.12. Retroactive changes

Changing decay parameters (e.g., half-life) is **not retroactive** to already-computed snapshots. But it **MUST** apply to future computations.

This creates a subtle issue: reputation at time T1 computed with old parameters may differ from reputation at time T2 computed with new parameters, even for the same historical contributions.

**Resolution:** reputation is always computed with the **current** parameters at the time of evaluation. Historical snapshots (e.g., for votes) preserve the parameters in effect at snapshot time.

---

## 10. Revocation

A contribution that is later found problematic can be revoked.

### 10.1. Event structure

```json
{
  "version": 1,
  "type": "contribution.revoke",
  "author": "did:cl:main:auditor",
  "created_at": 1731000000,
  "parents": ["blake3:..."],
  "payload": {
    "contribution_id": "blake3:abc...",
    "reason": "fraud",
    "evidence": [
      {"type": "link", "value": "ipfs://..."}
    ]
  },
  "signature": "ed25519:..."
}
```

### 10.2. Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| `contribution_id` | string | MUST | The ID of the contribution to revoke. |
| `reason` | string | MUST | Reason for revocation. |
| `evidence` | array | MAY | Evidence supporting revocation. |

### 10.3. Reasons

| Reason | Meaning |
|---|---|
| `fraud` | Work was not done or was fabricated. |
| `error` | Contribution was misclassified or double-counted. |
| `harm` | Contribution caused harm (security, legal, ethical). |
| `duplicate` | Same work counted twice. |
| `withdrawn` | Subject withdrew the contribution. |
| `other` | Custom reason (must include explanation). |

### 10.4. Who can revoke

- **Subject:** can revoke their own contribution.
- **Issuer:** can revoke contributions they issued.
- **Auditor:** with role `auditor` in the context, can revoke after review.
- **Community vote:** a qualified majority can revoke any contribution.

### 10.5. Effects

When a contribution is revoked:

- CU is set to 0.
- Reputation is reduced accordingly.
- The contribution record remains in the ledger (append-only).
- The revocation event is linked.
- Attestations or roles that depended on the contribution **MAY** be revoked by the community.

### 10.6. Reversal of revocation

A revoked contribution **MAY** be un-revoked via a `contribution.unrevoke` event:

```json
{
  "type": "contribution.unrevoke",
  "author": "did:cl:main:auditor",
  "payload": {
    "revocation_id": "blake3:...",
    "reason": "reversal",
    "evidence": [...]
  }
}
```

Rules:

- Only the original revoker or a higher authority can un-revoke.
- Un-revocation restores the CU.
- History is preserved (both revocation and un-revocation are in the ledger).

### 10.7. Mass revocation

If many contributions are fraudulent (e.g., a compromised identity), a community **MAY** vote to revoke all contributions from a specific identity or time period.

This is done via a `community.rule` event with a specific revocation directive.

---

## 11. Disputes

Disputes arise when a contribution's validity is contested.

### 11.1. Opening a dispute

```json
{
  "type": "contribution.dispute",
  "author": "did:cl:main:bob",
  "payload": {
    "contribution_id": "blake3:abc...",
    "reason": "evidence_invalid",
    "evidence": [...]
  }
}
```

### 11.2. Who can open a dispute

- The subject (defending).
- The issuer (challenging).
- Any identity with reputation ≥ threshold in the context.

### 11.3. Dispute process

1. Dispute opened.
2. Three auditors randomly selected (reputation ≥ threshold, not involved in the dispute).
3. Auditors review evidence.
4. Auditors vote: uphold / revoke / unclear.
5. Decision finalized.
6. CU adjusted accordingly.

### 11.4. Auditor selection

Random selection weighted by reputation, with the constraint that:

- no auditor is the subject or the issuer;
- no auditor has a conflict of interest (same organization, same project);
- auditors are from different organizations if possible.

### 11.5. Audit incentive

Auditors receive a small percentage of the disputed CU (or a fixed fee from the context's treasury).

If auditors do not vote within the deadline, they lose a small amount of reputation.

### 11.6. Appeals

A dispute decision **MAY** be appealed to a higher council (if the context has one). The council reviews the audit and makes a final decision.

### 11.7. Frivolous disputes

Filing a dispute in bad faith results in reputation penalty for the filer.

Repeated frivolous disputes may result in loss of the right to dispute.

---

## 12. Lifecycle

A contribution passes through several states.

### 12.1. States

```
pending → confirmed → (active | revoked)
                ↓
             disputed → (active | revoked)
```

| State | Meaning |
|---|---|
| `pending` | Created, waiting for confirmations. |
| `confirmed` | Confirmation threshold met, CU awarded. |
| `disputed` | Under dispute review. |
| `revoked` | Revoked, CU = 0. |

### 12.2. Transitions

**pending → confirmed:**
- Threshold met.
- CU is now attributed.

**pending → expired:**
- Timeout reached without confirmation.
- No CU awarded.

**confirmed → disputed:**
- Dispute opened.
- CU is frozen (not yet deducted).

**confirmed → revoked:**
- Direct revocation (by auditor or vote).
- CU set to 0.

**disputed → confirmed:**
- Dispute resolved in favor of the subject.
- CU remains awarded.

**disputed → revoked:**
- Dispute resolved against the subject.
- CU set to 0.

**revoked → active:**
- Un-revocation.
- CU restored.

### 12.3. CU computation over time

CU is recomputed continuously:

```
CU(t) = sum over all confirmed, non-revoked contributions:
    weight × quality × decay(t - t_created)
```

This means CU is not "awarded once" — it is a dynamic value that changes with:

- confirmations (adding quality);
- revocation;
- decay over time.

### 12.4. Reputation

Reputation is derived from CU per the formula in [reputation.md](./reputation.md).

Reputation is context-specific. A contribution in context A does not affect reputation in context B (unless the contexts recognize each other's contributions).

### 12.5. Historical state

Validators **MUST** be able to compute reputation at any historical time, given the events up to that time.

This is important for:

- votes (snapshots);
- disputes (was the threshold met at the time?);
- audits (reconstructing historical state).

---

## 13. Validation Rules

Validators **MUST** enforce these rules for contribution-related events.

### 13.1. `contribution.create` rules

- `version` **MUST** be supported.
- `author` **MUST** be a valid identity.
- `subject` **MUST** be a valid identity.
- `subject` **MUST NOT** equal `issuer` if both are present.
- `context` **MUST** refer to a known context.
- `weight_class` **MUST** be defined in the context.
- `timestamp` **MUST** be ≤ `created_at` (work done before or at record time).
- `evidence` entries **MUST** be valid.
- Event size **MUST NOT** exceed the maximum (64 KB recommended).

### 13.2. `contribution.confirm` rules

- `contribution_id` **MUST** reference an existing `contribution.create`.
- The contribution **MUST NOT** be already revoked.
- The confirmer **MUST NOT** be the subject.
- The confirmer **MUST NOT** have already confirmed this contribution.
- The confirmer **MUST** have the required role or reputation.
- `quality` **MUST** be in [0.0, 1.0] if present.

### 13.3. `contribution.revoke` rules

- `contribution_id` **MUST** reference an existing `contribution.create`.
- The revoker **MUST** have the right to revoke.
- `reason` **MUST** be one of the allowed reasons.
- If `reason = other`, a comment **MUST** be present.

### 13.4. `contribution.dispute` rules

- `contribution_id` **MUST** reference an existing `contribution.create`.
- The disputer **MUST** have the right to open a dispute.
- The contribution **MUST NOT** be already revoked.
- The dispute **MUST NOT** be redundant (a dispute is already open).

### 13.5. Weight lookup

Validators **MUST** look up the weight at `contribution.created_at`, not at the time of confirmation.

If rules changed between creation and confirmation, the original weight applies.

### 13.6. Decay application

Validators **MUST** apply decay when computing CU, unless the context disables it.

Decay is computed using the current time or the snapshot time (for votes).

### 13.7. Confirmation timeouts

If a context defines a timeout, validators **MUST** reject confirmations after the timeout.

If no timeout is defined, confirmations are accepted indefinitely.

### 13.8. Duplicate detection

Validators **SHOULD** detect duplicate contributions:

- same subject, same action, same context, same timestamp;
- same evidence hash;
- same metadata (e.g., same commit hash).

Duplicates **SHOULD** be rejected or flagged.

### 13.9. Context existence

Validators **MUST** check that the context exists before accepting a contribution.

If the context is being created in the same batch (genesis), the rules apply.

---

## 14. Examples

### 14.1. Simple self-attested contribution

```json
{
  "version": 1,
  "type": "contribution.create",
  "author": "did:cl:main:alice",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "subject": "did:cl:main:alice",
    "action": "code_commit",
    "context": "repo:github.com/x/y",
    "weight_class": "commit",
    "evidence": [
      {"type": "hash", "algo": "sha256", "value": "a1b2c3..."}
    ],
    "timestamp": 1730000000
  },
  "signature": "ed25519:..."
}
```

### 14.2. Issued contribution

```json
{
  "version": 1,
  "type": "contribution.create",
  "author": "did:cl:org:university",
  "created_at": 1730000000,
  "parents": ["blake3:..."],
  "payload": {
    "subject": "did:cl:main:alice",
    "issuer": "did:cl:org:university",
    "action": "course_completion",
    "context": "org:university",
    "weight_class": "course",
    "metadata": {"course_id": "CS-101", "grade": "A"},
    "timestamp": 1730000000
  },
  "signature": "ed25519:..."
}
```

### 14.3. Confirmation

```json
{
  "version": 1,
  "type": "contribution.confirm",
  "author": "did:cl:main:bob",
  "created_at": 1730000100,
  "parents": ["blake3:..."],
  "payload": {
    "contribution_id": "blake3:abc...",
    "quality": 0.9,
    "comment": "Clean code, good tests."
  },
  "signature": "ed25519:..."
}
```

### 14.4. Revocation

```json
{
  "version": 1,
  "type": "contribution.revoke",
  "author": "did:cl:main:auditor",
  "created_at": 1731000000,
  "parents": ["blake3:..."],
  "payload": {
    "contribution_id": "blake3:abc...",
    "reason": "fraud",
    "evidence": [
      {"type": "link", "value": "ipfs://..."}
    ]
  },
  "signature": "ed25519:..."
}
```

### 14.5. Full lifecycle

```
1. Alice creates a contribution (pending).
2. Bob confirms it (1 confirmation).
3. Carol confirms it (2 confirmations).
4. Threshold met → confirmed.
5. CU awarded: weight × quality × decay.
6. After 2 years, CU has decayed to ~50% (if half-life = 2 years).
7. After 5 years, CU has decayed to ~10% (if floor = 0.1).
```

---

## 15. Test Vectors

Test vectors for contributions live in `spec/test-vectors/contributions.json`.

### 15.1. Coverage

- Minimal contribution (subject = author, no issuer, no evidence).
- Full contribution (all fields).
- Issued contribution (author ≠ subject).
- Contribution with multiple evidence entries.
- Confirmation (with and without quality).
- Revocation (all reasons).
- Dispute.
- Invalid contributions:
  - missing required fields;
  - unknown context;
  - unknown weight class;
  - self-issued (issuer = subject);
  - timestamp > created_at;
  - oversized evidence;
  - invalid evidence type.

### 15.2. Fixed test context

```json
{
  "context": "test:contributions",
  "weights": {
    "commit": 1,
    "review": 2,
    "mentorship_hour": 5
  },
  "confirmation": {
    "small": {"count": 1, "min_reputation": 10},
    "medium": {"count": 2, "min_reputation": 50},
    "large": {"count": 3, "min_reputation": 100}
  },
  "decay": {
    "enabled": true,
    "half_life_days": 730,
    "floor": 0.1
  }
}
```

### 15.3. Verifying

Implementations **MUST** produce byte-identical event IDs for the contribution events in the test vectors.

### 15.4. Reputation calculation

The test vectors include reputation calculations, verifying that decay, quality, and revocation are applied correctly.

---

## 16. Open Questions

- How to handle **partial contributions** (work not fully completed)?
- Should there be a **maximum number of confirmations** to prevent over-confirmation?
- How to handle **cross-context contributions** that benefit multiple communities?
- Should **negative contributions** exist (work that harms the community)?
- How to detect **collusive confirmation rings**?
- Should contributions have an **expiry** (auto-revoke if not confirmed)?
- How to handle **AI-generated contributions** (code written by AI, submitted by a human)?
- Should there be a **minimum quality threshold** below which CU is not awarded?
- How to handle **contributions by bots** (automated systems)?
- Should contributions be **transferable between contexts**?
- How to handle **retroactive weight changes**?
- Should there be a **cap on CU per identity per context**?
- How to handle **contributions that become invalid due to external factors** (e.g., a dependency is deprecated)?
- Should **anonymous contributions** be allowed (no subject)?
- How to handle **collective contributions** (a team, not an individual)?

These will be resolved through RFCs and community discussion.

---

## Summary

**A contribution is:**

- A record of work.
- Scoped to a context.
- Subject to weight classes.
- Confirmed by peers.
- Subject to decay.
- Revocable.

**Lifecycle:**

- Pending → confirmed → active or revoked.
- Disputes possible at any stage.

**CU formula:**

```
CU = weight × quality × decay
```

**Validation:**

- Structural, semantic, authorization, timing, uniqueness.
- Weight looked up at creation time, not confirmation time.

**Decay:**

- Optional.
- Exponential with floor.
- Context-configurable.

**Revocation:**

- By subject, issuer, auditor, or vote.
- Preserves history.
- Reduces CU to 0.

**Disputes:**

- Opened by anyone with standing.
- Resolved by random auditors.
- Final decision by council (optional).

---

**Related documents:**

- [README](./README.md) — how to read the spec.
- [events.md](./events.md) — event format.
- [identity.md](./identity.md) — identity model.
- [reputation.md](./reputation.md) — reputation calculation.
- [bounty.md](./bounty.md) — bounties (which create contributions).
- [compute.md](./compute.md) — compute (which creates contributions).
- [test-vectors/](./test-vectors/) — test vectors.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 0.1 (draft)

---
