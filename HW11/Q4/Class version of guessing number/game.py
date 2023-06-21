import random
import pathlib
import pickle
import os


class Game:

    def __init__(self, min_num, max_num, guess_num, username):

        self.max_num = max_num
        self.min_num = min_num
        self.guess_num = guess_num
        self.username = username
        self.guess_count = 1

    def make_guess(self):
        try:
            print("\033[0;31m"f"Enter number #{self.guess_count}""\033[0m")
            self.guess = int(input("\033[0;32m""Enter your number:""\033[0m"))
        except ValueError:
            print('Not a valid guess.')
            return False
        return True

    def play(self):
        self.objective = random.randint(0, self.max_num)
        print(self.objective)

        self.point = self.get_points(self.username)

        while True:

            if not self.make_guess():
                continue

            if self.guess == self.objective:
                print("\033[0;34m""Congratulation, You Won. Your guess was correct""\033[0m")
                self.point += (self.guess_num - self.guess_count + 1) * 20
                self.save_points()
                break
            elif self.guess_count == self.guess_num:
                print("\033[0;35m""Sorry, You lost. None of your guess was correct.""\033[0m")
                self.point -= 50
                self.save_points()
                break
            else:
                print("\033[0;36m" f"Your guess was incorrect. You have {self.guess_num} more guess""\033[0m")
                if self.guess < self.objective:
                    print("\33[0;36m" "Enter Higher Number" "\033[0;m")
                elif self.guess > self.objective:
                    print("\33[0;36m" "Enter Lower Number" "\033[0;m")
                self.guess_count += 1

    @staticmethod
    def get_file_path():
        path = os.path.join('data', "points.pickle")
        return path

    @classmethod
    def read_file(cls):
        with open(cls.get_file_path(), 'rb') as f:
            info = pickle.load(f)
            return info

    @classmethod
    def write_file(cls, info):
        with open(cls.get_file_path(), 'wb') as f:
            pickle.dump(info, f)

    def save_points(self):
        info_file = pathlib.Path(self.get_file_path())
        if info_file.exists():
            info = self.read_file()
            for item in info:
                if item["username"] == self.username:
                    info.remove(item)
                    break

            info.append({"username": self.username, "points": self.point})
            self.write_file(info)
        else:
            with open(self.get_file_path(), 'wb') as f:
                pickle.dump([{"username": self.username, "points": self.point}], f)

    @classmethod
    def get_points(cls, username):
        info_file = pathlib.Path(cls.get_file_path())
        if info_file.exists():
            info = cls.read_file()
            for i in info:
                if i['username'] == username:
                    points = i['points']
                    return points
            points = 100
            return points
        else:
            points = 100
            return points
