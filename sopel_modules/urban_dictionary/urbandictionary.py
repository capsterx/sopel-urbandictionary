from sopel.module import commands, example
from sopel import web

import sopel.module
import socket

import re

import urbandictionary as ud

BOLD=chr(0x02)
ITALICS=chr(0x1D)
UNDERLINE=chr(0x1F)

def ud_conv(s):
    return re.sub(r"\[([\w' \"_-]*)\]", f"{UNDERLINE}\\1{UNDERLINE}", s)

@sopel.module.commands('ud')
@sopel.module.example('.ud netflix and chill')
def urbandictionary_lookup(bot, trigger):
    if not trigger.group(2):
        bot.say(f"{trigger.nick} You must specify something to search")
        return

    defs = []
    try:
        defs = ud.define(trigger.group(2))
    except Exception as e:
        bot.say(f"{trigger.nick} {e}")
        return

    if len(defs) == 0:
        bot.say(f"{trigger.nick} no results found for {trigger.group(2)}")
        return

    defs.sort(key = lambda x: x.upvotes, reverse=True)
    d = defs[0]
    bot.say(f"{BOLD}{d.word}{BOLD}: {ud_conv(d.definition)} {BOLD}Example{BOLD}: {ud_conv(d.example)}", max_messages=3)
