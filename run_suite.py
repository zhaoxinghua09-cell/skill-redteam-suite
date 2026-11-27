#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Red-team a skill reviewer: score two fake packages, fail if the reviewer is fooled.

How the verdict is decided (this took two experiments to get right):

  · shape   (runner prints PASS with zero assertions; demo prints one line)
      → must land BELOW the pass line, and must LOSE reproducible points.
  · vacuity (formally complete, content empty: 若-table, ten NEVER...因为 rules, stub refs)
      → its TOTAL may legitimately pass, because a structure score only sees shape.
        What must happen is that it LOSES reproducible points too.

Why not judge by total score alone: a well-shaped fake reaches 88–92/100 on our own
ruler even after two patches. Total is a shape score. The reproducible dimension is where
"this package verifies nothing" actually shows up, so that is what the suite asserts.

Measured (lgd-skill-review v1.1.16 vs a copy with its three anti-gaming checks disabled):

    reviewer        shape                 vacuity
    v1.1.16       78 WARN  repro 11/20    88 PASS  repro 16/20   → both blocked
    weakened      87 PASS  repro 20/20    92 PASS  repro 20/20   → both get through

Run: python run_suite.py --reviewer /path/to/review.py [--threshold 80]
Exit 0 = no probe got through; 1 = at least one did.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(HERE, "probes")

PROBE_RULES = {
    # name: (must be below the pass line, must lose reproducible points)
    "shape": (True, True),
    "vacuity": (False, True),
}


def score(reviewer, pkg):
    p = subprocess.run([sys.executable, reviewer, pkg, "--run"],
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    out = (p.stdout or "") + (p.stderr or "")
    total = re.search(r"(?:总分|total)[：:]\s*(\d+)/100", out)
    repro = re.search(r"reproducible\s+(\d+)/20", out)
    return {
        "total": int(total.group(1)) if total else None,
        "repro": int(repro.group(1)) if repro else None,
    }


def judge(name, r, threshold):
    """Return (blocked, reasons)."""
    must_total, must_repro = PROBE_RULES[name]
    reasons, ok = [], True
    if r["total"] is None:
        return True, ["reviewer printed no score (cannot be fooled by what it cannot read)"]
    if must_total and r["total"] >= threshold:
        ok = False
        reasons.append("total %d >= pass line %d" % (r["total"], threshold))
    if must_repro:
        if r["repro"] is None:
            reasons.append("warn: no reproducible breakdown printed, key rule unverified")
        elif r["repro"] >= 20:
            ok = False
            reasons.append("reproducible %d/20 — a package that verifies nothing earned full marks"
                           % r["repro"])
    return ok, reasons


DEMO_REVIEWER_SRC = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"Demo reviewer for run_suite.py --demo: it always claims 100/100 and full reproducible.
A working red-team suite MUST see this reviewer as GOT THROUGH; that is what proves the
harness is able to catch a rubber stamp.\"\"\"
import sys
print("总分: 100/100")
print("reproducible 20/20")
sys.exit(0)
"""


def make_demo_reviewer(tmpdir):
    p = os.path.join(tmpdir, "demo_reviewer.py")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(DEMO_REVIEWER_SRC)
    return p


def run_demo():
    """No --reviewer: run the harness against a rubber-stamp reviewer we know is foolable.

    The assertion is inverted on purpose: both probes must GOT THROUGH. If a probe says
    BLOCKED here, the harness is the thing that is broken, not the reviewer.
    """
    tmp = tempfile.mkdtemp(prefix="redteam-demo-")
    reviewer = make_demo_reviewer(tmp)
    print("no --reviewer given -> DEMO mode")
    print("reviewer: %s (always prints 100/100)" % reviewer)
    print("expectation: both probes must GOT THROUGH <- that proves the harness can catch a stamp")
    through = 0
    try:
        for name in ("shape", "vacuity"):
            dst = os.path.join(tmp, name)
            shutil.copytree(os.path.join(PROBES, name), dst)
            r = score(reviewer, dst)
            blocked, reasons = judge(name, r, 80)
            print("  %-8s total %s   repro %s   %s"
                  % (name, r["total"],
                     ("%d/20" % r["repro"]) if r["repro"] is not None else "-",
                     "GOT THROUGH (expected)" if not blocked else "BLOCKED <- harness broken"))
            for why in reasons:
                print("           - %s" % why)
            if not blocked:
                through += 1
        print("\nDEMO: %d/%d probes got through as expected" % (through, len(PROBE_RULES)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0 if through == len(PROBE_RULES) else 1

def main():
    ap = argparse.ArgumentParser(description="Red-team a skill reviewer with two fake packages.")
    ap.add_argument("--reviewer", default=None,
                    help="path to a reviewer CLI; omit to run the built-in DEMO (rubber-stamp)")
    ap.add_argument("--threshold", type=int, default=80, help="pass line for the shape probe")
    ap.add_argument("--keep", action="store_true", help="keep a copy of the probes used")
    a = ap.parse_args()

    if a.reviewer is None:
        return run_demo()

    if not os.path.exists(a.reviewer):
        sys.stderr.write("reviewer not found: %s\n" % a.reviewer)
        return 2
    if not os.path.isdir(PROBES):
        sys.stderr.write("probes/ missing next to run_suite.py\n")
        return 2

    tmp = tempfile.mkdtemp(prefix="redteam-")
    fails = 0
    try:
        print("reviewer: %s   pass line: %d" % (a.reviewer, a.threshold))
        for name in ("shape", "vacuity"):
            dst = os.path.join(tmp, name)
            shutil.copytree(os.path.join(PROBES, name), dst)
            r = score(a.reviewer, dst)
            blocked, reasons = judge(name, r, a.threshold)
            print("  %-8s total %s   repro %s   %s"
                  % (name, r["total"],
                     ("%d/20" % r["repro"]) if r["repro"] is not None else "-",
                     "BLOCKED" if blocked else "GOT THROUGH <- hole"))
            for why in reasons:
                print("           - %s" % why)
            if not blocked:
                fails += 1
        print("\n%s" % ("ALL PROBES BLOCKED" if fails == 0 else
                        "%d probe(s) got through - this reviewer can be fooled" % fails))
    finally:
        if a.keep:
            print("probes kept at:", tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
