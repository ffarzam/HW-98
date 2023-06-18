import argparse
import pathlib
import os


def get_dir_size(path):
    size = 0
    for i in os.scandir(path):
        if os.path.isfile(i):
            size += os.path.getsize(i)
        else:
            size+=get_dir_size(i)
    return size

def get_file_size(path):
    if os.path.exists(path):
        return os.path.getsize(path)
    return f"No file with that name"

def get_size_extension(path,file_format):
    size = 0
    for i in os.scandir(path):
        if os.path.isfile(i):
            if i.name.endswith(f".{file_format}"):
                size += os.path.getsize(i)
        else:
            size += get_size_extension(i,file_format)
    return size

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-d",type=pathlib.Path)
group.add_argument("-f",type = pathlib.Path)
parser.add_argument("-F",type = str)
args=parser.parse_args()

if args.d:
    if args.F:
        final_size = get_size_extension(args.d, args.F)
        print("\033[0;31m" f"Size: {(final_size / 1024)} KB" "\033[0m")
    else:
        final_size = get_dir_size(args.d)
        print("\033[0;31m" f"Size: {(final_size / 1024)} KB" "\033[0m")

elif args.f:
    final_size = get_file_size(args.f)
    if isinstance(final_size,str):
        print("\033[0;31m" f"{final_size} " "\033[0m")
    else:
        print("\033[0;31m" f"Size: {(final_size / 1024)} KB" "\033[0m")