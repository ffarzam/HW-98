from actions import *
import logging

logging.basicConfig(format="%(levelname)s (%(asctime)s): %(message)s (line: %(lineno)d [%(filename)s])",
                    filename='user.log', level=logging.DEBUG, encoding="utf-8", datefmt="%Y/%m/%d %I:%M:%S %p")

import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--start", required=True, type=int)
parser.add_argument("-e", "--end", required=True, type=int)
parser.add_argument("-g", "--guess", required=True, type=int)
args = parser.parse_args()

while True:

    do_what = input("User Panel \n1)Sign-up \n2)Sign-in\n3)Exit\n ----> ")

    if do_what == "1":
        while True:
            # try:
            user = sign_up()
            save_user(user)
            break
        # except Exception as e:
        #     print(simple_colors.red(e))

    elif do_what == "2":
        username = input(simple_colors.blue("Enter your username: "))
        password = input(simple_colors.blue("Enter your password: "))

        if user := User.login(username, password):
            print(simple_colors.green("You've logged in successfully!"))
            print("Let's guess!")
            logging.info(f"User {username} Logged in")

            while True:
                do_what = input("What do u want to do?\n1)Start the game\n2)I try it another time"
                                "\n3)Show my points\n4)Exit\n")

                if do_what == "1":
                    main_game(args.start, args.end, args.guess, username)

                elif do_what == "2":
                    logging.info(f"user {username} logged out")
                    break
                elif do_what=="3":
                    show_points(username)

                elif do_what == "4":
                    logging.info(f"user {username} logged out")
                    exit()

                else:
                    print(simple_colors.red("Wrong Input! Try again:"))

        else:
            logging.info(f"Unsuccessful attempted to log in as {username}")
            print(simple_colors.red("User not found"))

    elif do_what == "3":
        exit()

    else:
        print(simple_colors.red("Wrong Input! Try again:"))
