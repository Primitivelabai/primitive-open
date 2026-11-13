---
name: open-source-scrub
description: Check that a repository, skill, plugin, package or folder is safe and honest to publish before it goes public. Covers private names and emails, local paths, secrets, quoted feedback, internal architecture, commit-author identity, authorship, credits and licence consistency. Use before making a repo public, publishing a skill or plugin, uploading a zip, open-sourcing internal work, or when someone asks "is this safe to post?". Do not use as a substitute for a secret-scanning service or legal advice.
---

# Open-Source Scrub

Publishing is hard to undo. Once a repo is public it can be cloned, cached and indexed within minutes. Scrub before, not after.

The leaks that actually happen are rarely API keys. They are the human things: a person's real feedback quoted in a "lessons" file, an internal system named in a reference doc, a username inside a commit email, a skill that turns out to be someone else's.

## Core rule

**Read every file you publish, as a stranger would.** Pattern scans find candidates; only reading finds meaning. A file that passes every grep can still describe your client.

## 1. Inventory

List exactly what will be published: every tracked file, every file inside any zip or archive, and the git history (not just the latest tree). Anything in history is published too.

- If history contains anything private, publish from a fresh single-commit history instead of cleaning old commits.
- Drop internal working files (`PLAN.md`, handoffs, notes, `.env.example` with real values, test fixtures from real data).

## 2. Provenance: is it yours to publish?

For each skill, file or asset, establish who wrote it:

- Check `author`, `license` and `copyright` fields, plugin manifests and `LICENSE` files. Third-party skills often sit in the same folders as your own.
- Account names can differ from people's names. Confirm an unfamiliar author against the account that created it before deciding it belongs to someone else, or that it is yours.
- Look for "adapted from", "based on", "source notes" or upstream paths. Adapted work keeps its upstream licence and credit.
- If the origin is "something I read", ideas are fine; copied wording is not. Rewrite in your own words and drop the source notes.

Outcome per item: **ours**, **ours with credit** (name the source and licence), or **not ours** (leave it out).

## 3. Content scrub

Check each file for:

| Look for | Why it matters |
| --- | --- |
| People's names, emails, phone numbers, usernames | Identity and privacy |
| Clients, patients, customers, employers, case details | Confidentiality, often legal |
| Quoted feedback ("Love it, but…") | Someone's private words, published without asking |
| Local paths (`C:\Users\…`, `/home/…`, `/Users/…`) | Reveal usernames and machine layout |
| Internal system names, repo names, branches, ticket numbers, board or job IDs | Map of your internals for anyone curious |
| Product internals from an unrelated product (examples lifted from real work) | Leaks roadmap and design |
| Secrets: keys, tokens, private keys, connection strings, `.env` files | Direct compromise |
| Money, pricing, contracts, grants | Commercial confidentiality |
| Rendering junk from copying out of a web UI | Looks careless, breaks markdown |

Rewrite rather than delete where the content is useful: turn a quote into a general symptom, a real product example into a neutral one.

Starter scan (adjust names to the project, then read every hit):

```bash
git ls-files | xargs grep -n -I -i -E "<real names>|<company internals>|@gmail|@outlook|C:\\\\Users|/Users/|/home/" 
git ls-files | xargs grep -n -I -E "(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY|xox[bp]-)"
git ls-files | grep -i -E "\.env|secret|\.pem|\.key$|credential"
```

## 4. Identity in metadata

- **Commit author name and email** on every commit. GitHub no-reply addresses include the account username (`12345+username@users.noreply.github.com`), which links the work to that account.
- Package and plugin manifests (`author`, `email`, `homepage`).
- Document metadata in PDFs, Office files and images (author, company, GPS). Strip it.

Decide deliberately whether the work should be linked to a personal account, a company account or a brand.

## 5. Licence and consistency

- One licence per repository unless there is a clear reason. A component's licence field must match the repository licence.
- Adapted third-party material keeps its notices.
- The README must not promise things that are not there yet.
- Follow the destination repository's contributing rules (spelling, dependencies, tests).

## 6. Validate and record

- Run the platform's own validators (plugin, package or skill validators).
- Run the scans again after every edit.
- Keep a short scrub record: what was removed, rewritten or credited, and what was checked. Do not publish the record if it names what was removed.

## Stop and ask

Publishing is the owner's decision. Never push, make public or upload as part of a scrub. Report:

```
SCRUB: READY | READY WITH CHANGES | NOT READY

PUBLISHING   what exactly will become public (files, history, archives)
OWNERSHIP    ours / ours with credit / not ours, per item
FIXED        what was removed or rewritten
OPEN         anything still needing the owner's decision
CHECKS       scans and validators run, with results
```

Never write "safe" or "clean" without listing what was checked. A scrub found nothing it did not look for.
