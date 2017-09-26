from telegram.ext import Updater
import BotCommands
import BotConfig
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BotUpdater = Updater(token=BotConfig.TOKEN)

BotCommands.RegisterMyCommands(BotUpdater.dispatcher)
BotUpdater.start_polling()
