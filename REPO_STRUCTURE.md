# Repository Structure

**Contribution Ledger — complete file map with descriptions.**

**Version:** 1.0  
**Status:** Living document  
**Related:** [README](../README.md) · [Whitepaper](./whitepaper.md) · [CONTRIBUTING](../CONTRIBUTING.md)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Full Tree](#2-full-tree)
3. [Root Files](#3-root-files)
4. [docs/ — Documentation](#4-docs--documentation)
5. [spec/ — Technical Specification](#5-spec--technical-specification)
6. [rfcs/ — Requests for Comments](#6-rfcs--requests-for-comments)
7. [.github/ — GitHub Configuration](#7-github--github-configuration)
8. [Future Directories](#8-future-directories)
9. [Naming Conventions](#9-naming-conventions)
10. [What Goes Where](#10-what-goes-where)

---

## 1. Overview

The repository has four main areas:

| Area | Purpose | Audience |
|---|---|---|
| Root files | Entry points, rules, licenses | Everyone |
| `docs/` | Conceptual documentation | Readers, newcomers |
| `spec/` | Technical specification | Implementers |
| `rfcs/` | Change proposals | Contributors |

**Rule of thumb:**

- **`docs/`** — why and what. Readable by anyone.
- **`spec/`** — how. Readable by developers.
- **`rfcs/`** — changes. Readable by contributors.

---

## 2. Full Tree

```
Contribution-Ledger/
│
├── README.md                      # Project overview (EN + RU)
├── SUMMARY.md                     # One-page summary (EN)
├── SUMMARY.ru.md                  # One-page summary (RU)
├── LICENSE                        # CC BY-SA 4.0 (text) / MIT (code)
├── CONTRIBUTING.md                # How to contribute
├── CODE_OF_CONDUCT.md             # Community rules
├── REPO_STRUCTURE.md              # This file
├── CHANGELOG.md                   # Version history
├── AUTHORS.md                     # Contributors list
├── CONTRIBUTORS.md                # Extended contributor recognition
│
├── docs/                          # Conceptual documentation
│   ├── whitepaper.md              # Full whitepaper (EN)
│   ├── whitepaper.ru.md           # Full whitepaper (RU)
│   ├── economics.md               # How participants earn
│   ├── useful-work.md             # Compute and community help
│   ├── roadmap.md                 # 5-year plan
│   ├── faq.md                     # 30+ questions
│   ├── glossary.md                # Terms and definitions
│   └── comparison.md              # CL vs Bitcoin, Ethereum, Nostr, etc.
│
├── spec/                          # Technical specification
│   ├── README.md                  # How to read the spec
│   ├── events.md                  # Canonical serialization, event envelope
│   ├── identity.md                # Keys, DID, attestations, recovery
│   ├── contribution.md            # Contribution records, weights, decay
│   ├── reputation.md              # Formula, context, caching
│   ├── ledger.md                  # DAG, Merkle, storage
│   ├── consensus.md               # Validators, finalization, fork
│   ├── bounty.md                  # Bounty lifecycle, escrow, arbitration
│   ├── vote.md                    # Proposals, quadratic weight, delegation
│   ├── compute.md                 # Compute tasks, verification, staking
│   ├── sync.md                    # P2P synchronization, gossip
│   ├── api.md                     # REST, WebSocket, gRPC
│   ├── privacy.md                 # ZK, selective disclosure
│   └── test-vectors/              # Test vectors for implementations
│       ├── events.json
│       ├── reputation.json
│       ├── votes.json
│       └── README.md
│
├── rfcs/                          # Requests for Comments
│   ├── README.md                  # RFC process overview
│   ├── 0000-template.md           # RFC template
│   └── (numbered RFCs as they arrive)
│
├── .github/                       # GitHub configuration
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   ├── rfc_proposal.md
│   │   └── config.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── markdown-lint.yml
│       └── link-check.yml
│
└── (future — see Section 8)
    ├── core/                      # Reference implementation
    ├── clients/                   # Web, mobile, CLI
    ├── tools/                     # Utilities
    └── examples/                  # Sample integrations
```

---

## 3. Root Files

These are the first files a visitor sees. They must be clear, short, and honest.

### 3.1. `README.md`

**Purpose:** Project overview, English + Russian.  
**Audience:** Everyone.  
**Length:** ~300 lines.  
**Contents:**
- One-sentence pitch.
- What is it, why, how people earn.
- Not a cryptocurrency (comparison table).
- Status and roadmap link.
- How to contribute.
- License.

**Rule:** If a visitor cannot understand the project in 30 seconds, rewrite it.

### 3.2. `SUMMARY.md`

**Purpose:** One-page summary for quick reading.  
**Audience:** People who want the gist without the full whitepaper.  
**Length:** ~100 lines.  
**Contents:**
- Problem, idea, how people earn.
- Useful work.
- Governance.
- Status, risks, what we need.
- One-line pitch.

**Use cases:**
- Send to a friend.
- Attach to a grant application.
- Print as a one-pager.

### 3.3. `SUMMARY.ru.md`

**Purpose:** Russian version of `SUMMARY.md`.  
**Audience:** Russian-speaking readers.

### 3.4. `LICENSE`

**Purpose:** Legal terms.  
**Contents:**
- Text and documentation: **CC BY-SA 4.0**.
- Code: **MIT** or **Apache 2.0**.

**Rule:** No license = no one can legally use the project. Do not skip this.

### 3.5. `CONTRIBUTING.md`

**Purpose:** How to contribute.  
**Audience:** Anyone who wants to help.  
**Length:** ~400 lines.  
**Contents:**
- What we need (critics, developers, translators, etc.).
- Ways to contribute.
- Getting started.
- How to propose changes (small, medium, large).
- RFC process.
- PR guidelines.
- Commit message convention.
- Review process.
- Code style, writing style.
- What we will not accept (no token, no speculation).
- Recognition.

### 3.6. `CODE_OF_CONDUCT.md`

**Purpose:** Community rules.  
**Audience:** All participants.  
**Length:** ~350 lines.  
**Contents:**
- Our pledge.
- Standards of behavior.
- Unacceptable behavior.
- Project-specific rules (no crypto shilling, no hype, no recruitment).
- Scope.
- Enforcement guidelines.
- Appeals.

### 3.7. `REPO_STRUCTURE.md`

**Purpose:** This file. Map of the repository.  
**Audience:** New contributors.  
**Contents:**
- Full tree.
- Description of each file.
- Where new content goes.

### 3.8. `CHANGELOG.md`

**Purpose:** Version history.  
**Audience:** Anyone tracking changes.  
**Format:** [Keep a Changelog](https://keepachangelog.com/).

**Example:**

```markdown
## [1.2.0] - 2025-01-15

### Added
- Whitepaper v1.2 (EN, RU)
- docs/economics.md
- docs/useful-work.md
- docs/roadmap.md

### Changed
- Repositioned economy from "optional" to "core value proposition"

## [1.1.0] - 2024-12-01

### Added
- Section 3: Value for Participants
- Section 13: Economics
```

### 3.9. `AUTHORS.md`

**Purpose:** List of project authors and maintainers.  
**Format:**

```markdown
# Authors

## Founder
- mikky1sCp (@mikky1sCp)

## Maintainers
- (to be added)

## Co-authors
- (to be added)
```

### 3.10. `CONTRIBUTORS.md`

**Purpose:** Extended recognition of contributors.  
**Difference from AUTHORS.md:**
- `AUTHORS.md` — people with commit rights.
- `CONTRIBUTORS.md` — everyone who contributed (code, docs, translation, review, criticism).

**Format:**

```markdown
# Contributors

| Name | Contribution | Date |
|---|---|---|
| @user1 | Translated FAQ to Spanish | 2025-03 |
| @user2 | Reviewed reputation formula | 2025-02 |
| @user3 | Found 12 typos in whitepaper | 2025-01 |
```

**Rule:** Every contribution counts. Even a typo fix.

---

## 4. docs/ — Documentation

Conceptual documentation. Readable by anyone, not just developers.

### 4.1. `docs/whitepaper.md`

**Purpose:** Full whitepaper in English.  
**Audience:** Anyone who wants the complete design.  
**Length:** ~1 500 lines.  
**Contents:**
1. Abstract
2. Philosophy and Motivation
3. Value for Participants
4. The Problem
5. Why Not a Cryptocurrency
6. System Overview
7. Identity Model
8. Contribution Model
9. Reputation Model
10. Ledger and Data Structures
11. Consensus and Validators
12. Governance and Voting
13. Economics
14. Useful Work
15. Privacy and Security
16. Threats and Defenses
17. Use Cases
18. Architecture and Stack
19. Roadmap
20. Project Governance
21. Open Questions
22. Conclusion
23. Appendices

### 4.2. `docs/whitepaper.ru.md`

**Purpose:** Russian version of the whitepaper.  
**Rule:** Keep in sync with the English version. Note the version at the top.

### 4.3. `docs/economics.md`

**Purpose:** How participants earn.  
**Audience:** Anyone asking "what's in it for me?"  
**Length:** ~500 lines.  
**Contents:**
- Core principle: profit from outside.
- Where money comes from.
- 9 earning schemes (bounties, work, grants, cooperatives, communities, roles, savings, reputation as capital, compute).
- Summary table.
- What CL does not offer.
- Who benefits, who does not.
- 3-year example.
- Prohibition on CU monetization.

**Rule:** This is the second file a visitor should read after the summary.

### 4.4. `docs/useful-work.md`

**Purpose:** Compute and community help.  
**Audience:** People interested in the compute side.  
**Length:** ~600 lines.  
**Contents:**
- The idea: useful work instead of mining.
- Why not mining.
- The trap (speculation).
- Three rules to avoid cryptocurrency.
- Types of useful work.
- Three phases: community help, small compute, AI and large compute.
- Task lifecycle.
- Verification methods (redundancy, sampling, ZK, reputation, staking).
- Pricing.
- Compute task events.
- Anti-abuse.
- Hardware and rewards.

### 4.5. `docs/roadmap.md`

**Purpose:** 5-year plan.  
**Audience:** Contributors, grant reviewers, partners.  
**Length:** ~500 lines.  
**Contents:**
- Principles.
- Year-by-year breakdown (Q1–Q4 each).
- Milestones summary.
- What success looks like.
- What failure looks like.
- Risks and pivots.
- What this roadmap is not.

### 4.6. `docs/faq.md`

**Purpose:** Common questions and answers.  
**Audience:** Everyone.  
**Length:** ~500 lines.  
**Contents:**
15 sections, ~70 questions:
1. The basics.
2. Why not a cryptocurrency.
3. How people earn.
4. Contribution Units (CU).
5. Identity and privacy.
6. Reputation.
7. Bounties and payments.
8. Useful work and compute.
9. Governance.
10. Technical questions.
11. Project status.
12. How to help.
13. Criticism and doubts.
14. Comparison to other projects.
15. Legal.

**Rule:** If a question comes up twice, add it to the FAQ.

### 4.7. `docs/glossary.md`

**Purpose:** Terms and definitions.  
**Audience:** Anyone confused by jargon.  
**Length:** ~100 terms.  
**Format:**

```markdown
## A

**Attestation** — A signed claim about an identity, issued by an organization.
Example: "did:cl:org:university attests that did:cl:main:alice is a student."

**AUDITOR** — A participant with high reputation who resolves disputes.

## B

**Bounty** — A paid task posted by an organization. See [docs/economics.md](../docs/economics.md#3-scheme-1-bounties).

**BLAKE3** — A cryptographic hash function used in CL. Faster than SHA-256.
```

### 4.8. `docs/comparison.md`

**Purpose:** How CL compares to other projects.  
**Audience:** People who ask "isn't this just X?"  
**Length:** ~300 lines.  
**Contents:**
- CL vs Bitcoin.
- CL vs Ethereum.
- CL vs Gitcoin.
- CL vs Nostr.
- CL vs Holochain.
- CL vs LinkedIn.
- CL vs DAO.
- CL vs Bittensor.
- CL vs Golem / iExec.
- Complementary projects.

**Rule:** Be fair. Do not strawman. If another project does something better, say so.

---

## 5. spec/ — Technical Specification

The specification is what implementers read. It must be precise, unambiguous, and complete.

### 5.1. `spec/README.md`

**Purpose:** How to read the spec.  
**Contents:**
- What the spec is and is not.
- Versioning policy.
- Normative vs informative language (RFC 2119: MUST, SHOULD, MAY).
- How to propose spec changes.
- Test vectors.

### 5.2. `spec/events.md`

**Purpose:** Event format and serialization.  
**Contents:**
- Event envelope structure.
- Canonical serialization (CBOR).
- Hashing (BLAKE3).
- Signatures (Ed25519).
- Parent references (DAG).
- Event types (full list).
- Validation rules.

### 5.3. `spec/identity.md`

**Purpose:** Identity model.  
**Contents:**
- Key generation.
- DID format.
- Identity creation.
- Attestations.
- Verification levels.
- Key rotation.
- Social recovery.
- Multiple identities.

### 5.4. `spec/contribution.md`

**Purpose:** Contribution records.  
**Contents:**
- Contribution record format.
- Weight classes.
- Confirmation rules.
- Decay function.
- Revocation.
- Evidence handling.

### 5.5. `spec/reputation.md`

**Purpose:** Reputation calculation.  
**Contents:**
- Formula.
- Context definition.
- Quality coefficient.
- Decay function.
- Revocation coefficient.
- Caching and snapshots.
- Determinism requirements.

### 5.6. `spec/ledger.md`

**Purpose:** Ledger structure.  
**Contents:**
- DAG structure.
- Merkle trees.
- Checkpoints.
- Storage schema.
- Compression.

### 5.7. `spec/consensus.md`

**Purpose:** Consensus and validators.  
**Contents:**
- Validator roles.
- Finalization threshold.
- Rotation.
- Fork rules.
- Federation.

### 5.8. `spec/bounty.md`

**Purpose:** Bounty lifecycle.  
**Contents:**
- Creation.
- Escrow.
- Claim.
- Submit.
- Verify.
- Complete.
- Dispute and arbitration.
- Payment recording.

### 5.9. `spec/vote.md`

**Purpose:** Voting.  
**Contents:**
- Proposal creation.
- Options.
- Quadratic weight.
- Delegation.
- Snapshot.
- Tallying.
- Secret voting (ZK).
- Veto.

### 5.10. `spec/compute.md`

**Purpose:** Compute tasks.  
**Contents:**
- Task format.
- Claim and staking.
- Submission.
- Verification (redundancy, sampling, ZK).
- Payment.
- Anti-abuse.

### 5.11. `spec/sync.md`

**Purpose:** P2P synchronization.  
**Contents:**
- libp2p integration.
- Gossip protocol.
- Header exchange.
- Missing event request.
- Conflict resolution.

### 5.12. `spec/api.md`

**Purpose:** API endpoints.  
**Contents:**
- REST endpoints.
- WebSocket subscriptions.
- gRPC services.
- Authentication.
- Rate limits.

### 5.13. `spec/privacy.md`

**Purpose:** Privacy features.  
**Contents:**
- Selective disclosure.
- ZK proofs.
- Private contexts.
- Encryption.
- Data minimization.

### 5.14. `spec/test-vectors/`

**Purpose:** Test vectors for implementation compatibility.  
**Contents:**
- `events.json` — canonical serialization examples.
- `reputation.json` — reputation calculation examples.
- `votes.json` — voting tally examples.
- `README.md` — how to use the vectors.

**Rule:** Any two implementations must produce identical results on these vectors.

---

## 6. rfcs/ — Requests for Comments

The RFC process is how significant changes are proposed and decided.

### 6.1. `rfcs/README.md`

**Purpose:** RFC process overview.  
**Contents:**
- When to write an RFC.
- How to write one.
- RFC states (Draft, Discussion, Accepted, Rejected, Withdrawn, Superseded).
- How decisions are made.

### 6.2. `rfcs/0000-template.md`

**Purpose:** Template for new RFCs.  
**Sections:**
- Summary.
- Motivation.
- Design.
- Alternatives.
- Drawbacks.
- Open questions.

### 6.3. Numbered RFCs

**Format:** `rfcs/NNNN-short-title.md`.  
**Example:** `rfcs/0001-federation-protocol.md`.

**Numbering:** Sequential. Never reuse a number. Rejected RFCs keep their number.

---

## 7. .github/ — GitHub Configuration

Standard GitHub files for issues, PRs, and automation.

### 7.1. `.github/ISSUE_TEMPLATE/`

| File | Purpose |
|---|---|
| `bug_report.md` | Template for bug reports |
| `feature_request.md` | Template for feature ideas |
| `rfc_proposal.md` | Template for RFC proposals |
| `config.yml` | Configures issue chooser |

### 7.2. `.github/PULL_REQUEST_TEMPLATE.md`

**Purpose:** Template for PRs.  
**Contents:**
- What changed.
- Why.
- How.
- References to issues/RFCs.
- Checklist.

### 7.3. `.github/workflows/`

| File | Purpose |
|---|---|
| `markdown-lint.yml` | Lint markdown files |
| `link-check.yml` | Check for broken links |
| `spellcheck.yml` | Spell check (optional) |
| `ci.yml` | Run tests (when code exists) |

**Rule:** Automate what can be automated. Do not make reviewers do it.

---

## 8. Future Directories

These directories do not exist yet. They will be added as the project grows.

### 8.1. `core/` — Reference Implementation

**Language:** Rust or Go.  
**Purpose:** The canonical implementation of the protocol.

```
core/
├── src/
│   ├── events/
│   ├── identity/
│   ├── reputation/
│   ├── ledger/
│   ├── consensus/
│   ├── bounty/
│   ├── vote/
│   └── compute/
├── tests/
├── benches/
├── Cargo.toml (or go.mod)
└── README.md
```

### 8.2. `clients/` — User-Facing Applications

```
clients/
├── web/                # TypeScript + React
├── mobile/             # React Native or Flutter
├── cli/                # Command-line interface
└── README.md
```

### 8.3. `tools/` — Utilities

```
tools/
├── ledger-explorer/    # Browse the ledger
├── event-inspector/    # Inspect events
├── migration/          # Migrate between versions
└── README.md
```

### 8.4. `examples/` — Sample Integrations

```
examples/
├── git-hook/           # Record commits to CL
├── telegram-bot/       # Bot for contribution tracking
├── cooperative/        # Example cooperative setup
└── README.md
```

### 8.5. `deploy/` — Deployment

```
deploy/
├── docker/
├── kubernetes/
├── systemd/
└── README.md
```

### 8.6. `security/` — Security

```
security/
├── audits/             # External audit reports
├── bug-bounty.md       # Bug bounty program
└── README.md
```

---

## 9. Naming Conventions

### 9.1. Files

- **Lowercase with hyphens.** `useful-work.md`, not `UsefulWork.md`.
- **Descriptive names.** `reputation.md`, not `rep.md`.
- **Translations use suffixes.** `whitepaper.ru.md`, `whitepaper.es.md`.
- **Test vectors use `.json`.**

### 9.2. Directories

- **Lowercase, plural where appropriate.** `docs/`, `rfcs/`, `spec/`.
- **No spaces.**
- **Short names.** `spec/`, not `technical-specification/`.

### 9.3. RFCs

- **Format:** `NNNN-short-title.md`.
- **NNNN** is 4-digit sequential.
- **short-title** uses hyphens.

### 9.4. Commits

See [CONTRIBUTING.md](../CONTRIBUTING.md#7-commit-message-convention).

- `docs:`, `spec:`, `rfc:`, `feat:`, `fix:`, `chore:`.

### 9.5. Branches

- `main` — stable.
- `dev` — integration (optional).
- `feature/short-name` — feature branches.
- `rfc/NNNN-short-title` — RFC branches.
- `fix/short-name` — bug fixes.

---

## 10. What Goes Where

A quick reference for where to put new content.

| Content | Location |
|---|---|
| New idea for the protocol | `rfcs/NNNN-title.md` |
| Technical detail of a feature | `spec/feature.md` |
| Explanation for newcomers | `docs/` |
| Question from a user | `docs/faq.md` |
| Term definition | `docs/glossary.md` |
| Comparison to another project | `docs/comparison.md` |
| New scheme for earning | `docs/economics.md` |
| Compute task details | `docs/useful-work.md` + `spec/compute.md` |
| Bug report | GitHub issue |
| Feature request | GitHub issue |
| Typo fix | Pull request |
| Translation | `docs/*.<lang>.md` |
| Code | `core/`, `clients/`, `tools/` |
| Test vectors | `spec/test-vectors/` |
| Security report | Email (see [CODE_OF_CONDUCT](../CODE_OF_CONDUCT.md)) |

### 10.1. Decision tree

**Is it a change to the protocol?**
- Yes → RFC.
- No → continue.

**Is it implementation detail?**
- Yes → `spec/`.
- No → continue.

**Is it explanation for readers?**
- Yes → `docs/`.
- No → continue.

**Is it a bug or feature request?**
- Yes → GitHub issue.
- No → discussion.

### 10.2. Common mistakes

| Mistake | Correct place |
|---|---|
| Putting technical details in whitepaper | `spec/` |
| Putting ideas in code comments | RFC or spec |
| Putting FAQ answers in README | `docs/faq.md` |
| Putting economy details in whitepaper | `docs/economics.md` |
| Putting roadmap in README | `docs/roadmap.md` |

---

## Summary

**Four areas:**

1. **Root** — entry points, rules, licenses.
2. **docs/** — conceptual documentation.
3. **spec/** — technical specification.
4. **rfcs/** — change proposals.

**Golden rules:**

- Whitepaper explains why. Spec explains how.
- Ideas go to RFCs. Details go to spec.
- FAQ answers questions. Glossary defines terms.
- Every contribution counts.

**When in doubt:** open an issue and ask. There are no stupid questions.

---

**Related documents:**

- [README](../README.md) — project overview.
- [CONTRIBUTING](../CONTRIBUTING.md) — how to help.
- [Whitepaper](./whitepaper.md) — full design.
- [Roadmap](./roadmap.md) — 5-year plan.

**License:** CC BY-SA 4.0

**Last updated:** 2025  
**Version:** 1.0

---

