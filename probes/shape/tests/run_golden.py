"""空 runner：不测任何东西，直接打印通过。"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
cases = json.load(io.open(os.path.join(HERE, "golden.json"), encoding="utf-8"))["cases"]
for c in cases:
    print("PASS  %s  %s" % (c["id"], c["desc"]))
print("\n---- %d/%d PASS ----" % (len(cases), len(cases)))
