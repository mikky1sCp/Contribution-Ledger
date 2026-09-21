# Economics of Contribution Ledger

**How participants earn — without a token, without speculation, without air.**

**Version:** 1.0  
**Status:** Living document  
**Related:** [Whitepaper](../docs/whitepaper.md) · [Useful Work](./useful-work.md) · [FAQ](./faq.md)

---

## Table of Contents

1. [Core Principle](#1-core-principle)
2. [Where Money Comes From](#2-where-money-comes-from)
3. [Scheme 1: Bounties](#3-scheme-1-bounties)
4. [Scheme 2: Work via Reputation](#4-scheme-2-work-via-reputation)
5. [Scheme 3: Grants and Funds](#5-scheme-3-grants-and-funds)
6. [Scheme 4: Cooperative Payouts](#6-scheme-4-cooperative-payouts)
7. [Scheme 5: Paid Communities](#7-scheme-5-paid-communities)
8. [Scheme 6: Roles and Access](#8-scheme-6-roles-and-access)
9. [Scheme 7: Savings on Intermediaries](#9-scheme-7-savings-on-intermediaries)
10. [Scheme 8: Reputation as Capital](#10-scheme-8-reputation-as-capital)
11. [Scheme 9: Compute and Useful Work](#11-scheme-9-compute-and-useful-work)
12. [Summary Table](#12-summary-table)
13. [What CL Does Not Offer](#13-what-cl-does-not-offer)
14. [Who Benefits and Who Does Not](#14-who-benefits-and-who-does-not)
15. [Example: A 3-Year Path](#15-example-a-3-year-path)
16. [Funding the CL Project Itself](#16-funding-the-cl-project-itself)
17. [Prohibition on CU Monetization](#17-prohibition-on-cu-monetization)
18. [Why This Is Sustainable](#18-why-this-is-sustainable)
19. [Open Questions](#19-open-questions)

---

## 1. Core Principle

**Profit comes from outside the system.**

It comes from:

- organizations that pay for work;
- clients who need tasks done;
- funds that support open-source and public goods;
- cooperatives that share revenue;
- communities that charge dues;
- task issuers who pay for compute.

It does **not** come from:

- token emission;
- new buyers entering the system;
- the pockets of later participants;
- speculation;
- staking or yield;
- thin air.

**The ledger records contribution. Money moves separately.**

A participant earns by doing verified work for someone who pays. CL makes the record of that work permanent, portable, and non-purchasable. But CL does not create the money — the market does.

### 1.1. Comparison

| Cryptocurrency | Contribution Ledger |
|---|---|
| Profit from token price | Profit from paid contribution |
| Early buyers gain at the expense of late ones | No one gains at another's expense |
| Needs new money to grow | Needs organizations that pay for work |
| Profit for speculators | Profit for workers |
| Zero-sum | Positive-sum |
| Passive income (staking) | No passive income |
| Value from scarcity | Value from usefulness |

### 1.2. Why this matters

If profit comes from new buyers, the system is a Ponzi by design. Eventually, new buyers stop coming, and the system collapses.

If profit comes from real clients and real work, the system can run indefinitely. It does not need new entrants to survive. It needs people who do useful things and people who pay for them.

This is the difference between a casino and a market.

---

## 2. Where Money Comes From

Five external sources:

| Source | Who | What they pay for |
|---|---|---|
| Clients | Companies, startups, individuals | Tasks they need done |
| Funds | NLnet, OTF, Mozilla, EU, local | Open-source, public goods |
| Cooperatives | Member-owned organizations | Labor and shared revenue |
| Communities | Members | Access, services, governance |
| Task issuers | AI labs, researchers, studios | Compute, data, labeling |

In all cases, money enters CL from the outside. CL does not print it.

### 2.1. Payment rails

CL does not move money. It records that money moved.

- **Fiat** — Stripe, Wise, bank transfer.
- **Stablecoins** — USDC, USDT, DAI (external wallets).
- **Crypto** — BTC, ETH, others (optional, external).
- **In-kind** — access, services, resources.

The ledger stores: amount, currency, method, external reference. No personal data.

### 2.2. Escrow

For bounties and compute tasks, funds are held in **escrow** before work begins.

- Escrow is a multisig identity: client + arbiter + protocol.
- Funds are released on verified completion.
- Disputes go to arbitration (3 randomly chosen auditors).

If the client does not fund escrow, do not do the work.

---

## 3. Scheme 1: Bounties

**The simplest and most immediate way to earn.**

An organization posts a task with a reward. A participant claims it, completes it, gets it confirmed, gets paid.

### 3.1. How it works

1. **Post.** Client creates a bounty:

```json
{
  "type": "bounty.create",
  "issuer": "did:cl:org:startupX",
  "task": "Write API documentation for v2",
  "reward": {"amount": 500, "currency": "USD", "method": "escrow"},
  "escrow_id": "did:cl:escrow:main:123",
  "deadline": 1730100000,
  "requirements": ["3 peer reviews", "grammar check", "code examples tested"],
  "context": "repo:github.com/x/y",
  "weight_class": "bounty_doc"
}
```

2. **Fund.** Client locks $500 in escrow.
3. **Claim.** Participant claims the bounty.
4. **Submit.** Participant completes the task and submits evidence.
5. **Review.** Peers confirm the work meets requirements.
6. **Complete.** Escrow releases $500 to the participant.
7. **Record.** `payment.record` is written to the ledger. CU and reputation are awarded.

### 3.2. What the participant gets

- **Money** — $500, paid in fiat or stablecoin.
- **CU** — non-transferable contribution units.
- **Reputation** — in the context of the bounty.
- **Portfolio record** — permanent, verifiable, undeletable.

### 3.3. What the client gets

- **Verified executor** — reputation visible before hiring.
- **Transparent accounting** — every step recorded.
- **Lower fraud risk** — escrow + peer review + arbitration.
- **Reputation trail** — the client's own contributions are recorded.

### 3.4. Realistic amounts

| Task type | Range |
|---|---|
| Small (typo fix, minor doc) | $20–100 |
| Medium (feature, review, translation) | $100–1 000 |
| Large (module, full doc set, audit) | $1 000–10 000 |
| Long-term contract | Salary |

Rates are set by the market. CL does not fix them.

### 3.5. Dispute resolution

If the work is disputed:

1. Either party opens a dispute.
2. Three auditors are randomly selected (high reputation in context).
3. They review evidence and vote.
4. Decision is final. Escrow is distributed accordingly.
5. Auditors receive a small percentage of the disputed amount.

Frivolous disputes are penalized by reputation.

---

## 4. Scheme 2: Work via Reputation

**The compounding effect of a verifiable portfolio.**

An employer or client views a CL profile and sees:

- 340 confirmed commits;
- 120 code reviews;
- 50 hours of mentorship;
- 12 attestations from independent organizations;
- reputation 780 in "backend";
- reputation 320 in "security";
- 3 completed audits, all confirmed.

This is not a resume. A resume can be fabricated. This is not a review. Reviews can be bought. This is a **cryptographically verifiable record of work**.

### 4.1. What the participant gets

- Job offers.
- Freelance contracts.
- Invitations to private projects.
- Access to closed vacancies.
- Better rates than anonymous workers.
- Ability to negotiate from evidence, not claims.

### 4.2. What the employer gets

- Less hiring risk.
- Faster screening.
- Evidence instead of assertions.
- Protection against resume fraud.

### 4.3. The compounding effect

| Stage | Reputation | Typical rate multiplier |
|---|---|---|
| Anonymous | 0 | 1× |
| Newcomer | 10–100 | 1.5–2× |
| Trusted | 100–500 | 2–4× |
| Veteran | 500–2 000 | 4–8× |
| Council | 2 000+ | 8–10× |

These are estimates, not promises. Real rates depend on market, skills, and context.

### 4.4. Portability

The key difference from platforms: **reputation moves with you.**

- Leave GitHub — your CL record remains.
- Switch from one project to another — reputation carries over (if contexts recognize each other).
- Start a new community — your history is provable.

No platform can take it away. No platform can sell it. No platform can edit it.

---

## 5. Scheme 3: Grants and Funds

**Money for open-source and public goods, distributed by verified contribution.**

Funds today (NLnet, Open Technology Fund, Mozilla, EU programs, local foundations) distribute millions of dollars annually. The process is often opaque: applications, letters of intent, subjective committee decisions.

CL offers a different model.

### 5.1. How it works

1. A fund announces a program in CL: "Grants for privacy-preserving tools, $200 000 total."
2. Contributors submit their work, already recorded in the ledger.
3. The fund sees:
   - what each person has done;
   - who confirmed it;
   - what the community trusts;
   - how reputation is distributed.
4. Funding decisions are made with full evidence, not on claims.
5. Payments are recorded on-ledger.

### 5.2. What the participant gets

- Grants from $5 000 to $500 000.
- Transparent process — reasons are visible.
- Less bureaucracy — no 30-page applications.
- Reputation as a grantee.
- Track record for future funding.

### 5.3. What the fund gets

- Confidence in the executor.
- Transparent reporting.
- Lower risk of misuse.
- Evidence of impact.
- Cheaper due diligence.

### 5.4. Examples

**Example A: Individual grant.**  
Alice maintains a cryptographic library used by 10 000 projects. Her CL record shows 5 years of commits, 800 reviews, 40 attestations. She receives a $50 000 grant. Without CL, she would spend 3 months on applications.

**Example B: Retroactive funding.**  
A fund distributes $100 000 retroactively. CL shows who contributed what over the last 2 years. The fund allocates proportionally to verified contribution. No politics. No lobbying.

**Example C: Matching funds.**  
A community raises $30 000. A foundation matches it 2:1, funding $60 000 more. CL makes the matching transparent and verifiable.

### 5.5. Why this is different from Gitcoin

Gitcoin uses a token (GTC) and quadratic funding. CL uses no token and a different mechanism — allocation by verified contribution and reputation.

Gitcoin could be built **on top of** CL as a funding layer.

---

## 6. Scheme 4: Cooperative Payouts

**Revenue sharing without equity.**

A cooperative earns money from services, products, or subscriptions. Revenue is distributed by contribution — not by shares, not by capital invested.

### 6.1. The formula

```
member share = (member's CU / total CU) × distributable amount
```

CU is non-transferable. It cannot be bought. It can only be earned.

### 6.2. Example

A developer cooperative earns $100 000 in a year.

Total CU across all members: 10 000.

| Member | CU | Share | Payout |
|---|---|---|---|
| Alice | 500 | 5% | $5 000 |
| Bob | 1 200 | 12% | $12 000 |
| Carol | 300 | 3% | $3 000 |
| Dave | 800 | 8% | $8 000 |
| Others | 7 200 | 72% | $72 000 |

Calculation is automatic. Rules are public. No disputes over "who did more" — the ledger shows it.

### 6.3. What the participant gets

- A share of revenue proportional to contribution.
- Transparent calculation.
- A vote on distribution rules.
- Protection from CU purchases (no one can buy their way in).
- Long-term alignment: contribution this year affects payout this year.

### 6.4. What the cooperative gets

- Fair distribution.
- Motivated members.
- Fewer conflicts.
- A clear record of who contributed what.

### 6.5. This is not stock

**CU is not equity.**

- Cannot be sold.
- Cannot be transferred.
- Cannot be inherited.
- Does not represent ownership.
- Does not pay dividends.

CU gives a share in the **result of labor**, not in the **company itself**.

### 6.6. Decay and vesting

Communities may add:

- **Decay** — CU loses value over time, so recent contribution matters more.
- **Vesting** — CU becomes fully active after a period (prevents gaming).
- **Floors** — minimum payout regardless of CU (protects newcomers).

These are community choices, not protocol rules.

---

## 7. Scheme 5: Paid Communities

**Membership dues that fund the commons.**

A closed community charges monthly or annual dues. Money funds:

- validators (infrastructure);
- grants to active members;
- moderation;
- events;
- tools.

### 7.1. Example

A community has 500 members, each paying $10/month. Total: $5 000/month.

| Allocation | Amount | Purpose |
|---|---|---|
| Validators | $2 000 | Run nodes, secure ledger |
| Grants | $1 500 | Fund active members' projects |
| Infrastructure | $1 000 | Servers, tools, storage |
| Events | $300 | Meetups, conferences |
| Reserve | $200 | Emergency fund |

### 7.2. What the participant gets

- Access to knowledge, data, or tools.
- Networking with other members.
- Eligibility for grants.
- Influence on community decisions.
- The satisfaction of funding a shared resource.

### 7.3. What the community gets

- Independence from corporations.
- Sustainable funding.
- Motivation for active members.
- Autonomy from external platforms.

### 7.4. Variants

- **Tiered membership** — different levels, different benefits.
- **Free tier** — read-only access, no vote.
- **Contribution-based waiver** — active contributors pay less or nothing.
- **Barter** — services instead of money.

The community decides.

---

## 8. Scheme 6: Roles and Access

**Reputation opens doors that money cannot buy.**

High reputation in a context grants roles:

- Maintainer.
- Auditor.
- Curator.
- Moderator.
- Council member.
- Grant reviewer.

Roles are paid positions — funded by communities, funds, or organizations.

### 8.1. Examples

**Security auditor.**  
A participant with reputation 2 000 in "security" is authorized to audit smart contracts. Typical fee: $5 000–50 000 per audit. The role is earned, not purchased.

**Maintainer.**  
A participant with reputation 5 000 in a project's context becomes a maintainer. Maintainers often receive grants, stipends, or salary.

**Council member.**  
A council member of a fund or DAO receives a stipend ($500–5 000/month). Position is elected by reputation.

**Curator.**  
A curator of a dataset, list, or registry receives payment per curation. Access is earned.

### 8.2. What the participant gets

- Money (fees, stipends, salaries).
- Influence (shaping rules and priorities).
- Access (data, tools, people).
- Career (roles become credentials).

### 8.3. Access as a form of profit

Not all profit is money. Access to:

- private data;
- closed APIs;
- elite networks;
- decision-making rooms;

is worth money — and can be monetized through roles.

---

## 9. Scheme 7: Savings on Intermediaries

**Profit is not always income. Sometimes it is what you do not pay.**

CL replaces or reduces:

| Intermediary | Typical fee | CL cost |
|---|---|---|
| Freelance platforms (Upwork, Fiverr) | 10–20% | 0–2% |
| HR agencies | 15–30% | 0% |
| Legal verification | $1 000–10 000 | Negligible |
| Reputation platforms | Subscription | Free |
| Escrow services | 1–5% | Near-zero |
| Background checks | $50–500 | On-ledger evidence |

### 9.1. Example

A freelancer earns $10 000 through Upwork. Platform fee: $1 500.

Through CL: fee $0–200 (infrastructure). Savings: **$1 300–1 500 per deal**.

Over a year with 5 similar deals: **$6 500–7 500 saved**.

### 9.2. For organizations

A company hires 10 freelancers a year through agencies. Agency fees: 20% of $200 000 = $40 000.

Through CL: near-zero. Savings: **~$40 000 per year**.

### 9.3. Hidden savings

- Faster hiring (evidence instead of screening).
- Lower fraud (escrow + reputation).
- Fewer disputes (transparent records).
- Less legal overhead (clear rules).

These are hard to quantify but real.

---

## 10. Scheme 8: Reputation as Capital

**Reputation is not money. But it gives access to money.**

High reputation unlocks:

- **Investment** — investors fund founders with verified track records.
- **Grants** — funds give money to trusted contributors.
- **Upfront payment** — clients pay before work, because reputation guarantees quality.
- **Partnerships** — partners join projects led by trusted people.
- **Credit** — lenders offer better terms to those with verifiable history.

### 10.1. Examples

**Startup founder.**  
Alice has reputation 5 000 in "protocol design". An angel investor funds her startup without a working prototype. The reputation is the collateral.

**Freelancer.**  
Bob has reputation 2 000 in "smart contracts". A client pays 50% upfront, before any work. Bob's record is the guarantee.

**Grant recipient.**  
Carol has reputation 3 000 in "privacy tools". A foundation gives her $100 000 without a formal application. Her track record speaks.

### 10.2. What this is not

- Not a loan.
- Not equity.
- Not a security.
- Not a financial instrument.

It is **social capital** made measurable and portable.

### 10.3. Why it matters

Today, access to capital requires:

- collateral (money);
- credit history (banks);
- connections (networks);
- credentials (institutions).

CL adds a new path: **verified contribution**. For people without money, connections, or credentials, this is a way in.

---

## 11. Scheme 9: Compute and Useful Work

**Earning by contributing compute power or helping the community.**

Instead of mining (burning energy on hashes), participants contribute useful work.

See [Useful Work](./useful-work.md) for full details.

### 11.1. Types of useful work

- **AI training** — model training, fine-tuning.
- **Inference** — running models for clients.
- **Data labeling** — annotating datasets.
- **Simulation** — scientific, engineering, financial.
- **Rendering** — 3D, video, graphics.
- **Community help** — moderation, translation, verification.
- **Network support** — relays, storage, indexing.

### 11.2. Rates

| Task | Rate |
|---|---|
| Moderation hour | $5–15 |
| Translation (per 1 000 words) | $10–30 |
| GPU hour (consumer) | $0.10–0.50 |
| GPU hour (datacenter) | $1–5 |
| AI training job | $50–5 000 |
| Inference (per 1 000 requests) | $0.50–5 |

Rates are set by task issuers, not by the protocol.

### 11.3. Verification

To prevent fraud:

- **Redundancy** — same task to 3 executors. Results must match.
- **Sampling** — 5% of tasks audited manually.
- **Cryptographic proofs** — for ZK computations.
- **Reputation** — new accounts checked strictly.
- **CU staking** — participants stake CU (not money) to claim tasks; slashed on fraud.

### 11.4. The trap to avoid

As soon as "connect compute — earn CU" appears, people assume CU can be sold. Then:

- A market forms.
- A price emerges.
- Speculation follows.
- CL becomes a cryptocurrency.

**Three rules prevent this:**

1. CU awarded only for **verified results**, not time online.
2. Task issuer pays in **money**, not CU.
3. CU **cannot be exchanged** for money directly.

See [Section 17](#17-prohibition-on-cu-monetization).

---

## 12. Summary Table

| Source | Who pays | Amount | Frequency | Skill needed |
|---|---|---|---|---|
| Bounties | Organizations | $20–10 000 | Per task | Varies |
| Work via reputation | Employers | Salary | Ongoing | Professional |
| Grants | Funds | $5 000–500 000 | Per project | Specialist |
| Cooperative payouts | Cooperatives | Revenue share | Per period | Member |
| Paid communities | Members | Access, grants | Monthly | Member |
| Roles and access | Organizations | $5 000–50 000 | Per contract | Expert |
| Savings on intermediaries | — | 10–30% | Per deal | Any |
| Reputation as capital | Investors, funds | Access | As needed | Trusted |
| Compute tasks | Task issuers | $0.10–10/hour | Per task | Hardware |
| Community help | Communities | $5–30/hour | Per task | Any |

---

## 13. What CL Does Not Offer

To avoid illusions:

### 13.1. No token

There is nothing to buy or sell. No ICO, no presale, no airdrop, no fair launch.

### 13.2. No moonshots

Reputation does not rise in price. It cannot be traded. It does not appreciate.

### 13.3. No passive income

You cannot buy CU and earn interest. You cannot stake for yield. You cannot rent out reputation.

### 13.4. No fast money

Profit comes from work. If you want fast money, this is not for you.

### 13.5. No guarantees

If a community is poor, there will be no money. If a client does not pay, escrow protects you — but only if funded. If a fund rejects your grant, that is the fund's decision.

### 13.6. No speculation

No derivatives. No futures. No leverage. No arbitrage.

### 13.7. No gambling

No lotteries, no prediction markets, no zero-sum games.

### 13.8. No rent-seeking

You cannot extract value by owning, only by contributing.

---

## 14. Who Benefits and Who Does Not

### 14.1. Who benefits

**Freelancers and specialists.**  
Work without 10–30% platform fees. Verifiable portfolio.

**Maintainers of open-source projects.**  
Grants and reputation that belong to them.

**Volunteers.**  
Recognition without money.

**Cooperatives.**  
Fair distribution of revenue by contribution.

**Communities.**  
Independence and sustainable funding.

**Organizations.**  
Verified executors and transparent records.

**Students and newcomers.**  
A path to build reputation without credentials.

**People without capital, connections, or credentials.**  
A way in that does not require money.

### 14.2. Who does not benefit

**Speculators.**  
Nothing to buy.

**Rentiers.**  
No passive income.

**Scammers.**  
Cannot rug and leave.

**Those unwilling to work.**  
CU cannot be bought.

**Those seeking status without effort.**  
Reputation is earned.

**Crypto maximalists.**  
No token means no moonshot.

---

## 15. Example: A 3-Year Path

A concrete, realistic example.

### 15.1. Year 1

Alice registers in CL.

- 50 commits.
- 20 code reviews.
- 10 hours of mentorship.
- Earns 400 CU.
- Reputation: 400 in "backend".

First bounties: $2 000 for the year.

**Total Year 1:** ~$2 000 + 400 CU + reputation.

### 15.2. Year 2

Reputation: 1 200 in "backend", 200 in "security".

- Receives a $15 000 grant for her open-source project.
- Takes contracts through CL: $30 000 for the year.
- Becomes a validator for a small community.
- Receives CU stipend for validating: 200 CU.

**Total Year 2:** ~$45 000 + 600 CU + roles.

### 15.3. Year 3

Reputation: 3 500 in "backend", 1 200 in "security", 500 in "protocol design".

- Leads her own project funded by a foundation: $50 000.
- Cooperative payouts from a developer cooperative: $20 000.
- Invited to the council of two organizations (stipends: $10 000).
- Consults on security audits: $15 000.

**Total Year 3:** ~$95 000 + significant reputation + council seats.

### 15.4. Three-year totals

| Year | Income | Reputation | Roles |
|---|---|---|---|
| 1 | $2 000 | 400 | — |
| 2 | $45 000 | 1 400 | Validator |
| 3 | $95 000 | 5 200 | Council (×2) |
| **Total** | **~$142 000** | **5 200** | **Multiple** |

This is not a moonshot. It is a career.

And every dollar came from real work for real clients and funds — not from speculation.

---

## 16. Funding the CL Project Itself

**The project needs money to exist. Here is how it will get it.**

### 16.1. Sources

- **Grants** — NLnet, Open Technology Fund, Mozilla, EU programs, local foundations.
- **Donations** — from individuals and organizations aligned with the mission.
- **Community dues** — once communities form, optional contributions.
- **Integration services** — paid help for organizations integrating CL.
- **Support contracts** — paid support for enterprises running nodes.
- **Training and workshops** — paid education.

### 16.2. What is not a source

- Token sales. There is no token.
- ICO, IDO, IEO, fair launch.
- Equity sale (the project has no equity).
- Advertising.
- Data sale.

### 16.3. How funds are used

- Development (core protocol, clients, tools).
- Security audits.
- Documentation and translation.
- Community support.
- Legal and administrative.
- Founder and contributor stipends (if funding allows).

### 16.4. Transparency

All funding and spending will be recorded on-ledger (or in a public log if the ledger is not yet live). Anyone can verify.

### 16.5. Honest note

At the time of writing, there is **no funding**. The project is unfunded. This document describes intent, not reality.

---

## 17. Prohibition on CU Monetization

**This is the core principle. It is not negotiable.**

### 17.1. What is forbidden

The protocol forbids:

- Transferring CU to another identity.
- Selling CU for money or anything else.
- Buying CU.
- Collateralizing CU.
- Exchanging CU for goods, services, or other assets.
- Creating derivatives on CU (futures, options, swaps).
- Pooling CU in a tradeable instrument.
- Wrapping CU in any form.
- Custodying CU on behalf of another (except recovery, with strict rules).

### 17.2. How it is enforced

- **Protocol level** — CU is bound to an identity. Transfer events do not exist.
- **Validation level** — any attempt to transfer CU is rejected by validators.
- **Social level** — communities can revoke CU from those who attempt to circumvent the rules.
- **Fork level** — if a group tries to change this rule, the community can fork and exclude them.

### 17.3. Why it matters

If CU can be bought, then:

- Reputation is for sale.
- Votes are for sale.
- Governance is for sale.
- The whole system becomes a plutocracy.
- It becomes a cryptocurrency.
- It loses its reason to exist.

**The no-transfer rule is not a feature. It is the foundation.**

### 17.4. What about forks?

Anyone can fork the code and add transferable tokens. That fork is a different project. It is not CL. It will not be supported, merged, or recognized by the CL community.

The license allows forks. The community does not.

### 17.5. What about CU used as a signal?

CU can be used as:

- A signal of reputation (visible to others).
- A weight in votes (quadratic).
- A share in cooperative revenue (per rules).

CU cannot be used as:

- A medium of exchange.
- A store of value.
- A unit of account.
- A financial asset.

---

## 18. Why This Is Sustainable

### 18.1. No bubble

Profit comes from real work. There is no speculative premium to collapse.

### 18.2. No rug pulls

CU cannot be sold. There is no exit scam possible.

### 18.3. No plutocracy

The rich cannot buy power. Reputation is earned.

### 18.4. No dependence on new participants

The system works without new buyers. It needs workers and clients, not speculators.

### 18.5. No regulatory risk of securities

No token means no securities law. No exchange means no money transmission. No emission means no monetary policy.

### 18.6. No energy waste

Useful work replaces mining. Compute is used, not burned.

### 18.7. Alignment of incentives

- Participants want work.
- Clients want workers.
- Funds want impact.
- Communities want independence.
- The protocol wants accurate records.

All incentives point in the same direction.

### 18.8. Long-term viability

The system does not need to grow exponentially. It needs to be useful. A small, functioning community is better than a large, collapsing one.

---

## 19. Open Questions

Economics is not settled. These questions remain:

1. How to price contribution in creative and subjective fields?
2. How to prevent reputation farming via low-quality contributions?
3. How to balance decay (freshness) against stability (long-term contribution)?
4. How to fund validators in poor communities?
5. How to prevent CU from becoming a de facto currency via informal exchanges?
6. How to handle cross-community reputation recognition?
7. How to price compute tasks fairly?
8. How to prevent arbitrage between communities with different rules?
9. How to handle disputes at scale?
10. How to ensure that new contributors are not discouraged by high thresholds?

These are subjects of open discussion. Solutions will emerge through RFCs and pilot experience.

---

## Summary

**The economics of Contribution Ledger are simple:**

- Money comes from outside: clients, funds, cooperatives, communities.
- CU are earned, not bought. They are non-transferable.
- Reputation is contextual and non-purchasable.
- Profit is from work, not speculation.
- The system is positive-sum, not zero-sum.
- No token. No exchange. No speculation.

**This is not a get-rich-quick scheme. It is a way to make work visible, portable, and fairly rewarded.**

If you want moonshots, look elsewhere.  
If you want your work to count, read on.

---

**Related documents:**

- [Whitepaper](../docs/whitepaper.md) — full design.
- [Useful Work](./useful-work.md) — compute and community help.
- [FAQ](./faq.md) — common questions.
- [CONTRIBUTING](../CONTRIBUTING.md) — how to help.

**License:** CC BY-SA 4.0

**Last updated:** 2026  
**Version:** 1.0

---
