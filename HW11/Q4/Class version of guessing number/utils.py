import os
import hashlib
import re


def validate_password(pwd):
    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%_^&.*-]).{8,}$"
    match = re.match(password_pattern, pwd)
    return bool(match)

def validate_email(email):
    password_pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-z0-9.-]+[.]\S{2,3}$"
    match = re.match(password_pattern, email)
    return bool(match)

def validate_phone(phone):
    password_pattern = r"^(09(\d{9}))$"
    match = re.match(password_pattern, phone)
    return bool(match)

def hashing(unhashed_pass, salt=None):
    if salt is None:
        salt = os.urandom(32)
        hashed_pass = hashlib.pbkdf2_hmac('sha256', unhashed_pass.encode('utf-8'), salt, 100000)
        return {'salt': salt, 'key': hashed_pass}
    else:
        hashed_pass = hashlib.pbkdf2_hmac('sha256', unhashed_pass.encode('utf-8'), salt, 100000)
        return {'salt': salt, 'key': hashed_pass}