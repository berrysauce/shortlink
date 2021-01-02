```
                              __               __  ___       __  
                        _____/ /_  ____  _____/ /_/ (_)___  / /__
                       / ___/ __ \/ __ \/ ___/ __/ / / __ \/ //_/
                      (__  ) / / / /_/ / /  / /_/ / / / / / ,<   
                     /____/_/ /_/\____/_/   \__/_/_/_/ /_/_/|_|  
                                            
```

![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/berrysauce/shortlink)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/berrysauce/shortlink)
![GitHub repo size](https://img.shields.io/github/repo-size/berrysauce/shortlink)
![Python version](https://img.shields.io/badge/python-3.7-blue)

---

# shortlink
Self-hostable link shortening API made with Python

Ever wanted to have your own link shortener for free? With shortlink you can turn long links like `myexampledomain.com/this-is-an-example-post` to `example.co/324nk1`. This has multiple advantages: you can write down and share the links much easier, they look prettier, and you can fit the links character-limited fields (e.g. Tweet).

Shortlink is easy to install and host on any Python 3.7 and pip capable device.

## Requirements
- Python 3 and pip
- a domain
- a computer

## Installation
First of all, clone the GitHub repository with
```
git clone https://github.com/berrysauce/shortlink.git
```
*(if don't have git installed, install it like [this](https://www.git-scm.com/book/en/v2/Getting-Started-Installing-Git))*

Then, navigate to the repository folder with 
```
cd shortlink
```

Now, let's install the requirements needed for shortlink with
```
pip3 install -r requirements.txt
```

After that, you should be set to begin the shortlink setup with 
```
python3 main.py
```
*(This is also the command to start your script)*

The program should prompt you with a few questions. Please read through them carefully!

If the server got started, you're done! Shortlink is now running. You can stop it with `Ctrl + C`.
If you need to change something in your config, edit it with `nano sl/config.ini`. **Please do NOT change the key value since this will lock you out of your API!** If you need to change your password, backup the `db.json` file, re-install shortlink and put it back in the `sl` folder.
