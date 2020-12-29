from pyfiglet import Figlet
import configparser
from fastapi import FastAPI
from tinydb import TinyDB, Query
import os
from fastapi.responses import RedirectResponse, HTMLResponse
import uvicorn
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import string
import random
from inspect import getsourcefile


# GENERAL SETUP

custom_fig = Figlet(font="slant")
config = configparser.ConfigParser()

class Link(BaseModel):
    slashtag: Optional[str] = None
    link: str
    key: str

app = FastAPI()

# [...]   Test
# [LOG]   Test
# [ERROR] Test


# API

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/404")
def read_root():
    html_content = """
        <html>
            <head>
                <title>Page not found - 404</title>
            </head>
            <body>
                <h1>404</h1>
                <p>This link doesn't seem to exist.</p>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content, status_code=404)


@app.get("/{slashtag}")
def read_item(slashtag: str):
    try:
        link = Query()
        #result = db.search(link.slashtag == slashtag)
        result = db.get(link.slashtag == slashtag)
        return RedirectResponse(result["link"])
    except:
        return RedirectResponse("/404")


@app.post("/add")
def add_item(linkitem: Link):
    config.read("sl/config.ini")
    if config.get("SERVER", "key") == linkitem.key:
        slashtagLength = 7
        if linkitem.slashtag is None:
            slashtag = "".join(random.choices(string.ascii_lowercase + string.digits, k=slashtagLength))
        else:
            slashtag = linkitem.slashtag
        db.insert({"slashtag": slashtag, "link": linkitem.link})
        url = config.get("SERVER", "domain")
        return {"msg": "200 - link added", "link": url+"/"+slashtag}
    else:
        return {"msg": "Authentication failed!"}


# SETUP SCRIPT

def start():
    print(custom_fig.renderText("shortlink"))
    print("Version: 1.0.0 \nLicense: MIT \nAuthor: berrysauce\n")
    try:
        with open("sl/config.ini", "r") as f:
            f.read()
    except IOError:
        print("[...]   Starting setup - no config found")
        os.mkdir("sl")
        print(50 * "-")
        print("Welcome to shortlink! Please follow this setup\n before you continue using shortlink.")
        domain = input("\n What's your domain name? Type skip to use localhost. >>> ")
        if domain == "skip":
            domain = "127.0.0.1"
        key = input("\n Please enter your Password for accessing the API. Keep this secret! >>> ")

        print("[...]   Creating config")
        config["SERVER"] = {"domain": domain,
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

start()
db = TinyDB("sl/db.json")
uvicorn.run(app)
