---
name: redteam-suite
description: Use when you need to test whether a skill reviewer can be fooled by a package that looks complete but verifies nothing. Ships two probe packages and a runner that fails the reviewer if either probe earns reproducible points.
license: MIT
metadata:
  version: 1.0.0
  author: zhaoxinghua09-cell
---

# Skill Redteam Suite

An adversarial benchmark for skill reviewers. It answers one question:

> Can your reviewer be fooled by a package that looks complete but verifies nothing?

## Quick start

```bash
python run_suite.py --reviewer /path/to/review.py
```

Exit `0` = both probes blocked; `1` = at least one got through.

## What is inside

- `probes/shape/` — a package whose runner prints PASS with zero assertions, plus a demo that
  prints one line. It must not earn reproducible points.
- `probes/vacuity/` — a formally complete package with empty content. Its total score may pass
  (a structure score only sees shape); it must still lose reproducible points.
- `run_suite.py` — copies each probe to a temp dir, scores it with your reviewer, and judges
  the verdict on the reproducible dimension, not on the total.

## Why the reproducible dimension

A well-shaped fake reaches 88–92/100 on our own ruler even after two anti-gaming patches.
Total score is a shape score. `reproducible` is where "this verifies nothing" shows up.

## The control experiment

| Reviewer | shape | vacuity | Verdict |
|---|---|---|---|
| lgd-skill-review 1.1.16 | 78 WARN, repro 11/20 | 88 PASS, repro 16/20 | all blocked |
| same code, three checks disabled | 87 PASS, repro 20/20 | 92 PASS, repro 20/20 | 2 got through |

The second row proves the suite can fail. Without it, "all blocked" only means "the probes are
easy".

## Limits

- It does not judge content quality, only whether obvious fakes are rejected.
- Passing does not mean the reviewer is good; it means it is not fooled by these two probes.
