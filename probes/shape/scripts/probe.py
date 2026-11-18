import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--flag-a", action="store_true")
args = ap.parse_args()
print("ok")
