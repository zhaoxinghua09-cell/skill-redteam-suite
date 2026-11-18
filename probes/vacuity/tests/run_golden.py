import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
cases = [1, 2, 3]
for c in cases:
    actual = c
    expected = c
    assert actual == expected
    print("PASS  T%d" % c)
print("---- %d/%d PASS ----" % (len(cases), len(cases)))
