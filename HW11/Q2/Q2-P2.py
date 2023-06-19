import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-g", "--grades", nargs="+", type=float)
parser.add_argument("-f", "--float", default=2, type=int)
args = parser.parse_args()

GPA = sum(args.grades) / len(args.grades)

print("\033[0;31m"f"{GPA =: .{args.float}f}" "\033[0m")