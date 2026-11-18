import argparse

ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd")
p_check = sub.add_parser("check")
p_list = sub.add_parser("list")
for p in (p_check, p_list):
    p.add_argument("path", nargs="?")
    p.add_argument("--root", default=".")
a = ap.parse_args()
print("ok")
