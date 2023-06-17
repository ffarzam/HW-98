import sys

def gpa(lst):
    return sum(lst) / len(lst)

def make_float(lst):
    return list(map(float,lst))

def main():
    pre_lst = sys.argv[1:]
    float_lst = make_float(pre_lst)
    result = gpa(float_lst)
    return result

if __name__ == '__main__':
    GPA = main()
    print("\033[0;31m" f"GPA: {GPA}" "\033[0m")

