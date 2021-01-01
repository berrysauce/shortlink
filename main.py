from pyfiglet import Figlet
import configparser
from fastapi import FastAPI, Response, status
from tinydb import TinyDB, Query
from fastapi.responses import RedirectResponse, HTMLResponse
import uvicorn
from pydantic import BaseModel
from typing import Optional
import string
import random
from sltools import setup, hashing

'''
        shortlink
-----------------------------
Self-hosted, easy to use link
shortener made in Python 3.7.

License: MIT
Author: berrysauce
'''

# GENERAL SETUP

custom_fig = Figlet(font="slant")
config = configparser.ConfigParser()


class Link(BaseModel):
    slashtag: Optional[str] = None
    link: str
    key: str

class All(BaseModel):
    key: Optional[str] = None

app = FastAPI()

# [...]   Test
# [LOG]   Test
# [ERROR] Test


# API

@app.get("/", status_code=301)
def read_root():
    return RedirectResponse(config.get("SERVER", "redirect"))


@app.get("/404", status_code=404)
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
    return HTMLResponse(content=html_content)


@app.get("/{slashtag}", status_code=301)
def read_item(slashtag: str, response: Response):
    try:
        link = Query()
        result = db.get(link.slashtag == slashtag)
        return RedirectResponse(result["link"])
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return RedirectResponse("/404")


@app.get("/api/all", status_code=200)
def read_all(response: Response, key: Optional[str] = None):
    if config.get("SERVER", "visibility") == "public":
        return iter(db)
    else:
        if hashing.verifypw(key) is True:
            return iter(db)
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"msg": "No permission"}


@app.post("/api/add", status_code=201)
def add_item(linkitem: Link, response: Response):
    if hashing.verifypw(linkitem.key) is True:
        slashtagLength = int(config.get("SERVER", "length"))
        if linkitem.slashtag is None:
            slashtag = "".join(random.choices(string.ascii_lowercase + string.digits, k=slashtagLength))
            db.insert({"slashtag": slashtag, "link": linkitem.link})
            url = config.get("SERVER", "host")
            return {"msg": "Link added", "link": url + "/" + slashtag}
        else:
            link = Query()
            result = db.get(link.slashtag == linkitem.slashtag)
            if result == None:
                slashtag = linkitem.slashtag
            else:
                response.status_code = status.HTTP_409_CONFLICT
                return {"msg": "Already exists!"}

            db.insert({"slashtag": slashtag, "link": linkitem.link})
            url = config.get("SERVER", "host")
            return {"msg": "Link added", "link": url+"/"+slashtag}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg": "Authentication failed!"}


# START SCRIPT

setup.start()
db = TinyDB("sl/db.json")
config.read("sl/config.ini")
host = config.get("SERVER", "host")
port = int(config.get("SERVER", "port"))
logging = config.get("SERVER", "logging")
uvicorn.run(app, host=host, port=port, log_level=logging)
