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
    italics =  re.sub(r"\[([\w' \"_-]*)\]", f"{UNDERLINE}\\1{UNDERLINE}", s.strip())
    newlines = re.sub(r"\r?\n(\r?\n)*", f" {BOLD}--{BOLD} ", italics)
    return newlines

def urbandictionary_lookup(bot, nick, word):
    if not word:
        bot.say(f"{nick} You must specify something to search")
        return

    defs = []
    try:
        defs = ud.define(word)
    except Exception as e:
        bot.say(f"{nick} {e}")
        return

    if len(defs) == 0:
        bot.say(f"{nick} no results found for {word}")
        return

    defs.sort(key = lambda x: x.upvotes, reverse=True)
    d = defs[0]
    bot.say(f"{BOLD}{d.word}{BOLD}: {ud_conv(d.definition)} {BOLD}Example{BOLD}: {ud_conv(d.example)}", max_messages=3)

@sopel.module.commands('ud')
@sopel.module.example('.ud netflix and chill')
def urbandictionary_lookup_cmd(bot, trigger):
    return urbandictionary_lookup(bot, trigger.nick, trigger.group(2))

@sopel.module.commands('udrw')
@sopel.module.example('.udrw')
def urbandictionary_random_words(bot, trigger):
    bot.say(', '.join([x.word for x in ud.random()]))

@sopel.module.commands('udr')
@sopel.module.example('.udr')
def urbandictionary_random(bot, trigger):
    defs = ud.random()
    defs.sort(key = lambda x: x.upvotes, reverse=True)
    return urbandictionary_lookup(bot, trigger.nick, defs[0].word)
