from sopel.module import commands, example
from sopel import web

import sopel.module
import socket

import urbandictionary as ud

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
    bot.say(f"{d.word}: {d.definition} | example: {d.example}")
