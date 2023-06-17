import argparse
import pathlib
import os


def get_dir_size(path):
    size = 0
    for i in os.scandir(args.d):
        if os.path.isfile(i):
            size += os.path.getsize(i)
        else:
            size+=get_dir_size(i)
    return size

def get_file_size(path):
    if os.path.exists(path):
        return os.path.getsize(path)
    return f"No file with that name"

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-d",type=pathlib.Path)
group.add_argument("-f",type = pathlib.Path)
args=parser.parse_args()


if args.d:

    final_size=get_dir_size(args.d)
    print("\033[0;31m" f"Size: {(final_size / 1024)} KB" "\033[0m")

elif args.f:
    final_size = get_file_size(args.f)
    if isinstance(final_size,str):
        print("\033[0;31m" f"{final_size} " "\033[0m")
    else:
        print("\033[0;31m" f"Size: {(final_size / 1024)} KB" "\033[0m")


