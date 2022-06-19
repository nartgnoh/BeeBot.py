# BeeBot.py

A cute bee-themed Discord.py bot for my personal Discord server.

![BeeBot](SmileBee.png)

## Description

Welcome to BeeBot.py!

Code-base for a bee-themed Discord.py bot who responds with cute and helpful reactions, helps with organizing game nights, plays music and much more!

## Getting Started

### Dependencies

* Runs on Python3 and pip
```
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.8
```

* Install discord.py
```
$ pip install discord.py
```
* Install dotenv
```
$ pip install python-dotenv
```
* Install Riotwatcher
```
$ pip install riotwatcher
```
* Install discord-pretty-help
```
$ pip install discord-pretty-help
```
  
### Installing

Run in Terminal:
```
$ git clone git@github.com:nartgnoh/Discord_Beebot.git
```

### Setup

* Create a .env file and add the specified tokens
```
$ echo "# .env
DISCORD_TOKEN=$INSERT DISCORD TOKEN$
TENOR_KEY=$INSERT TENOR TOKEN$
RIOT_LOL_KEY=$INSERT RIOT API LOL KEY$" > .env
```
Click [here](https://discord.com/developers/applications/) to find steps for a Discord token and [here](https://discordpy.readthedocs.io/en/stable/api.html) for useful docs.

Click [here](https://tenor.com/gifapi) to find steps for a Tenor token and [here](https://tenor.com/gifapi/documentation) for useful docs.

Click [here](https://developer.riotgames.com/) to find steps for a Riot API key, [here](https://developer.riotgames.com/apis) for useful docs, and [here](https://developer.riotgames.com/docs/lol) for data dragon.

## Executing program

You can either run BeeBot.py locally or on a Google Cloud VM
### Running Locally

* Go through the "Getting Started" section above
* Run locally using;
```
$ cd BeeBot.py
$ python3 bee_bot.py
```

### Running on Google Cloud Platform VM

* Create an instances the on [Google Cloud Platform](https://console.cloud.google.com/compute/instances)
* Setup an [SSH connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
* Go through the "Getting Started" section above
* First make sure bee_bot.py is in an executable state
```
$ cd BeeBot.py
$ chmod +x bee_bot.py
```
* These commands will be helpful with navigating the running processes of BeeBot.py:
```
### CD into BeeBot.py directory
$ cd BeeBot.py

### Run bee_bot.py
$ nohup python3 -u bee_bot.py &>> activity.log &

### Lookup all python3 processes
$ ps -ef | grep python3

### To kill bee_bot.py process
### First lookup bee_bot.py process
$ ps -ef | grep python3
### Looks like this: user+    1224     936 14 04:54 pts/0    00:00:00 python3 -u bee_bot.py
### Using the number of the process, kill the process
$ kill 1224
```
* ## Authors

* Hong Tran [@nartgnoh](https://github.com/nartgnoh)
