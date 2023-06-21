from users import User
import logging
import simple_colors
import datetime
from game import Game


def sign_up():
    username = input(simple_colors.blue("Enter your username: "))
    password = input(simple_colors.blue("Enter your password:"))
    # password = pwinput.pwinput(prompt=simple_colors.blue("Enter your password: "), mask='*')

    user = User.register(username, password)

    print(simple_colors.green("You've registered successfully!"))
    logging.info(f"User {username} registered successfully")
    return user


def save_user(user):
    user.save()


def main_game(start,end,guess,username):

    game = Game(start,end,guess,username)
    game.play()


def show_points(username):
    points=Game.get_points(username)
    print(points)

