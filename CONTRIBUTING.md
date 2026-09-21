# Contributing to Contribution Ledger

Thank you for your interest in Contribution Ledger (CL). This project is at an early stage — the whitepaper is a draft, and the implementation has not started. That means there is a lot of room to shape the project, and your input matters now more than ever.

This document explains how to contribute, what we need, and what we expect from participants.

---

## Table of Contents

1. [What we need](#1-what-we-need)
2. [Ways to contribute](#2-ways-to-contribute)
3. [Getting started](#3-getting-started)
4. [How to propose changes](#4-how-to-propose-changes)
5. [RFC process](#5-rfc-process)
6. [Pull request guidelines](#6-pull-request-guidelines)
7. [Commit message convention](#7-commit-message-convention)
8. [Review process](#8-review-process)
9. [Code style](#9-code-style)
10. [Writing style](#10-writing-style)
11. [What we will not accept](#11-what-we-will-not-accept)
12. [Recognition](#12-recognition)
13. [Questions](#13-questions)

---

## 1. What we need

CL is not just a coding project. It is a protocol, a governance model, an economic design, and a social experiment. We need people with different skills.

**Right now (whitepaper stage):**

- **Critics.** Read the whitepaper and find what is wrong, unclear, or missing. This is the most valuable contribution today.
- **Cryptographers.** Review the cryptographic choices: Ed25519, BLAKE3, Merkle structures, ZK proofs.
- **Distributed systems engineers.** Review the consensus, DAG, and federation design.
- **Economists.** Review the profit schemes and incentive design.
- **Legal experts.** Review regulatory risks, especially around CU and payments.
- **Translators.** RU → EN, EN → other languages.
- **Writers.** Improve clarity, structure, and accessibility.

**Soon (specification stage):**

- **Rust / Go developers** for the reference implementation.
- **TypeScript developers** for the web client.
- **DevOps** for CI/CD, testnets, deployment.

**Later (pilot stage):**

- **Community organizers** to run the first pilots.
- **Moderators** to help with discussions.
- **Designers** for UI/UX.

If you have a skill not listed here — open an issue and tell us how you can help.

---

## 2. Ways to contribute

You do not need to write code to contribute. Every contribution counts.

| Type | Where | Example |
|---|---|---|
| Report a problem | Issues | "Section 9.2 formula is ambiguous" |
| Suggest an idea | Discussions | "What if CU decay was optional per context?" |
| Improve text | Pull request | Fix typos, clarify wording |
| Translate | Pull request | Add `whitepaper.es.md` |
| Review a proposal | Comments on RFC | Point out a flaw in the design |
| Write an RFC | Pull request to `rfcs/` | Propose a new event type |
| Implement code | Pull request | Core protocol in Rust |
| Build a tool | Separate repo | CLI for reading the ledger |
| Run a pilot | Discussion → issue | Test with your community |
| Spread the word | Everywhere | Tell people who might care |

**Documentation, translation, and criticism are as valuable as code.** Do not assume your contribution is too small.

---

## 3. Getting started

### 3.1. Read first

Before contributing, read:

1. [README.md](./README.md) — project overview.
2. [Whitepaper](./docs/whitepaper.md) — the full design.
3. [Economics](./docs/economics.md) — how people earn.
4. [Useful Work](./docs/useful-work.md) — compute and community help.
5. [FAQ](./docs/faq.md) — common questions.

This will save you time and avoid repeated discussions.

### 3.2. Set up Git

```bash
git clone https://github.com/mikky1sCp/Contribution-Ledger.git
cd Contribution-Ledger
```

### 3.3. Find something to do

- Check [Issues](../../issues) labeled `good first issue` or `help wanted`.
- Check [Discussions](../../discussions) for open questions.
- If nothing fits, open an issue describing what you want to do.

Do not start large work without discussing it first. A five-minute conversation can save a week of wasted effort.

---

## 4. How to propose changes

### 4.1. Small changes (typos, wording, links)

Open a pull request directly. No prior discussion needed.

### 4.2. Medium changes (new sections, clarifications)

Open an issue first. Describe:

- what you want to change;
- why it matters;
- what the current text says;
- what your proposal says.

Wait for feedback before writing a full PR.

### 4.3. Large changes (new concepts, protocol changes)

Write an **RFC** (see next section). Large changes must be discussed publicly before being merged.

**Rule of thumb:** if your change touches more than one section or changes the meaning of the protocol, it is a large change.

---

## 5. RFC process

RFC (Request for Comments) is how we propose, discuss, and accept significant changes.

### 5.1. When to write an RFC

- New event type in the ledger.
- Change to the reputation formula.
- Change to consensus or validators.
- Change to the economic model.
- Change to the CU transfer ban.
- Any change that affects interoperability.

### 5.2. How to write an RFC

1. Copy `rfcs/0000-template.md` to `rfcs/NNNN-short-title.md`.
   - Use the next available number.
   - Use a short, descriptive title.
2. Fill in the sections:
   - **Summary** — one paragraph.
   - **Motivation** — why this change is needed.
   - **Design** — the technical or conceptual details.
   - **Alternatives** — what else was considered.
   - **Drawbacks** — what could go wrong.
   - **Open questions** — what is still undecided.
3. Open a pull request.
4. Discussion happens in the PR and in Discussions.
5. After rough consensus, a maintainer merges the RFC.
6. If the RFC changes the protocol, a follow-up PR updates the whitepaper and specification.

### 5.3. RFC states

- **Draft** — being written.
- **Discussion** — open for comments.
- **Accepted** — agreed, ready to implement.
- **Rejected** — not accepted, with reasons.
- **Withdrawn** — author withdrew it.
- **Superseded** — replaced by a newer RFC.

Rejected RFCs are kept in the repository. They are part of the project's history.

---

## 6. Pull request guidelines

### 6.1. Before opening a PR

- Read `CONTRIBUTING.md` (this file).
- Check that no existing PR or issue covers the same thing.
- Make sure your branch is up to date with `main`.
- Test your changes if applicable (spelling, links, formatting).

### 6.2. PR title

Use the same convention as commits (see Section 7).

Examples:
- `docs: clarify reputation decay formula`
- `rfc: add compute.task.verify event`
- `fix: broken link in README`

### 6.3. PR description

Include:

- **What** — what changed.
- **Why** — why it matters.
- **How** — how you did it (if non-obvious).
- **References** — link to related issues, discussions, or RFCs.

Template:

```markdown
## What
Clarify the reputation decay formula in Section 9.2.

## Why
The original formula was ambiguous about the floor value.

## How
Added an explicit definition: `floor = 0.1`.

## References
Closes #42.
```

### 6.4. PR size

- Prefer small PRs over large ones.
- One logical change per PR.
- If a PR grows too big, split it.

### 6.5. Draft PRs

Use draft PRs for work in progress. Mark as ready when you want review.

---

## 7. Commit message convention

We use [Conventional Commits](https://www.conventionalcommits.org/).

Format:

```
<type>(<scope>): <short description>

<optional body>

<optional footer>
```

Types:

- `docs` — documentation changes.
- `feat` — new feature (code).
- `fix` — bug fix.
- `rfc` — RFC-related changes.
- `spec` — specification changes.
- `refactor` — code refactoring.
- `test` — tests.
- `chore` — maintenance.
- `style` — formatting only.

Examples:

```
docs: clarify reputation decay formula
rfc: add compute.task.verify event
fix: broken link in README
spec: define CU revocation rules
```

Keep the subject line under 72 characters. Use the imperative mood ("add", not "added").

---

## 8. Review process

### 8.1. Who reviews

- **Documentation PRs** — any maintainer.
- **RFCs** — at least two maintainers and open community discussion.
- **Code PRs** — at least one maintainer with relevant expertise.
- **Protocol changes** — at least two maintainers and a public discussion period of no less than 7 days.

### 8.2. Timeline

We aim to respond to PRs within 7 days. If a PR sits longer, ping a maintainer.

### 8.3. What reviewers look for

- **Correctness** — is the change technically sound?
- **Clarity** — is it understandable to someone new?
- **Consistency** — does it match the rest of the project?
- **Consequences** — does it break anything?
- **Alternatives** — were other options considered?

### 8.4. Feedback

Reviewers will:

- ask questions;
- suggest improvements;
- request changes if needed;
- approve when ready.

**Feedback is about the work, not the person.** We expect the same from contributors.

### 8.5. Disagreements

If you disagree with a reviewer:

1. Explain your reasoning in the PR.
2. Request a second opinion.
3. If unresolved, open a Discussion thread.
4. Final decisions on protocol changes are made by rough consensus, not by authority.

---

## 9. Code style

Code style will be defined once the reference implementation starts. For now:

- **Rust** — `rustfmt`, `clippy` with `-D warnings`.
- **Go** — `gofmt`, `go vet`, `staticcheck`.
- **TypeScript** — `prettier`, `eslint`.
- **Markdown** — 80–100 characters per line, one sentence per line.
- **JSON** — 2-space indentation.

Every code PR must include tests. No exceptions for protocol logic.

---

## 10. Writing style

We write for a global audience, in English, in plain language.

### 10.1. Principles

- **Clear over clever.** Simple sentences beat complex ones.
- **Specific over vague.** "CU decays with a 2-year half-life" beats "CU decays over time".
- **Active voice.** "The validator signs the event" beats "The event is signed by the validator".
- **Define terms.** On first use, explain acronyms and jargon.
- **No hype.** Avoid "revolutionary", "game-changing", "next-generation".
- **No empty promises.** Do not promise features we have not designed.

### 10.2. Structure

- One idea per paragraph.
- Use headings to break up long sections.
- Use tables for comparisons.
- Use code blocks for examples.
- Use links for references.

### 10.3. Terminology

Use these terms consistently:

- **Contribution Unit (CU)** — not "coin", "token", "credit".
- **Ledger** — not "blockchain" (CL is not a blockchain).
- **Validator** — not "miner".
- **Attestation** — not "certificate".
- **Context** — not "community" or "space" when referring to a scope.
- **Useful Work** — not "mining".

### 10.4. Language

- English is the primary language of the repository.
- Russian is supported in `docs/*.ru.md`.
- Other languages are welcome as `docs/*.<lang>.md`.
- Keep translations in sync with the English version. If you update English, note the change for translators.

---

## 11. What we will not accept

CL has a clear boundary. We will reject contributions that:

### 11.1. Turn CL into a cryptocurrency

- Adding a transferable token.
- Allowing CU to be bought, sold, or transferred.
- Adding staking for profit.
- Adding yield, interest, or derivatives.
- Integrating with exchanges or DEXs.
- Any mechanism that lets CU be converted to money directly.

**This is the core principle of the project.** Any PR that violates it will be closed without merge.

### 11.2. Compromise privacy

- Storing personal data on-ledger.
- Requiring KYC at the protocol level (communities may choose it, but not the protocol).
- Adding global tracking or surveillance features.

### 11.3. Centralize control

- Giving a single entity the power to change rules unilaterally.
- Removing the right to fork.
- Adding a mandatory central server.

### 11.4. Introduce hype or spam

- Marketing content.
- Referral schemes.
- Paid promotion.
- AI-generated low-quality content without review.

### 11.5. Violate the Code of Conduct

See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

---

## 12. Recognition

CL is about recognizing contribution. We apply the same principle to our own project.

Contributors will be recorded in `CONTRIBUTORS.md`, and — once the protocol is live — their contributions will be recorded in the CL ledger itself.

Recognition includes:

- **Attribution** in `CONTRIBUTORS.md`.
- **Mention** in release notes for significant contributions.
- **CU and reputation** in the CL ledger (when live).
- **Priority** for grants and roles, once funding exists.

We do not pay for contributions at this stage. We are honest about this. If and when funding arrives, it will be distributed by contribution, using the same rules we propose for others.

---

## 13. Questions

If something is unclear:

- Open a [Discussion](../../discussions).
- Open an [Issue](../../issues) labeled `question`.
- Ask in the PR or issue where you are working.

There are no stupid questions. If you are confused, others probably are too — asking helps everyone.

---

## Summary

- Read the whitepaper before contributing.
- Start small. Open an issue before large work.
- Use RFCs for protocol changes.
- Follow Conventional Commits.
- Write clearly, in plain English.
- Do not turn CL into a cryptocurrency.
- Be respectful.
- Ask questions.

Thank you for being here. This project only exists if people care about it.

---

**Last updated:** 2026  
**Version:** 1.0