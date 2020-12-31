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
from sltools import setup


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
    return RedirectResponse(config.get("SERVER", "redirect"))


@app.get("/404")
def read_notfound():
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
        result = db.get(link.slashtag == slashtag)
        return RedirectResponse(result["link"])
    except:
        return RedirectResponse("/404")


@app.get("/api/all")
def read_all():
    if config.get("SERVER", "visibility") == "public":
        return iter(db)
    else:
        return {"msg": "No permission"}


@app.post("/api/add")
def add_item(linkitem: Link):
    if config.get("SERVER", "key") == linkitem.key:
        slashtagLength = int(config.get("SERVER", "length"))
        if linkitem.slashtag is None:
            slashtag = "".join(random.choices(string.ascii_lowercase + string.digits, k=slashtagLength))
        else:
            slashtag = linkitem.slashtag
        db.insert({"slashtag": slashtag, "link": linkitem.link})
        url = config.get("SERVER", "host")
        return {"msg": "200 - link added", "link": url+"/"+slashtag}
    else:
        return {"msg": "Authentication failed!"}


# START SCRIPT

setup.start()
db = TinyDB("sl/db.json")
config.read("sl/config.ini")
host = config.get("SERVER", "host")
port = int(config.get("SERVER", "port"))
logging = config.get("SERVER", "logging")
uvicorn.run(app, host=host, port=port, log_level=logging)
