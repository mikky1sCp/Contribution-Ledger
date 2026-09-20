# Contribution Ledger

**A decentralized ledger of contribution, reputation, and access — without cryptocurrency.**

[![Status](https://img.shields.io/badge/status-draft-yellow.svg)](#status)
[![Version](https://img.shields.io/badge/whitepaper-v1.2-blue.svg)](docs/whitepaper.md)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/text-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE)
[![License: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE-CODE)

---

## What is this?

Contribution Ledger (CL) records who did what in a community — verifiably, permanently, and without a token, exchange, or speculation.

Today your reputation belongs to platforms. Lose the account — lose the record. In CL, contribution is signed, portable, and permanent.

---

## Why?

**Centralized platforms** own your reputation. Stack Overflow, GitHub, LinkedIn, Upwork — you can't take your achievements with you, rules change without your consent, and accounts vanish with the service.

**Cryptocurrencies** turn reputation into a speculative asset. Votes are bought, whales dominate, and profit goes to early buyers — not to workers.

**CL takes the technology without the speculation.** Cryptographic proofs, decentralized ledgers, community consensus — but no token to pump, dump, or rug.

---

## How do people earn?

CL does not offer token gains. It offers **real profit from real work**.

| Source | Who pays | Amount |
|---|---|---|
| **Bounties** | Organizations | $20–10,000 per task |
| **Work via reputation** | Employers | Salary, ongoing |
| **Grants** | Funds (NLnet, OTF, Mozilla, EU) | $5,000–500,000 |
| **Cooperative payouts** | Cooperatives | Revenue share by CU |
| **Paid communities** | Members | Access, grants |
| **Roles and access** | Organizations | $5,000–50,000 per contract |
| **Compute tasks** | AI labs, researchers | $0.10–10 per hour |
| **Savings on intermediaries** | — | 10–30% per deal |

Read the full economics section: [docs/whitepaper.md#13-economics](docs/whitepaper.md).

---

## Not a cryptocurrency

| Property | Cryptocurrency | Contribution Ledger |
|---|---|---|
| Unit of account | Transferable token | Non-transferable CU |
| Transfer to others | Allowed | **Forbidden by protocol** |
| Buy / sell | Via exchanges | **Impossible** |
| Emission | By algorithm | For verified contribution |
| Incentive | Price profit | Work profit |
| Consensus | PoW / PoS | Federated / reputational |
| Who gets rich | Early buyers | Those who work |

**No token. No mining. No exchange. No speculation.** CU cannot be bought, sold, transferred, or collateralized.

---

## How it works (in one minute)

1. **Identity** — you generate a keypair. Your DID is your public key. No personal data on-chain.
2. **Contribution** — you do work (code, review, moderation, teaching, compute). It gets signed and confirmed by the community.
3. **Reputation** — confirmed contributions accumulate as Contribution Units (CU), weighted by context and time.
4. **Access** — reputation opens roles, votes, bounties, grants, and cooperative payouts.
5. **Profit** — money comes from outside: organizations, clients, funds, cooperatives. Not from token emission.

---

## Useful work, not mining

Participants can contribute **useful work** instead of burning energy:

- donating compute to train AI models;
- supporting network infrastructure;
- helping the community (moderation, translation, verification);
- running simulations, rendering, scientific computations.

Paid by the task issuer. Verified by redundancy, sampling, and reputation. CU awarded only for **verified results**, never for time online.

> Detailed in [Section 14 — Useful Work](docs/whitepaper.md).

---

## Status

**Whitepaper v1.2 — public draft. Implementation not started.**

Current stage:

- [x] Whitepaper drafted (EN + RU)
- [ ] Technical specification
- [ ] Reference implementation (Rust / Go)
- [ ] MVP with single node
- [ ] Pilot with 10–50 people
- [ ] Federated network

See [ROADMAP.md](ROADMAP.md) for the full 5-year plan.

---

## Read

- 📄 [Whitepaper (English)](docs/whitepaper.md)
- 📄 [Whitepaper (Русский)](docs/whitepaper.ru.md)
- 📘 [Economics](docs/economics.md) *(coming soon)*
- 📘 [Technical Specification](docs/specification.md) *(coming soon)*
- ❓ [FAQ](docs/faq.md) *(coming soon)*

---

## Contribute

CL is open. Everyone is welcome — developers, cryptographers, economists, community builders.

**We need:**

- Rust / Go developers for the core
- Cryptography reviewers
- Communities willing to pilot
- Translators
- Writers and editors

**How to help:**

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check open [issues](https://github.com/mikky1sCp/Contribution-Ledger/issues)
3. Open a discussion or submit a pull request

> Before opening a PR, please open an issue first. We discuss before we build.

---

## Open questions

We don't have all the answers. If you do — join the discussion.

- How to measure contribution in creative and subjective fields?
- How to prevent CU from becoming a de facto currency?
- How to verify useful compute without waste?
- How to fund validators without money?
- How to avoid founder capture?

Full list: [Section 21 — Open Questions](docs/whitepaper.md).

---

## Philosophy

- **Contribution over capital.** Actions create value, not money.
- **Reputation is not for sale.** If it can be bought, it means nothing.
- **Profit from work, not speculation.** Earn from what you do.
- **Transparency without surveillance.** Rules public, data private.
- **Communities over platforms.** No corporation owns your reputation.
- **Right to exit.** Fork the ledger, take your data.

---

## License

- **Text (whitepaper, docs):** [CC BY-SA 4.0](LICENSE)
- **Code:** [MIT](LICENSE-CODE)

---

## Links

- **Repository:** https://github.com/mikky1sCp/Contribution-Ledger
- **Issues:** https://github.com/mikky1sCp/Contribution-Ledger/issues
- **Discussions:** https://github.com/mikky1sCp/Contribution-Ledger/discussions

---

**CL is not a product. It is a protocol. It lives as long as there are communities that use it.**
