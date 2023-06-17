import sys
import re


def make_one_string(lst):
    return ' '.join(lst)

def validate_numbers(string):
    num_lst = re.findall(r'[0-9]+',string)
    return num_lst

def gpa(lst):
    return sum(lst) / len(lst)

def make_float(lst):
    return list(map(float,lst))

def main():
    pre_lst = sys.argv[1:]
    my_string= make_one_string(pre_lst)
    numbers_list= list(validate_numbers(my_string))
    float_lst = make_float(numbers_list)
    result = gpa(float_lst)
    return result

if __name__ == '__main__':
    GPA = main()
    print("\033[0;31m" f"GPA: {GPA}" "\033[0m")