# Roadmap

**Contribution Ledger — 5-year plan, from whitepaper to self-sustaining protocol.**

**Version:** 1.0  
**Status:** Living document  
**Related:** [Whitepaper](../docs/whitepaper.md) · [Economics](./economics.md) · [Useful Work](./useful-work.md)

---

## Table of Contents

1. [Principles](#1-principles)
2. [Overview](#2-overview)
3. [Year 1 — Foundation](#3-year-1--foundation)
4. [Year 2 — Pilot and Federation](#4-year-2--pilot-and-federation)
5. [Year 3 — Protocol v1.0](#5-year-3--protocol-v10)
6. [Year 4 — Ecosystem](#6-year-4--ecosystem)
7. [Year 5 — Sustainability](#7-year-5--sustainability)
8. [Milestones Summary](#8-milestones-summary)
9. [What Success Looks Like](#9-what-success-looks-like)
10. [What Failure Looks Like](#10-what-failure-looks-like)
11. [Risks and Pivots](#11-risks-and-pivots)
12. [What This Roadmap Is Not](#12-what-this-roadmap-is-not)

---

## 1. Principles

This roadmap follows five rules.

**1. Whitepaper first, code second.** No implementation without a specification. Otherwise, we rewrite everything twice.

**2. Community before scale.** Ten real users beat a thousand spectators.

**3. Verification before compute.** You cannot verify 1 000 tasks if you cannot verify 10.

**4. Money from outside.** No token, no emission, no speculation. Profit comes from clients, funds, and cooperatives.

**5. No promises of dates.** This is a plan, not a contract. Things slip. We say so.

---

## 2. Overview

| Year | Theme | Users | Key deliverable |
|---|---|---|---|
| 1 | Foundation | 10–50 | MVP, whitepaper, specification |
| 2 | Pilot and federation | 100–500 | Federated consensus, first bounties |
| 3 | Protocol v1.0 | 5 000–10 000 | Mobile client, compute pilot |
| 4 | Ecosystem | 20 000–50 000 | Integrations, self-funding |
| 5 | Sustainability | 100 000+ | Runs without the founder |

These are targets, not promises. Each year depends on the previous.

---

## 3. Year 1 — Foundation

**Goal:** Build the foundation. Prove the idea to 10–50 people.

### 3.1. Q1 — Whitepaper and specification

- [x] Whitepaper v1.2 (EN, RU).
- [x] README, CONTRIBUTING, CODE_OF_CONDUCT, FAQ, SUMMARY.
- [x] `docs/economics.md`, `docs/useful-work.md`, `docs/roadmap.md`.
- [ ] Technical specification:
  - `spec/events.md` — canonical serialization, event envelope.
  - `spec/identity.md` — keys, DID, attestations, recovery.
  - `spec/reputation.md` — formula, context, decay.
  - `spec/bounty.md` — lifecycle, escrow, arbitration.
  - `spec/vote.md` — proposals, quadratic weight, delegation.
  - `spec/compute.md` — tasks, verification, staking.
- [ ] Test vectors for the specification.
- [ ] RFC repository and template.

**Deliverable:** a complete, readable specification anyone can implement.

### 3.2. Q2 — MVP core

Minimal working node. Single instance. No P2P.

- [ ] Key generation (Ed25519).
- [ ] Event creation, signing, hashing (BLAKE3).
- [ ] Canonical serialization (CBOR).
- [ ] SQLite storage: `events`, `event_parents`.
- [ ] Basic state: identity, contribution, reputation.
- [ ] Minimal rules: `identity.create`, `contribution.create`, `contribution.confirm`.
- [ ] CLI for creating events and inspecting state.
- [ ] First test suite.

**Deliverable:** a node that runs, accepts events, and computes reputation.

### 3.3. Q3 — Web client and pilot

- [ ] REST API (5–7 endpoints).
- [ ] Web client: profile, add contribution, confirm, reputation.
- [ ] Docker image for easy deployment.
- [ ] Documentation for running a node.
- [ ] Pilot with 10 people:
  - one chat or project;
  - real contributions tracked;
  - feedback collected.

**Deliverable:** 10 people using CL for real work.

### 3.4. Q4 — Refinement and first co-authors

- [ ] Fix what the pilot broke.
- [ ] Publish pilot report: what worked, what did not.
- [ ] Recruit 2–3 co-authors.
- [ ] Open first RFCs based on pilot learnings.
- [ ] Begin work on P2P sync (design only).
- [ ] Write grant applications (NLnet, OTF).

**Deliverable:** a project with more than one person, and a pilot report.

### 3.5. Year 1 success criteria

- 10+ real users.
- 100+ verified contributions in the ledger.
- 2+ co-authors.
- Specification complete enough for a second implementation.
- First grant application submitted.

### 3.6. Year 1 risks

- **No users.** If no one uses the MVP, pivot to a different community.
- **Founder burnout.** Pace is a marathon, not a sprint.
- **Specification drift.** Keep spec and code in sync.
- **Grant rejection.** Apply to multiple funds.

---

## 4. Year 2 — Pilot and Federation

**Goal:** Move from a single node to a network. Reach 100–500 users.

### 4.1. Q1 — Federation design

- [ ] P2P sync design (libp2p).
- [ ] Federated consensus design.
- [ ] Validator selection and rotation rules.
- [ ] Cross-ledger attestation format.
- [ ] RFC: federation protocol.

**Deliverable:** a design for multiple ledgers to interoperate.

### 4.2. Q2 — P2P and federation MVP

- [ ] libp2p integration.
- [ ] Gossip protocol for events.
- [ ] Header exchange and sync.
- [ ] Federated finalization (2/3 threshold).
- [ ] Two nodes, one federation, in test.

**Deliverable:** two independent nodes sharing a ledger.

### 4.3. Q3 — Bounties and payments

- [ ] Bounty lifecycle: create, claim, submit, verify, complete.
- [ ] Escrow via multisig.
- [ ] Fiat integration (Stripe or Wise).
- [ ] Arbitration: random auditor selection, voting.
- [ ] First real bounty: $50–500.

**Deliverable:** first money paid to a contributor through CL.

### 4.4. Q4 — First communities and legal entity

- [ ] 3–5 pilot communities:
  - open-source project;
  - cooperative;
  - volunteer group;
  - student club;
  - local community.
- [ ] Legal entity: foundation or cooperative.
- [ ] Terms of service, privacy policy.
- [ ] First security audit (external, even if basic).
- [ ] Grant received (target: $20 000–100 000).

**Deliverable:** a functioning federation with real communities.

### 4.5. Year 2 success criteria

- 100–500 users across 3–5 communities.
- 1 000+ verified contributions.
- First bounty paid ($50–500).
- Legal entity established.
- First external security audit completed.
- At least one grant received.

### 4.6. Year 2 risks

- **Federation is harder than expected.** Consensus bugs, network issues.
- **Legal complexity.** Different jurisdictions for different communities.
- **Audit cost.** Security audits are expensive.
- **Community conflicts.** Rules disagreements between communities.
- **Grant delays.** Funding may arrive later than planned.

---

## 5. Year 3 — Protocol v1.0

**Goal:** Stabilize the protocol. Reach 5 000–10 000 users. Launch compute pilot.

### 5.1. Q1 — Privacy and ZK

- [ ] Selective disclosure of reputation.
- [ ] ZK proofs for "reputation > X" without revealing all contributions.
- [ ] Private contexts (encrypted events).
- [ ] RFC: privacy model.

**Deliverable:** privacy-preserving reputation.

### 5.2. Q2 — Mobile client and SDK

- [ ] Mobile app (React Native or Flutter):
  - profile;
  - contributions;
  - bounties;
  - votes.
- [ ] SDK for third-party integrations.
- [ ] Integration: Git (GitHub, GitLab, Gitea).

**Deliverable:** CL in your pocket, CL in your repository.

### 5.3. Q3 — Compute pilot

- [ ] Compute task format (see `spec/compute.md`).
- [ ] Small-task scheduler.
- [ ] First tasks: rendering, simulation, test runs.
- [ ] Verification via redundancy + sampling.
- [ ] First paying compute client.

**Deliverable:** compute tasks working on a small scale.

### 5.4. Q4 — Protocol v1.0 freeze

- [ ] Protocol v1.0 frozen.
- [ ] Test vectors published.
- [ ] Second independent implementation (any language).
- [ ] Second security audit.
- [ ] Documentation complete.
- [ ] 5 000–10 000 users.

**Deliverable:** a stable protocol anyone can implement.

### 5.5. Year 3 success criteria

- 5 000–10 000 users.
- Protocol v1.0 frozen.
- Two independent implementations.
- Mobile client.
- Compute pilot with real clients.
- Second security audit.
- Sustainable funding (grants + community dues).

### 5.6. Year 3 risks

- **ZK proofs are expensive.** May not be feasible for all use cases.
- **Mobile complexity.** Two platforms, two bugs.
- **Compute verification fails at scale.** Fall back to Phase 2 tasks.
- **Protocol drift.** Freeze is harder than expected.
- **Founder still central.** Bus factor = 1 is a problem.

---

## 6. Year 4 — Ecosystem

**Goal:** Grow the ecosystem. Reach 20 000–50 000 users. Achieve self-funding.

### 6.1. Q1 — Standardization

- [ ] RFC process mature.
- [ ] Interop tests between implementations.
- [ ] Published standard (IETF-style draft or equivalent).
- [ ] Specification translated to major languages.

**Deliverable:** CL as a documented standard, not a single project.

### 6.2. Q2 — Integrations

- [ ] Messengers: Telegram, Discord, Matrix bots.
- [ ] LMS: Moodle, Canvas for education.
- [ ] CRM: for cooperatives and client work.
- [ ] Payment processors: expand fiat rails.
- [ ] Compute: Kubernetes, Ray, Slurm integrations.

**Deliverable:** CL reachable from tools people already use.

### 6.3. Q3 — Self-funding

- [ ] Community dues model mature.
- [ ] Grant funding reduced to <50% of budget.
- [ ] First paid support contracts.
- [ ] First paid integrations.
- [ ] Reserve fund established.

**Deliverable:** the project no longer depends solely on grants.

### 6.4. Q4 — Governance transition

- [ ] Foundation or cooperative board elected.
- [ ] Maintainers from multiple organizations.
- [ ] RFC process fully community-driven.
- [ ] Founder role reduced to contributor.

**Deliverable:** governance distributed beyond the founder.

### 6.5. Year 4 success criteria

- 20 000–50 000 users.
- 10+ communities.
- Two or more independent implementations.
- Self-funding achieved (<50% grants).
- Board of 5+ members.
- Founder not a bottleneck.

### 6.6. Year 4 risks

- **Growth overwhelms moderation.** Community management is hard.
- **Governance conflicts.** Power struggles during transition.
- **Funding instability.** Grants end; dues must cover.
- **Technical debt.** Early design choices limit scale.
- **Competition.** Another project with a token attracts users.

---

## 7. Year 5 — Sustainability

**Goal:** The project runs without the founder. 100 000+ users. Fully decentralized governance.

### 7.1. Q1 — Founder transition

- [ ] Founder steps back from day-to-day.
- [ ] Successor maintainers in place.
- [ ] Founder retains advisory role (optional).
- [ ] No single point of failure in governance.

**Deliverable:** founder not required for the project to run.

### 7.2. Q2 — Decentralized governance

- [ ] Council elected by users, not appointed.
- [ ] Budget approved by community vote.
- [ ] RFCs decided by rough consensus across implementations.
- [ ] Multiple foundations in different jurisdictions.

**Deliverable:** governance distributed across the network.

### 7.3. Q3 — Compute at scale

- [ ] AI training tasks at scale.
- [ ] 1 000+ GPUs in the network.
- [ ] Real AI clients.
- [ ] Verification robust under adversarial conditions.
- [ ] Federated learning pilot.

**Deliverable:** CL as a real compute market.

### 7.4. Q4 — Long-term viability

- [ ] Sustainable funding model proven over 2 years.
- [ ] Multiple independent teams.
- [ ] Protocol unchanged (or changed by RFC).
- [ ] Community healthy, not dependent on any single person.
- [ ] Next 5-year plan drafted by the community.

**Deliverable:** a project that will outlive its founder.

### 7.5. Year 5 success criteria

- 100 000+ users.
- Founder not required for daily operation.
- Decentralized governance in place.
- Compute at scale (1 000+ GPUs).
- Sustainable funding for 2+ years.
- Multiple independent implementations.
- Healthy community.

### 7.6. Year 5 risks

- **Founder cannot let go.** Common failure mode.
- **Governance capture.** A faction takes over.
- **Compute market fails.** Falls back to Phase 2.
- **Legal attack.** Regulatory pressure on some jurisdiction.
- **Fork.** Community splits; two projects.
- **Stagnation.** No new contributors; slow decay.

---

## 8. Milestones Summary

| Milestone | Target date | Year |
|---|---|---|
| Whitepaper v1.2 | Done | 1 |
| Technical specification | Q1 | 1 |
| MVP node | Q2 | 1 |
| Web client | Q3 | 1 |
| First 10 users | Q3 | 1 |
| First co-authors | Q4 | 1 |
| Federation MVP | Q2 | 2 |
| First bounty paid | Q3 | 2 |
| Legal entity | Q4 | 2 |
| First security audit | Q4 | 2 |
| Protocol v1.0 | Q4 | 3 |
| Mobile client | Q2 | 3 |
| Compute pilot | Q3 | 3 |
| 5 000 users | Q4 | 3 |
| Standard published | Q1 | 4 |
| Self-funding | Q3 | 4 |
| Founder transition | Q1 | 5 |
| Decentralized governance | Q2 | 5 |
| Compute at scale | Q3 | 5 |
| 100 000 users | Q4 | 5 |

---

## 9. What Success Looks Like

### 9.1. Technical

- Two or more independent implementations.
- Protocol stable for 2+ years.
- No critical security incidents.
- Compute verified at scale.
- Federation across 10+ communities.

### 9.2. Social

- 100 000+ active users.
- Communities in 20+ countries.
- 5+ languages supported.
- No single point of failure (technical or social).
- Founder not required for daily operation.

### 9.3. Economic

- Sustainable funding for 2+ years.
- Multiple revenue sources.
- No token, no speculation.
- Real money flowing from clients to contributors.
- Grants <50% of budget by Year 4.

### 9.4. Mission

- CU is non-transferable. Always.
- Reputation cannot be bought. Always.
- No token. Ever.
- The project outlives its founder.

---

## 10. What Failure Looks Like

We will be honest about this.

### 10.1. Failure modes

**Mode A — No users.**  
The MVP works, but no one uses it. The project fades.

**Mode B — Founder burnout.**  
One person cannot sustain 5 years. The project stalls.

**Mode C — Grant dependency.**  
Grants fund it, then stop. No self-sustaining model. Death.

**Mode D — Legal shutdown.**  
A regulator targets a key jurisdiction. Nodes go down. Community scatters.

**Mode E — Governance capture.**  
A faction seizes the project. Community forks. Original fades.

**Mode F — Technical failure.**  
Federation does not work. Compute verification fails. Protocol stalls.

**Mode G — Token temptation.**  
A fork adds a token. It attracts all users. Original is forgotten.

### 10.2. What remains after failure

Even if the project fails:

- The whitepaper remains.
- The code remains.
- The ideas remain.
- The pilot data remains.
- The community that formed remains.

Failure in the open is still useful. Others can learn from it and try again.

### 10.3. When to stop

We will consider stopping if:

- After 18 months: no users beyond the founder and co-authors.
- After 3 years: no sustainable funding.
- After 4 years: no second implementation.
- Anytime: security cannot be guaranteed.

**Stopping is not failure. Continuing a dead project is.**

---

## 11. Risks and Pivots

### 11.1. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| No users | Medium | High | Pilot with real communities early |
| Founder burnout | High | High | Recruit co-authors Year 1 |
| Grant rejection | Medium | Medium | Apply to many funds |
| Legal attack | Low | High | Multiple jurisdictions |
| Fork with token | Medium | High | Community rejects it |
| Compute fails | Medium | Medium | Fall back to Phase 2 |
| Governance capture | Medium | High | Fork rights, rotation |
| Technical debt | High | Medium | Freeze spec early |
| Competition | High | Medium | Differentiation: no token |
| Economic model fails | Medium | High | Multiple revenue sources |

### 11.2. Pivot options

If the original plan fails, we can pivot to:

**Pivot A — Focus on community help only.**  
Drop compute. Focus on contribution tracking for communities.

**Pivot B — Focus on one vertical.**  
Pick one industry (open-source, cooperatives, education) and go deep.

**Pivot C — Become a library, not a protocol.**  
Provide tools for others to build their own ledgers.

**Pivot D — Become an archive.**  
Publish everything as a research artifact and stop active development.

**Pivot E — Merge with an existing project.**  
If another project shares the vision, merge efforts.

### 11.3. When to pivot

- If after 12 months the pilot shows no traction → Pivot A or B.
- If after 24 months no funding → Pivot C.
- If after 36 months no second implementation → Pivot D.
- Anytime if the vision is compromised → Pivot E.

---

## 12. What This Roadmap Is Not

### 12.1. It is not a promise

Dates are targets, not commitments. Things slip. We will update this document.

### 12.2. It is not a business plan

CL is not a company. It is a protocol. There is no revenue model in the usual sense.

### 12.3. It is not a guarantee of success

Most projects like this fail. We might too. We are honest about this.

### 12.4. It is not a token roadmap

There is no token. There will be no token. Do not ask.

### 12.5. It is not fixed

This document will change. The community will shape it. What you read today may be different in 6 months.

### 12.6. It is not the only path

If you see a better path, write an RFC. This roadmap is a starting point, not a doctrine.

---

## Summary

**Five years. Five phases.**

1. **Foundation** — whitepaper, spec, MVP, first 10–50 users.
2. **Pilot and federation** — 100–500 users, first bounties, legal entity.
3. **Protocol v1.0** — 5 000–10 000 users, mobile, compute pilot.
4. **Ecosystem** — 20 000–50 000 users, integrations, self-funding.
5. **Sustainability** — 100 000+ users, decentralized governance.

**Five principles:**

1. Whitepaper first, code second.
2. Community before scale.
3. Verification before compute.
4. Money from outside.
5. No promises of dates.

**Five risks:**

1. No users.
2. Founder burnout.
3. Grant dependency.
4. Legal attack.
5. Fork with a token.

**Five success markers:**

1. Two or more implementations.
2. Sustainable funding.
3. Decentralized governance.
4. Real compute at scale.
5. The project outlives its founder.

---

**Related documents:**

- [Whitepaper](../docs/whitepaper.md) — full design.
- [Economics](./economics.md) — how participants earn.
- [Useful Work](./useful-work.md) — compute and community help.
- [FAQ](./faq.md) — common questions.
- [CONTRIBUTING](../CONTRIBUTING.md) — how to help.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 1.0

---
