import random as rnd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--start", required=True, type=int)
parser.add_argument("-e", "--end", required=True, type=int)
parser.add_argument("-g", "--guess", required=True, type=int)
args = parser.parse_args()

objective = rnd.randint(args.start, args.end)
print(objective)
count = 1
while True:
    print("\033[0;31m"f"Enter number #{count}""\033[0m")
    num = int(input("\033[0;32m""Enter your number:""\033[0m"))
    if num == objective:
        print("\033[0;34m""Congratulation, You Won. Your guess was correct""\033[0m")
        break
    elif count == args.g:
        print("\033[0;35m""Sorry, You lost. None of your guess was correct.""\033[0m")
        break
    else:
        print("\033[0;36m" f"Your guess was incorrect. You have {args.g - count} more guess""\033[0m")
        if num < objective:
            print("\33[0;36m" "Enter Higher Number" "\033[0;m")
        elif num > objective:
            print("\33[0;36m" "Enter Lower Number" "\033[0;m")

        count += 1
