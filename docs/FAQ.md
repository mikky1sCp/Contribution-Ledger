# Frequently Asked Questions

## Contribution Ledger

**Version:** 1.0  
**Last updated:** 2026

This FAQ answers the most common questions about Contribution Ledger (CL). If your question is not here, open a [Discussion](../../discussions) or an [Issue](../../issues) labeled `question`.

---

## Table of Contents

1. [The basics](#1-the-basics)
2. [Why not a cryptocurrency](#2-why-not-a-cryptocurrency)
3. [How people earn](#3-how-people-earn)
4. [Contribution Units (CU)](#4-contribution-units-cu)
5. [Identity and privacy](#5-identity-and-privacy)
6. [Reputation](#6-reputation)
7. [Bounties and payments](#7-bounties-and-payments)
8. [Useful work and compute](#8-useful-work-and-compute)
9. [Governance](#9-governance)
10. [Technical questions](#10-technical-questions)
11. [Project status](#11-project-status)
12. [How to help](#12-how-to-help)
13. [Criticism and doubts](#13-criticism-and-doubts)
14. [Comparison to other projects](#14-comparison-to-other-projects)
15. [Legal](#15-legal)

---

## 1. The basics

### 1.1. What is Contribution Ledger?

Contribution Ledger is an open, decentralized ledger that records what people contribute to communities — code, reviews, mentorship, moderation, compute. It is not a cryptocurrency. It has no token, no exchange, no speculation.

Think of it as a public record of who did what, owned by no one, buyable by no one.

### 1.2. Why does it exist?

Because today, your reputation belongs to platforms:

- Lose your GitHub account — lose your history.
- Leave Upwork — start from zero.
- Get banned on a forum — no appeal.
- Pay 10–30% in fees to intermediaries.

CL gives you a record of your contribution that is **signed, portable, and permanent**.

### 1.3. Is it a blockchain?

No. It uses some of the same ideas — hash-linked events, Merkle proofs, distributed consensus — but it is not a blockchain in the usual sense.

CL uses a **DAG** (directed acyclic graph) instead of a linear chain of blocks. There is no mining, no blocks in the Bitcoin sense, and no chain of hashes representing money.

"Blockchain" is a tool. CL uses parts of it, not all of it.

### 1.4. Who is building it?

It started as a solo project by [mikky1sCp](https://github.com/mikky1sCp). It is open to contributors. See [CONTRIBUTING.md](./CONTRIBUTING.md).

### 1.5. When will it launch?

There is no launch date. The whitepaper is a draft. The implementation has not started. We do not promise timelines.

If you want to help make it real, see [Section 12](#12-how-to-help).

---

## 2. Why not a cryptocurrency

### 2.1. Why no token?

Because a token changes the project's nature.

Once there is a transferable token:

- People buy it to speculate.
- The price becomes the focus.
- Early buyers get rich at the expense of late ones.
- Governance is captured by whales.
- Scammers appear.
- Regulators take interest.
- The mission shifts from "record contribution" to "pump the token".

CL is not against money. It is against **money that comes from speculation instead of work**.

### 2.2. But how will people be motivated without a token?

Through real profit from real work:

- **Bounties** — paid tasks.
- **Grants** — funding by verified contribution.
- **Cooperative payouts** — revenue share by CU.
- **Work** — a verifiable portfolio that gets you hired.
- **Roles** — paid positions earned through reputation.
- **Savings** — no 10–30% platform fees.

See [Section 3](#3-how-people-earn) for details, and [docs/economics.md](./docs/economics.md) for the full scheme.

### 2.3. Isn't this just a "fair launch" without a token?

No. A fair launch still launches a token. CL does not.

The closest analogy is a **professional guild** or a **cooperative**: you earn standing by doing work, and standing gives you access to opportunities.

### 2.4. What if someone forks CL and adds a token?

They can. The code will be open. The license allows forks.

But that fork is a different project. It is not CL. The CL community will not recognize it, will not merge it, and will not support it.

**The no-token rule is not a technical limitation — it is a definition.** Remove it, and you are building something else.

### 2.5. Can CU be traded on a DEX or wrapped?

Technically, someone could try. But:

- CU are bound to an identity.
- They are non-transferable at the protocol level.
- Wrapping requires a custodian who controls the identity.
- Such a custodian would break the protocol rules.

If this happens, the community can revoke the CU, ban the custodian, and fork the ledger.

### 2.6. What about stablecoins for payments?

Stablecoins may be used to **pay for work** — like any other currency. They are not part of the protocol. They are a payment rail.

The distinction:

- **CU** — non-transferable, protocol-level, cannot be bought.
- **Stablecoins** — transferable, external, used to pay for real work.

CL does not issue stablecoins. It records payments. The actual money moves outside.

---

## 3. How people earn

### 3.1. How do I make money with CL?

Eight ways:

1. **Bounties** — organizations post tasks, you complete them, you get paid.
2. **Work via reputation** — your CL profile gets you hired.
3. **Grants** — funds give money to verified contributors.
4. **Cooperative payouts** — you get a share of cooperative revenue.
5. **Paid communities** — your access has value; you may receive grants from dues.
6. **Roles** — auditor, maintainer, curator — paid positions.
7. **Savings** — no platform fees (10–30% saved).
8. **Reputation as capital** — investors fund you because you are trusted.

See [docs/economics.md](./docs/economics.md) for amounts and examples.

### 3.2. How much can I earn?

It depends on what you do.

| Source | Range |
|---|---|
| Bounties | $20–10 000 per task |
| Work via reputation | Salary, typically 2–10× better than anonymous |
| Grants | $5 000–500 000 |
| Cooperative payouts | Share of revenue |
| Roles | $5 000–50 000 per contract |
| Compute tasks | $0.10–10 per hour |

These are not promises. They are examples of what is possible in a functioning community.

### 3.3. Is this passive income?

No. There is no passive income in CL.

You cannot buy CU and earn interest. You cannot stake and earn yield. You cannot rent out reputation.

**Everything is earned by work.** If you do not work, you do not earn.

### 3.4. Can I invest in CL?

No. There is nothing to invest in.

There is no token, no equity, no shares. You can **contribute** — write code, translate, criticize — but you cannot buy a stake.

If CL later becomes a foundation or cooperative, membership may be possible. It will not be for sale.

### 3.5. What if the community has no money?

Then there will be no money to distribute.

CL is not a money printer. It is a coordination layer. If a community has no clients, no grants, no revenue, then there is nothing to pay out.

This is honest. Many communities will be poor. Some will be rich. CL does not change that — it only makes distribution fairer when there is something to distribute.

---

## 4. Contribution Units (CU)

### 4.1. What is a CU?

A Contribution Unit is a **non-transferable** record of verified contribution. It is not money. It is not a token. It cannot be bought or sold.

### 4.2. How do I earn CU?

By doing verified work:

- Writing code.
- Reviewing code.
- Writing documentation.
- Moderating.
- Mentoring.
- Translating.
- Testing.
- Completing bounties.
- Contributing compute.
- Helping the community.

Each community defines its own list and its own weights.

### 4.3. Can I transfer CU to someone else?

No. This is forbidden at the protocol level.

Any tool that enables CU transfer is incompatible with CL.

### 4.4. Can I sell CU?

No.

### 4.5. Can I buy CU?

No.

### 4.6. Can I lose CU?

Yes, in two ways:

1. **Decay.** CU can decay over time (if the community enables it). This prevents frozen power.
2. **Revocation.** If a contribution is found fraudulent, harmful, or erroneous, it can be revoked. CU are deducted.

History is preserved. But the CU are gone.

### 4.7. What can I do with CU?

- Build reputation.
- Unlock roles.
- Vote in governance.
- Receive cooperative payouts.
- Get priority in bounties and grants.

CU are a means, not an end.

### 4.8. Are CU like shares?

No. Shares represent ownership and can be sold. CU represent contribution and cannot be sold.

CU give you a share of **revenue** in a cooperative, but only through the cooperative's rules — not through a market.

### 4.9. Is CU a security?

No. It cannot be bought, sold, or transferred. It does not represent ownership. It does not pay dividends.

We will seek legal review before any public launch. See [Section 15](#15-legal).

---

## 5. Identity and privacy

### 5.1. Do I need to reveal my real name?

No. You can be pseudonymous.

But some communities may require verification for certain rights (voting, bounties, grants). The protocol allows this. It does not require it.

### 5.2. What data is stored about me?

Only what is necessary:

- Your DID (a public key).
- Hashes of evidence for contributions.
- Signatures.
- Metadata (type of contribution, weight, timestamp).
- Votes.
- Payment records (amount, no personal data).

**Not stored:** your name, email, passport, biometrics, private messages, bank details.

### 5.3. What is a DID?

A Decentralized Identifier. It is a public key that acts as your identity in the system. It contains no personal data.

Example: `did:cl:main:7Xk9fQ2mNpL3vR8sT1wY6zA4bC5dE6fG`

### 5.4. Can I have multiple identities?

Yes. You can have different DIDs for different communities. Linking them is optional.

### 5.5. What if I lose my key?

CL supports social recovery: 3 of 5 trusted contacts can help you recover access. There is also multisig recovery and offline backup.

Losing a key should not mean losing your reputation.

### 5.6. Can I delete my data?

You cannot delete events from the ledger — that is the point. But you can:

- Revoke evidence links.
- Request that private data be removed from external storage.
- Start a new identity.

The ledger records that a contribution happened. It does not need to record the content of the contribution. Evidence can be external and removable.

### 5.7. Is this GDPR-compliant?

We will design for GDPR compliance from the start. Personal data stays off-ledger. What remains on-ledger is pseudonymous and minimal.

Full legal review is a future step. See [Section 15](#15-legal).

### 5.8. Can I be anonymous?

Fully anonymous identities have limited rights. This is intentional.

Anonymous accounts are easy to create in bulk (Sybil attacks). To participate meaningfully — vote, confirm, receive bounties — you need some form of verification, whether through invitation, organization, or community attestation.

The level of anonymity is set by each community.

---

## 6. Reputation

### 6.1. How is reputation calculated?

Reputation is a weighted sum of your CU, with:

- Contribution weight.
- Quality (confirmations, disputes).
- Decay over time.
- Context (which community).

Formula:

```
R(u, c, t) = Σ w_i * q_i * d(t - t_i) * s_i
```

See [Section 9 of the whitepaper](./docs/whitepaper.md#9-reputation-model).

### 6.2. Is reputation global or per community?

**Per community.** Reputation in project X is not reputation in project Y.

Communities can recognize each other's reputation by agreement. This is federation.

### 6.3. Can reputation be bought?

No.

### 6.4. Can reputation be transferred?

No.

### 6.5. Can reputation decay?

Yes, if the community enables it. Decay prevents frozen power and encourages ongoing contribution. Half-life is typically 2 years.

### 6.6. What does reputation give me?

- Vote weight.
- Right to confirm contributions.
- Access to roles.
- Priority in bounties and grants.
- Right to create projects.
- Right to audit.

Reputation does **not** give you:
- The right to sell it.
- The right to transfer it.
- Absolute power.

### 6.7. Can I delegate my vote?

Yes. You can delegate your vote to someone you trust. Delegation is temporary, revocable, and does not transfer reputation.

---

## 7. Bounties and payments

### 7.1. What is a bounty?

A bounty is a paid task posted by an organization. Example: "Write API documentation — $500".

You claim it, complete it, get it confirmed, get paid.

### 7.2. How do I get paid?

The task issuer pays in fiat or stablecoin. CL records the payment but does not move money itself.

Fiat payments go through external providers (Stripe, Wise). Crypto payments go through external wallets. CL stores only the record.

### 7.3. What if the issuer doesn't pay?

Bounties use **escrow**: funds are locked before the task starts. They are released only on completion (or by arbitration).

If the issuer does not fund escrow, do not do the work.

### 7.4. What if I do the work poorly?

The community confirms contributions. If your work does not meet requirements, it is not confirmed, and you are not paid.

Repeated poor work affects your reputation.

### 7.5. How are disputes resolved?

Through **arbitration**:

1. A dispute is opened.
2. Three auditors are chosen randomly (high reputation in the context).
3. They vote.
4. The decision is final.

Auditors receive a small percentage of the disputed amount.

### 7.6. Who pays for arbitration?

A small fee from the disputed amount. This discourages frivolous disputes.

### 7.7. Can I cancel a bounty after claiming it?

Yes, with a reputation penalty. Repeated cancellations reduce your ability to claim future bounties.

---

## 8. Useful work and compute

### 8.1. What is "useful work"?

Instead of mining (burning energy on hashes), CL participants can contribute:

- **Compute power** — AI training, inference, simulations, rendering.
- **Community help** — moderation, translation, verification, mentoring.
- **Network support** — relays, storage, indexing.

Verified results earn CU. Task issuers pay in money.

### 8.2. How is this different from mining?

Mining produces nothing useful. It only secures the network.

Useful work produces a result that someone needs. It is verified, not wasted.

### 8.3. How do you verify that compute work was done honestly?

Five methods:

1. **Redundancy** — the same task is given to 3 executors. Results must match.
2. **Sampling** — 5% of tasks are audited manually.
3. **Cryptographic proofs** — for some tasks (ZK computations).
4. **Reputation** — new executors are checked strictly; experienced ones less so.
5. **Reference comparison** — known correct answers for test tasks.

For AI training: task = training, metric = validation set performance. If the model achieves the claimed quality, the work is credited.

### 8.4. Can I mine CL?

No. There is no mining. There is no block reward. There is no hash race.

### 8.5. What hardware do I need?

For community help: nothing special, just a computer.

For compute tasks: depends on the task. Consumer GPUs can earn $0.10–0.50/hour. Datacenter GPUs $1–5/hour.

### 8.6. Can I cheat the compute system?

You can try. The system is designed against it:

- Redundancy and sampling.
- CU staking (not money) for task claims, slashed on fraud.
- Rate limits for new accounts.
- Public audit trail.

Anyone caught cheating loses reputation and CU.

---

## 9. Governance

### 9.1. Who runs CL?

No single person or organization. The project is open. Decisions are made by rough consensus among contributors.

Once CL is live, communities govern themselves.

### 9.2. How are decisions made?

- Small changes: PR review by maintainers.
- Medium changes: issue + discussion.
- Large changes: RFC process.
- Protocol changes: consensus among maintainers, with public discussion.

See [CONTRIBUTING.md](./CONTRIBUTING.md).

### 9.3. What is quadratic voting?

A voting system where your vote weight is the square root of your reputation:

```
vote = sign(v) * sqrt(R)
```

This prevents whales from dominating. Doubling your reputation only gives 1.41× more vote weight.

### 9.4. Can someone take over CL?

The project is open. Anyone can fork.

If a group tries to capture the official repository, the community can:

- Fork the code.
- Fork the ledger.
- Continue under a new name.

This is a feature, not a bug.

### 9.5. What if the founder goes rogue?

The founder has no special power in the protocol. If the founder acts against the community, the community can fork and leave.

The founder's only power is social — the ability to influence discussion. This fades if it is abused.

### 9.6. How are validators chosen?

By the community. Criteria: technical reliability, reputation, independence, availability.

Validators cannot be bought. They rotate regularly.

---

## 10. Technical questions

### 10.1. What language is the reference implementation in?

Planned: **Rust** or **Go** for the core. **TypeScript** for the web client.

See [Section 18 of the whitepaper](./docs/whitepaper.md#18-architecture-and-stack).

### 10.2. What consensus does CL use?

Federated consensus with reputational validators. Not PoW, not PoS.

See [Section 11 of the whitepaper](./docs/whitepaper.md#11-consensus-and-validators).

### 10.3. What cryptography does CL use?

- **Ed25519** — signatures.
- **X25519** — key exchange.
- **BLAKE3** — hashing.
- **SHA-256** — for external compatibility.
- **ChaCha20-Poly1305** — encryption.
- **Bulletproofs** — optional ZK proofs.

We do not invent cryptography. We use established libraries.

### 10.4. Can CL scale?

Yes, via:

- DAG structure (parallel writes).
- Checkpoints (compressed history).
- Light nodes (headers only).
- Federation (multiple ledgers).

Scaling to millions of users is a research question. Scaling to thousands is feasible.

### 10.5. Can I run a node?

Yes, once the implementation exists. Full nodes store the entire ledger. Light nodes store headers only.

### 10.6. Can I build on CL?

Yes. The API will be open. You can build:

- Web clients.
- Mobile apps.
- Git integrations.
- Bots for Telegram, Discord, Slack.
- Compute schedulers.

### 10.7. Is there a testnet?

Not yet. There is no code. When code exists, there will be a testnet.

### 10.8. What is a checkpoint?

A signed snapshot of the ledger state. It allows light nodes to verify without downloading the whole history.

### 10.9. What happens if two validators disagree?

The DAG allows parallel events. Conflicts are resolved by:

- Time (earlier wins).
- Context rules (who has the right).
- Voting, if rules do not cover the case.

### 10.10. What if a validator goes offline?

If the threshold (2/3) is still met by other validators, the ledger continues. If not, finalization pauses until validators return or are replaced.

---

## 11. Project status

### 11.1. What stage is CL in?

**Whitepaper stage.** Draft v1.2 exists. Implementation has not started.

### 11.2. What exists now?

- Whitepaper (EN, RU).
- README.
- CONTRIBUTING, CODE_OF_CONDUCT, FAQ.
- Planned: specification, RFCs, reference implementation.

### 11.3. What does not exist?

- No code.
- No testnet.
- No mainnet.
- No token (never will).
- No community (yet).
- No funding (yet).

### 11.4. What is the roadmap?

Five years:

1. **Year 1** — whitepaper, specification, MVP, first 10–50 users.
2. **Year 2** — federation, 100–500 users, first bounties and grants.
3. **Year 3** — protocol v1.0, mobile, 5–10k users.
4. **Year 4** — ecosystem, integrations, compute pilot.
5. **Year 5** — decentralized governance, project runs without the founder.

See [docs/roadmap.md](./docs/roadmap.md).

### 11.5. How likely is success?

Honest answer: **uncertain**.

Many projects like this fail. The reasons:

- No users.
- No funding.
- Founder burnout.
- Technical challenges.
- Community conflicts.
- Legal issues.

We are not promising success. We are trying, in the open, and inviting others to try with us.

### 11.6. What if it fails?

Then the whitepaper, the code, and the ideas remain. Others can learn from them. Some may fork and succeed where we did not.

Failure in the open is still useful.

---

## 12. How to help

### 12.1. I can't code. Can I still help?

Yes. We need:

- **Critics** — find flaws in the design.
- **Translators** — RU → EN → other languages.
- **Writers** — improve clarity.
- **Community organizers** — run pilots.
- **Legal experts** — review risks.
- **Economists** — review incentives.

### 12.2. I can code. Where do I start?

1. Read the whitepaper.
2. Read [CONTRIBUTING.md](./CONTRIBUTING.md).
3. Check [Issues](../../issues) for `good first issue`.
4. Open a discussion before starting large work.

### 12.3. Can I run a pilot in my community?

Yes. Open an issue describing:

- Which community.
- How many people.
- What you want to track.
- What you expect.

We will help design the pilot.

### 12.4. Can I fund the project?

Not yet. We are not accepting donations until there is a legal entity and a clear plan.

If you want to help financially later, watch the repository.

### 12.5. Can I be paid to work on CL?

Not at this stage. There is no funding.

If funding arrives (grants, donations), it will be distributed by contribution — using the same principles CL proposes.

### 12.6. How do I stay updated?

- Watch the repository on GitHub.
- Follow [Discussions](../../discussions).
- Star the project if you find it interesting.

---

## 13. Criticism and doubts

### 13.1. "This will never work."

Maybe. You might be right.

The honest response: we do not know. We think the idea is worth trying. If you think it is not, tell us why — specifically. "It will fail" is not a critique. "It will fail because X, Y, Z" is.

### 13.2. "People only care about money."

Some do. Some do not.

CL is not for people who only want to speculate. It is for:

- Freelancers tired of platform fees.
- Maintainers who want portable reputation.
- Cooperatives that want fair distribution.
- Volunteers who want recognition.
- Communities that want independence.

If that is not enough people, the project fails. That is a real risk.

### 13.3. "Without a token, there is no incentive."

There are incentives:

- Money from bounties and grants.
- Better job prospects.
- Reputation as capital.
- Access to roles.
- Influence in governance.
- Savings on intermediaries.

These are real incentives. Whether they are enough is an open question.

### 13.4. "This is just a reputation system."

Partly. But reputation systems today are centralized and closed. CL is decentralized and open. That is a meaningful difference.

Also, CL adds:

- A ledger that cannot be rewritten.
- Cryptographic proofs.
- Federation across communities.
- Use of compute for useful work.
- Cooperative economics.

### 13.5. "You are reinventing the wheel."

We are **recombining** existing wheels. Satoshi did the same with Bitcoin.

Reinvention is not the goal. Useful recombination is.

### 13.6. "Who asked for this?"

No one, yet.

Most things no one asked for turn out to be useless. A few turn out to be essential.

We are betting on the latter. We may be wrong.

### 13.7. "This is too complex for normal people."

The **protocol** is complex. The **user experience** does not have to be.

A user should see:

- A profile.
- A list of contributions.
- A reputation score.
- Available bounties.
- Votes.

They should not need to know about DAGs, Merkle trees, or federated consensus.

Complexity is on the inside.

### 13.8. "Why not just use GitHub, LinkedIn, or Upwork?"

Because they own your reputation. You do not.

If GitHub changes its rules, your history changes. If Upwork bans you, your career suffers. If LinkedIn dies, your network dies.

CL is a way to own your record. It can be **added** to existing tools, not necessarily replace them.

### 13.9. "What about scammers, Sybils, and bots?"

They are a real problem. See [Section 15 of the whitepaper](./docs/whitepaper.md#15-threats-and-defenses).

No system solves this perfectly. CL uses:

- Invitations.
- Attestations.
- Rate limits.
- Redundancy.
- Staking (CU, not money).
- Reputation-based trust.

Perfect security is impossible. Better than current platforms is achievable.

---

## 14. Comparison to other projects

### 14.1. How is CL different from Bitcoin?

- Bitcoin is money. CL is not.
- Bitcoin has a token. CL does not.
- Bitcoin uses PoW. CL uses federated consensus.
- Bitcoin is anonymous. CL is pseudonymous with optional verification.
- Bitcoin has no useful work. CL does.
- Bitcoin has no reputation. CL is built on reputation.

### 14.2. How is CL different from Ethereum?

- Ethereum is a platform for tokens and contracts. CL is a ledger of contribution.
- Ethereum has gas fees. CL has no fees.
- Ethereum tokens are tradeable. CU are not.
- Ethereum governance is by token holders. CL governance is by reputation.

### 14.3. How is CL different from Gitcoin?

Gitcoin funds open-source work. CL records contribution.

Gitcoin uses tokens (GTC) and quadratic funding. CL uses no token and a different model.

Gitcoin could be built **on top of** CL as a funding layer.

### 14.4. How is CL different from Nostr?

Nostr is a protocol for social media. CL is a protocol for contribution.

Both are tokenless. Both are open. Both value decentralization.

Nostr tracks posts. CL tracks work.

They could complement each other.

### 14.5. How is CL different from Holochain?

Holochain is a framework for distributed apps. CL is a specific protocol.

Holochain is infrastructure. CL is an application of similar ideas.

### 14.6. How is CL different from LinkedIn?

LinkedIn is centralized, closed, and monetized by ads and premium. CL is decentralized, open, and tokenless.

LinkedIn shows what you claim. CL shows what is verified.

### 14.7. How is CL different from a DAO?

Most DAOs use tokens for governance. CL does not.

Most DAOs have plutocratic voting (1 token = 1 vote). CL uses quadratic voting with non-transferable reputation.

CL can be described as a **tokenless DAO** or a **cooperative**.

### 14.8. How is CL different from Bittensor?

Bittensor is a decentralized AI network with a token. CL is a contribution ledger without a token.

Bittensor pays for compute in tokens. CL pays for compute in money from task issuers.

CL is closer to a **compute marketplace** than to Bittensor.

### 14.9. How is CL different from Golem or iExec?

Golem and iExec are compute marketplaces with tokens. CL is a contribution ledger that includes compute as one type of work.

CL's primary purpose is recording contribution, not selling compute.

### 14.10. Is CL competing with any of these?

Not directly. Some are complementary.

CL could integrate with Git (for code), Nostr (for social), Golem (for compute), Gitcoin (for funding).

The idea is not to replace everything. It is to add a missing piece: **portable, non-transferable reputation**.

---

## 15. Legal

### 15.1. Is CL legal?

The concept is legal in most jurisdictions. It is a record-keeping system, not a financial instrument.

But: legal review is needed before any public launch. This has not happened yet.

### 15.2. Is CU a security?

No. CU cannot be bought, sold, or transferred. They do not represent ownership or profit-sharing in a company.

We will seek legal opinions to confirm this before launch.

### 15.3. Do I need to pay taxes on CU?

CU is not money. It cannot be converted to money. So typically, no — CU itself is not taxable.

But:

- **Bounties** paid in fiat or crypto — likely taxable as income.
- **Cooperative payouts** — likely taxable as income.
- **Grants** — rules depend on jurisdiction.

Consult a tax professional in your country.

### 15.4. What about GDPR?

Personal data stays off-ledger. What is on-ledger is pseudonymous and minimal.

We will design for GDPR compliance from the start. Full legal review is a future step.

### 15.5. Can governments shut it down?

They can shut down specific servers, organizations, or websites. They cannot shut down the protocol.

If one node goes down, others continue. If one community is banned, others remain.

This is not a promise of immunity. It is a property of decentralization.

### 15.6. What if a regulator demands KYC?

The **protocol** does not require KYC.

**Communities** may choose to require it for certain roles or payments. This is their decision.

The protocol provides tools. Communities use them as they see fit.

### 15.7. What jurisdiction is CL in?

None yet. No legal entity exists.

When one is created, it will likely be a foundation or cooperative in a jurisdiction friendly to open-source and privacy.

### 15.8. Can I use CL to pay for illegal things?

CL is a record-keeping system. It does not move money. If you use external payment rails to pay for illegal things, that is between you and the law.

The protocol does not encourage or facilitate illegal activity. Communities set their own rules and can ban bad actors.

---

## Still have a question?

- Open a [Discussion](../../discussions).
- Open an [Issue](../../issues) labeled `question`.
- Read the [whitepaper](./docs/whitepaper.md) — most answers are there.

There are no stupid questions. If something is unclear, asking helps everyone.

---

**Last updated:** 2026  
**Version:** 1.0