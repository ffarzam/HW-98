from validators import *
import pathlib
import pickle
import os


class User:
    username = Username_UDescriptor()
    password = Password_UDescriptor()

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def register(cls, username, password):
        return cls(username, password)

    @staticmethod
    def get_file_path():
        path = os.path.join('data', "user.pickle")
        return path

    @staticmethod
    def read_file():
        with open(User.get_file_path(), 'rb') as f:
            info = pickle.load(f)
            return info

    @staticmethod
    def write_file(info):
        with open(User.get_file_path(), 'wb') as f:
            pickle.dump(info, f)

    def save(self):
        info_file = pathlib.Path(self.get_file_path())
        if info_file.exists():
            info = self.read_file()
            info.append(self)
            self.write_file(info)
        else:
            with open(self.get_file_path(), 'wb') as f:
                pickle.dump([self], f)

    @classmethod
    def login(cls, username, password):
        info_file = pathlib.Path(cls.get_file_path())
        if info_file.exists():
            users = cls.read_file()
            for user in users:
                if user.username == username and user.password == hashing(password, user.password["salt"]):
                    return True  # return user
            return False

    @classmethod
    def get_user(cls, username, password):
        all_users = cls.read_file()
        for user in all_users:
            if user.username == username and user.password == hashing(password, user.password["salt"]):
                return user
