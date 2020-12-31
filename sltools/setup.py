import configparser
import os
from pyfiglet import Figlet

custom_fig = Figlet(font="slant")
config = configparser.ConfigParser()


def start():
    print(custom_fig.renderText("shortlink"))
    print("Version: 1.0.0 \nLicense: MIT \nAuthor: berrysauce\n")
    try:
        with open("sl/config.ini", "r") as f:
            f.read()
    except IOError:
        print("[...]   Starting setup - no config found")
        print(50 * "-")
        print("Welcome to shortlink! Please follow this setup \nbefore you continue using shortlink.")
        print("You can change these settings later by editing the values in sl/config.ini.")

        print(" \n[1/7] What's your domain name? Press enter to use the default (localhost).")
        domain = input("(example.com) >>> ")
        if not domain:
            domain = "127.0.0.1"

        print(" \n[2/7] What's your desired port? Press enter to use the default (8000).")
        port = input("(number) >>> ")
        if not port:
            port = "8000"

        print(" \n[3/7] Where should we redirect users when they visit the root? You can use your homepage domain here. Press enter to use the default (/404).")
        redirect = input("(domain) >>> ")
        if not redirect:
            redirect = "/404"

        print(" \n[4/7] What logging level do you wish? Press enter to use the default (info).")
        logging = input("(info/debug) >>> ")
        if not logging:
            logging = "info"

        print(" \nexample.com/423dn3")
        print("   (This part ^^)")
        print(" \n[5/7] How long should the slashtag be? Press enter to use the default (7).")
        length = input("(number) >>> ")
        if not length:
            length = 7

        print(" \n[6/7] Should all links be publicly visible? Press enter to use the default (private).")
        visibility = input("(public/private) >>> ")
        if not visibility:
            visibility = "private"

        print(" \n[7/7] Please enter your Password for accessing the API. Keep this secret!")
        key = input("(your password) >>> ")

        print(50 * "-")
        print("[...]   Creating config")
        os.mkdir("sl")

        config["SERVER"] = {"host": domain,
                            "port": port,
                            "redirect": redirect,
                            "length": length,
                            "logging": logging,
                            "visibility": visibility,
                            "key": key}
        with open("sl/config.ini", "w") as configfile:
            config.write(configfile)
        print("[...]   Created config")

        print("[...]   Creating database")
        with open("sl/db.json", "w") as database:
            database.write("")

        print("[...]   Created database")

    finally:
        print("[...]   Starting your server")
