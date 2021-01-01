import hashlib
import binascii
import os
import configparser

'''
shortlink
sltools/hashing.py

Source: https://www.vitoshacademy.com/hashing-passwords-in-python/
'''

config = configparser.ConfigParser()
config.read("sl/config.ini")


def hashpw(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwhash = binascii.hexlify(pwhash)
    return (salt + pwhash).decode('ascii')


def verifypw(provided_password):
    stored_password = config.get("SERVER", "key")
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwhash = binascii.hexlify(pwhash).decode('ascii')

    if pwhash == stored_password:
        return True
    else:
        return False