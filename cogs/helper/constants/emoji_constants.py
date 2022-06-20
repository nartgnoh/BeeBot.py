# *********************************************************************************************************************
# emojiconstants.py
# import cogs.helper.constants.emoji_constants as emoji_constants
# *********************************************************************************************************************

import os
import json

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))


def cute_animals(): return ['🦍 Gorilla', '🦧 Orangutan', '🐶 Dog', '🐺 Wolf', '🦊 Fox', '🦝 Raccoon', '🐱 Cat', '🦁 Lion', '🐯 Tiger', '🐴 Horse',
                            '🦓 Zebra', '🦌 Deer', '🐮 Cow', '🐷 Pig', '🐗 Boar', '🦏 Rhinoceros', '🐭 Mouse', '🐹 Hamster', '🐰 Rabbit', '🦔 Hedgehog',
                            '🦇 Bat', '🐻 Bear', '🐻‍❄️ Polar Bear', '🐨 Koala', '🐼 Panda', '🦥 Sloth', '🦦 Otter', '🐧 Penguin', '🕊️ Dove', '🦅 Eagle',
                            '🦆 Duck', '🦢 Swan', '🦉 Owl', '🦜 Parrot', '🦩 Flamingo', '🐸 Frog', '🐳 Whale', '🐬 Dolphin', '🦈 Shark', '🐙 Octopus',
                            '🐌 Snail', '🦋 Butterfly', '🐝 Bee', '🐞 Ladybug', '🕷️ Spider',
                            '🦛 Hippo', '🐿️ Chipmunk', '🦘 Kangaroo', '🦃 Turkey', '🐓 Rooster', '🐤 Chick', '🐊 Crocodile', '🐢 Turtle', '🦎 Lizard', '🐍 Snake',
                            '🐆 Leopard', '🐂 Ox', '🐃 Buffalo', '🐏 Ram', '🐑 Ewe', '🐐 Goat', '🐫 Camel', '🦙 Llama', '🦒 Giraffe', '🐘 Elephant']


def hearts(): return ["❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍"]


def emojis_list():
    # read emojis.json file
    emojis_json = "/".join(list(current_directory.split('/')
                                [0:-3])) + '/resource_files/json_files/emojis.json'
    with open(emojis_json, "r") as f:
        emojis_list = json.load(f)
    return emojis_list
