import pickle
import pathlib
from utils import *


class Username_UDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):

        path= os.path.join('data', "user.pickle")
        user_info_file = pathlib.Path(path)
        if user_info_file.exists():
            with open(path, "rb") as f:
                user_info = pickle.load(f)
            for i in user_info:
                if i.username == value:
                    raise ValueError("Username already exist")
        if 4 >= len(value) or len(value) > 24:
            raise TypeError("Username must contain more than 4 char and less than 24 char")

        instance.__dict__[self.name] = value

class Password_UDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not validate_password(value):
            raise ValueError("Passwords must be at least 8 characters in length,\nand it must include at least one "
                             "capital letter (or uppercase), one lowercase, one number and one special character")
        instance.__dict__[self.name] = hashing(value)

class Email_CDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not validate_email(value):
            raise TypeError("Email address is not Valid")

        instance.__dict__[self.name] = value

class Phone_CDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not validate_phone(value):
            raise TypeError("Phone number is not Valid")

        instance.__dict__[self.name] = value

class Name_CDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        path = os.path.join('data', "contacts.pickle")
        user_info_file = pathlib.Path(path)
        if user_info_file.exists():
            with open(path, "rb") as f:
                user_info = pickle.load(f)
            for i in user_info:
                if i.name == value[0] and i.user.username==value[1].username:
                    raise ValueError("Contact name already exist, choose another name")

        instance.__dict__[self.name] = value[0]

class Category_CDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
