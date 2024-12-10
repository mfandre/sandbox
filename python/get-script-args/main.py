import argparse

parser = argparse.ArgumentParser(description='test')
args, unknown = parser.parse_known_args()

print(args, unknown)