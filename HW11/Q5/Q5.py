import argparse
import pathlib
import os
import sys



sys.setrecursionlimit(20000)

def get_size(path):
    size = 0
    for i in os.scandir(args.d):
        if os.path.isfile(i):
            size += os.path.getsize(i)
        else:
            size+=get_size(path)
    return size

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-d",type=pathlib.Path)
args=parser.parse_args()
final_size=get_size(args.d)


print("\033[0;31m" f"Size: {(final_size/1024)} KB" "\033[0m")


