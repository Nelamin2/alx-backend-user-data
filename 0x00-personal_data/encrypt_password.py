#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a salted, hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


if __name__ == '__main__':
    password = "eggcellent"
    hashed_password = hash_password(password)
    print(hashed_password)
    print(is_valid(hashed_password, password))
    print(is_valid(hashed_password, "eggs"))
