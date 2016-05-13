import logging
import threading
import time
import traceback

import irc.bot
import markovify

import pnw.game
from pnw.data import *

IRC_SERVER = 'irc.coldfront.net'
IRC_CHANNEL = ''
IRC_PORT = 6667
IRC_NICKNAME = 'Megatron'
IRC_PASSWORD = ''
IRC_MASTER = ''
IRC_NICKSERV = 'NickServ'

COMMAND_START = '!'

PNW_GAME = pnw.game.Game(SPRING)
PNW_NATION_LINK = 'https://politicsandwar.com/nation/id='
PNW_SPY_LINK = 'https://politicsandwar.com/nation/espionage/eid='

MARKOV_CORPUS_FILE = 'megatron_corpus.txt'

NATION_WATCH_FILE = 'megatron_nations.cfg'
CHECK_INTERVAL = 55


class MegatronBot(irc.bot.SingleServerIRCBot):

    def __init__(self, server, port, channel, nickname, text_model):

        super().__init__([(server, port)], nickname, nickname)
        self.channel = channel
        self.commands = {}
        self.text_model = text_model

    def on_nicknameinuse(self, c, e):

        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):

        self.identify(IRC_PASSWORD)
        time.sleep(1)
        c.join(self.channel)

    def on_privmsg(self, c, e):

        self.on_pubmsg(c, e)

    def on_pubmsg(self, c, e):

        if e.arguments[0].startswith(COMMAND_START):
            self.do_command(e, e.arguments[0][len(COMMAND_START):].strip())
        elif e.arguments[0].startswith(c.get_nickname()):
            self.do_response(e, e.arguments[0][len(c.get_nickname()):].strip())

    def identify(self, password):

        self.connection.privmsg(IRC_NICKSERV, "IDENTIFY " + password)

    def do_command(self, e, cmd):

        nick = e.source.nick

        args = cmd.split(' ')
        channel = nick if e.type == "privmsg" else self.channel
        try:
            self.commands[args[0]](self, channel, nick, args[1:] if len(args) > 1 else None)
        except:
            traceback.print_stack()

    def add_handler(self, command, function):

        self.commands[command] = function

    def do_response(self, e, prompt):

        channel = e.source.nick if e.type == "privmsg" else self.channel
        combo = markovify.combine(
            [self.text_model, markovify.Text(prompt)], [0.5, 0.5]
        )
        sentence = combo.make_sentence()
        if sentence:
            self.connection.privmsg(channel, sentence)


class NationWatcher:

    def __init__(self, bot):

        self.bot = bot
        self.nations = {}

        self.load_nations(NATION_WATCH_FILE)
        self.check()

    def save_nations(self, filename):

        try:
            with open(filename, 'w') as f:
                f.write(' '.join([str(k) for k in self.nations.keys()]))
        except FileNotFoundError:
            logging.error("Failed to write nation watch list to {}".format(filename))

    def load_nations(self, filename):

        try:
            with open(filename, 'r') as f:
                for i in f.read().split():
                    self.nations[int(i)] = None
        except FileNotFoundError:
            logging.error("Failed to read nation watch list from {}".format(filename))

    def register(self, bot, channel, nick, args):

        if not args or len(args) > 1:
            bot.connection.privmsg(channel, "Usage: !watch nation_id")
            return

        try:
            nation_id = int(args[0])
            if nation_id < 0:
                raise ValueError()
            if nation_id in self.nations:
                bot.connection.privmsg(
                    channel,
                    "Error: already watching {}{}".format(
                        PNW_NATION_LINK,
                        nation_id
                    )
                )
                return
            self.nations[nation_id] = None
            bot.connection.privmsg(
                bot.channel,
                "Now watching {}{} (ordered by {})".format(
                    PNW_NATION_LINK,
                    nation_id,
                    nick
                )
            )
            self.save_nations(NATION_WATCH_FILE)
        except ValueError:
            bot.connection.privmsg(channel, "Error: Invalid nation ID")

    def unregister(self, bot, channel, nick, args):

        if not args or len(args) > 1:
            bot.connection.privmsg(channel, "Usage: !unwatch nation_id")
            return

        try:
            nation_id = int(args[0])
            if nation_id < 0:
                raise ValueError()
            if nation_id not in self.nations:
                bot.connection.privmsg(
                    channel,
                    "Error: not currently watching {}{}".format(
                        PNW_NATION_LINK,
                        nation_id
                    )
                )
                return
            del self.nations[nation_id]
            bot.connection.privmsg(
                bot.channel,
                "No longer watching {}{} (ordered by {})".format(
                    PNW_NATION_LINK,
                    nation_id,
                    nick
                )
            )
            self.save_nations(NATION_WATCH_FILE)
        except ValueError:
            bot.connection.privmsg(channel, "Error: Invalid nation ID")

    def list(self, bot, channel, nick, args):

        bot.connection.privmsg(
            channel,
            "Currently watching: {}".format(
                ' '.join(
                    ['{} ({})'.format(str(i), n)
                     for i, n in self.nations.items()
                    ]
                )
            )
        )

    def check(self):

        threading.Timer(CHECK_INTERVAL, self.check).start()
        logging.info("Checking for changes")
        PNW_GAME.update_nations(self.nations.keys())
        for i, n in self.nations.items():
            if n and self.nations[i] < PNW_GAME.nations[i].nukes:
                self.warn(i)
            self.nations[i] = PNW_GAME.nations[i].nukes

    def warn(self, nation_id):

        logging.warning("Nation #{} built a nuke".format(nation_id))
        users = list(self.bot.channels[self.bot.channel].users())
        users.remove(IRC_NICKNAME)
        self.bot.connection.privmsg(
            self.bot.channel,
            ' '.join(users)
        )
        self.bot.connection.privmsg(
            self.bot.channel,
            "WARNING: {0}{1} has just built a nuke! Spy it now: {2}{1}".format(
                PNW_NATION_LINK, nation_id, PNW_SPY_LINK
            )
        )


def see_nation(bot, channel, nick, args):

    if not args or len(args) < 2:
        bot.connection.privmsg(channel, "Usage: !see nation_id info [spies] [tax]")
        return

    try:
        nation_id = int(args[0])
    except ValueError:
        bot.connection.privmsg(channel, "Error: Invalid nation ID")
        return

    info = args[1]

    spies = 0
    if len(args) > 2:
        try:
            spies = int(args[2])
        except ValueError:
            bot.connection.privmsg(channel, "Error: Invalid spy count")
            return

    tax = 0.0
    if len(args) > 3:
        try:
            tax = float(args[3])
        except ValueError:
            bot.connection.privmsg(channel, "Error: Invalid tax rate")
            return

    PNW_GAME.update_nation_list()

    if nation_id not in PNW_GAME.nations:
        bot.connection.privmsg(channel, "Error: Nation not found")
        return
    nation = PNW_GAME.nations[nation_id]
    bot.connection.privmsg(channel, "Fetching info for '{}'...".format(nation.name))
    PNW_GAME.update_prices()
    PNW_GAME.update_alliance_list(False)
    PNW_GAME.update_nation(nation_id, True)
    nation.spies = spies
    PNW_GAME.update_alliance(nation.alliance_id)
    PNW_GAME.alliances[nation.alliance_id].revenue_tax = tax

    message = "Error: Invalid 'info', must be: gross, net or timer"
    if info == 'gross':
        message = "Money: ${0[0]:,.2f}, Food: {0[1]:,.2f} tons, Coal: {0[2]:,.2f} tons, Oil: {0[3]:,.2f} tons, Uranium: {0[4]:,.2f} tons, Iron: {0[5]:,.2f} tons, Bauxite: {0[6]:,.2f} tons, Lead: {0[7]:,.2f} tons, Gasoline: {0[8]:,.2f} tons, Steel: {0[9]:,.2f} tons, Aluminum: {0[10]:,.2f} tons, Munitions: {0[11]:,.2f} tons".format(nation.production)
    elif info == 'net':
        message = "Money: ${0[0]:,.2f}, Food: {0[1]:,.2f} tons, Coal: {0[2]:,.2f} tons, Oil: {0[3]:,.2f} tons, Uranium: {0[4]:,.2f} tons, Iron: {0[5]:,.2f} tons, Bauxite: {0[6]:,.2f} tons, Lead: {0[7]:,.2f} tons, Gasoline: {0[8]:,.2f} tons, Steel: {0[9]:,.2f} tons, Aluminum: {0[10]:,.2f} tons, Munitions: {0[11]:,.2f} tons".format(nation.revenue)
    elif info == 'timer':
        message = "City Project Timer (Turns Left): " + str(nation.city_project_timer_turns)
    bot.connection.privmsg(channel, message)

def main():

    # Set up logging
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        level=logging.INFO
    )
    logging.info("Megatron bootup sequence initiated")

    # Setup the Markov chain
    with open(MARKOV_CORPUS_FILE) as f:
        text = f.read()
    text_model = markovify.Text(text)

    # Initialize the bot
    bot = MegatronBot(
        IRC_SERVER, IRC_PORT, IRC_CHANNEL, IRC_NICKNAME, text_model
    )
    watcher = NationWatcher(bot)
    bot.add_handler('watch', watcher.register)
    bot.add_handler('unwatch', watcher.unregister)
    bot.add_handler('list', watcher.list)
    bot.add_handler('see', see_nation)
    bot.add_handler('help', lambda b, c, n, a: b.connection.privmsg(
        c,
        "Commands: !help, !watch, !unwatch, !list, !see"
    ))

    # Run the bot
    logging.info("Megatron bootup sequence finished")
    bot.start()

if __name__ == '__main__':
    main()
