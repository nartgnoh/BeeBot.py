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
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.8
```

* Install discord.py
```
python3 -m pip install -U discord.py
```
* Install dotenv
```
pip install python-dotenv
```
  
### Installing
Run in Terminal:
```
git clone git@github.com:nartgnoh/Discord_Beebot.git
```

### Setup

* Create a .env file and add the specified tokens
```
# .env
DISCORD_TOKEN=$INSERT DISCORD TOKEN$
TENOR_KEY=$INSERT TENOR TOKEN$
```
Click [here](https://discord.com/developers/applications/) to find steps for a Discord token.
Click [here](https://tenor.com/gifapi) to find steps for a Tenor token.

* Download python3, pip, discord.py

### Executing program
You can either run BeeBot.py locally or on a Google Cloud VM
#### Running Locally
* Run locally using;
```
python3 bee_bot.py
```

#### Running on Google Cloud Platform VM
* Create an instances the on [Google Cloud Platform](https://console.cloud.google.com/compute/instances)
* Setup an SSH connection and clone the repo
* Don't forget the .env file as specified in the "Setup" section!
* Now to run BeeBot.py in the background:
```
# First make sure bee_bot.py is in an executable state
chmod +x bee_bot.py
```
```
# To run the python
```
* ## Authors

* Hong Tran [@nartgnoh](https://github.com/nartgnoh)
