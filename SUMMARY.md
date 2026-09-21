# Contribution Ledger — One-Page Summary

**A decentralized ledger of contribution, reputation, and access — without cryptocurrency.**

---

## The problem

Your reputation today belongs to platforms.

- Lose your GitHub account — lose your history.
- Leave Upwork — start from zero.
- Get banned on a forum — no appeal.
- Pay 10–30% in fees to intermediaries.
- Your contributions are rented, not owned.

Cryptocurrency tried to fix this but created a worse problem: reputation became a tradeable token. Votes, trust, and standing can now be bought. Whales dominate. Speculation replaces work.

Neither model gives you what you actually need: **a permanent, portable, non-purchasable record of what you did.**

---

## The idea

Contribution Ledger (CL) is a public record of who contributed what — signed, verified, and owned by no one.

- Every contribution is **cryptographically signed**.
- Every record is **confirmed by peers** and stored in an **append-only ledger**.
- Reputation is **contextual** (per community) and **earned, not bought**.
- CU (Contribution Units) are **non-transferable** at the protocol level. They cannot be sold, bought, or collateralized.

CL uses the useful parts of blockchain — hash-linked events, Merkle proofs, distributed consensus — but removes the money. No token. No mining. No exchange. No speculation.

**This is not a limitation. It is the point.**

---

## How people earn

Profit comes from **outside** the system — from real clients, funds, and cooperatives. Not from new buyers. Not from air.

| Source | Who pays | Range |
|---|---|---|
| Bounties | Organizations | $20–10 000 per task |
| Work via reputation | Employers | Salary, 2–10× better than anonymous |
| Grants | Funds (NLnet, OTF, Mozilla, EU) | $5 000–500 000 |
| Cooperative payouts | Cooperatives | Share of revenue |
| Paid communities | Members | Monthly dues |
| Roles and access | Organizations | $5 000–50 000 per contract |
| Compute tasks | Task issuers | $0.10–10 per hour |
| Savings on intermediaries | — | 10–30% per deal |

**What CL does not offer:** token gains, passive income, staking yield, or speculation. If you want those, go elsewhere.

**What CL offers:** money for verified work, a portable portfolio, access to opportunities, and a vote that cannot be bought.

---

## Useful work instead of mining

Instead of burning energy on hashes, CL participants contribute things that matter:

- **Compute power** — AI training, inference, simulation, rendering.
- **Community help** — moderation, translation, verification, mentoring.
- **Network support** — relays, storage, indexing.

Results are verified (redundancy, sampling, cryptographic proofs). Task issuers pay in fiat or stablecoin. CU are earned as reputation, not as money.

---

## How it works (in 30 seconds)

1. You generate a keypair — this is your identity (`did:cl:...`).
2. You do work: code, review, moderation, mentorship, compute.
3. Peers confirm your contribution.
4. You earn CU and reputation in that context.
5. Reputation opens bounties, grants, roles, and votes.

Everything is signed. Everything is verifiable. Nothing is deletable. Nothing is buyable.

---

## Governance without plutocracy

- **Federated consensus** — validators are chosen by the community, not bought.
- **Quadratic voting** — vote weight is `√reputation`, so doubling reputation gives only 1.41× more power.
- **Right to fork** — any community can leave with its data.
- **No central owner** — no single entity can change the rules.

---

## Status

**Whitepaper v1.2 — draft. Implementation not started.**

- [x] Whitepaper (EN, RU)
- [x] README, CONTRIBUTING, CODE_OF_CONDUCT, FAQ
- [ ] Technical specification
- [ ] Reference implementation (Rust/Go)
- [ ] Web client
- [ ] Pilot with 10 participants
- [ ] Federation
- [ ] Compute pilot

We are not promising a launch date. We are building in the open and inviting others to build with us.

---

## Honest risks

- **No users yet.** A protocol without a community is dead code.
- **No funding yet.** We are not accepting donations until there is a legal entity.
- **Adoption is uncertain.** Many projects like this fail.
- **Compute verification is hard.** No one has fully solved it.
- **Legal review is pending.** Regulatory risk is real.

We do not hide these. We state them.

---

## What we need

- **Critics** — find flaws before we build.
- **Rust / Go developers** — core protocol, P2P, crypto.
- **Cryptographers** — review Ed25519, Merkle, ZK.
- **Community organizers** — first pilots.
- **Translators** — RU → EN → other languages.
- **Legal and economics reviewers.**

See [CONTRIBUTING.md](./CONTRIBUTING.md) to start.

---

## Read next

- [Whitepaper (full)](./docs/whitepaper.md)
- [Economics](./docs/economics.md)
- [Useful Work](./docs/useful-work.md)
- [FAQ](./docs/faq.md)

---

## One-line pitch

> **Contribution Ledger is GitHub without a company, LinkedIn without a platform, and a cooperative without shares — a public record of who did what, owned by no one, buyable by no one.**

---

**GitHub:** [mikky1sCp/Contribution-Ledger](https://github.com/mikky1sCp/Contribution-Ledger)  
**License:** CC BY-SA 4.0 (text) / MIT (code)

---

Это резюме на одну страницу. Его можно:

- положить в корень репозитория как `SUMMARY.md`;
- вставить в начало whitepaper как «Executive Summary»;
- использовать как питч для гранта или инвестора;
- отправить в личку человеку, чтобы он за 2 минуты понял суть.

