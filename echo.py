#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, __version__ as TG_VER
from telegram import __version_info__

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class FinanzaPersonale:
    def __init__(self):
        self.conti = {}
        self.storico = []

    def aggiungi_conto(self, nome_conto, saldo_iniziale):
        self.conti[nome_conto] = float(saldo_iniziale)

    def rimuovi_conto(self, nome_conto):
        del self.conti[nome_conto]

    def deposita(self, nome_conto, importo):
        self.conti[nome_conto] += int(importo)
        self.storico.append(("deposito", nome_conto, importo))

    def preleva(self, nome_conto, importo):
        self.conti[nome_conto] -= importo
        self.storico.append(("prelievo", nome_conto, importo))

    def trasferisci(self, conto_origine, conto_destinazione, importo):
        self.preleva(conto_origine, importo)
        self.deposita(conto_destinazione, importo)

    def totale_patrimonio(self):
        return sum(self.conti.values())

    def visualizza_storico(self):
        for operazione in self.storico:
            print(operazione)


# Creiamo un'istanza della classe FinanzaPersonale
mia_finanza = FinanzaPersonale()


# mia_finanza.preleva("Risparmio", 1000) # TODO: catchare l'eccezione
# mia_finanza.trasferisci("Conto Corrente", "Risparmio", 250)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    # await update.message.reply_text("Help!")
    buttons = [[KeyboardButton("/add_wallet")], [KeyboardButton("/get_total")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Help!")
    reply_markup = ReplyKeyboardMarkup(buttons)


async def add_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # """Echo the user message."""
    # await update.message.reply_text(update.message.text)

    # Effettuiamo alcune operazioni
    # mia_finanza.deposita(context.args[0], context.args[1])
    mia_finanza.aggiungi_conto(context.args[0], context.args[1])
    await update.message.reply_text("Wallet creato con successo!")


async def get_tot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(mia_finanza.totale_patrimonio())


async def add_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    mia_finanza.deposita(context.args[0], context.args[1])
    await update.message.reply_text(mia_finanza.totale_patrimonio())


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token("6294770070:AAG4lFdwnL-a-nflyWgjEeWaQKZaSLUSdWA")
        .build()
    )

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add_wallet", add_wallet))
    application.add_handler(CommandHandler("get_total", get_tot))
    application.add_handler(CommandHandler("add_transaction", add_transaction))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
