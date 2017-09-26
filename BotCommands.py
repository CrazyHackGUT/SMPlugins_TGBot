import BotHelpers
import telegram
from telegram.ext import Filters
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler

import SourcePawnBuilder

# Command Handlers
def OnStartTyped(bot, update):
    bot.send_message(
        chat_id    = update.message.chat_id,
        text       = "Hello! I'm bot-builder. I can build plugins. Send me the files for compilation, and I'll compile them.\n<b>You can attach your own include-files</b>. Just send me command /addinc and send me in reply your include file. I save him in your own directory.\n\n<b>My GitHub</b>: https://github.com/CrazyHackGUT/SMPlugins_TGBot",
        parse_mode = telegram.ParseMode.HTML
    )

def OnAddIncTyped(bot, update):
    bot.send_message(
        chat_id             = update.message.chat_id,
        reply_to_message_id = update.message.message_id,
        text                = "Now, send me your include file. He it should be in format <b>.inc</b>. If he placed in subdir (<b>/include/shop/</b> for example), also send me in caption, where he should be placed.",
        parse_mode          = telegram.ParseMode.HTML,
        reply_markup        = telegram.ForceReply(True)
    )

def OnDelIncTyped(bot, update):
    CmdArgs = update.message.text.split(" ", 2)
    OwnerID = update.message.chat_id
    if update.message.from_user:
        OwnerID = update.message.from_user.id

    if len(CmdArgs) == 1:
        bot.send_message(
            chat_id             = update.message.chat_id,
            reply_to_message_id = update.message.message_id,
            text                = "<b>Usage</b>: /delinc emitsoundany\nDelete <em>emitsoundany</em> if he uploaded by user.",
            parse_mode          = telegram.ParseMode.HTML
        )
    else:
        CmdArgs[1] = BotHelpers.PreparePath(CmdArgs[1])
        szFilePath = "SPComp/user_includes/{}/{}.inc".format(OwnerID, CmdArgs[1])
        if BotHelpers.FileExists(szFilePath):
            BotHelpers.Rm(szFilePath)
            bot.send_message(
                chat_id             = update.message.chat_id,
                reply_to_message_id = update.message.message_id,
                text                = "<b>Done!</b> Include file <em>{}</em> has been deleted.".format(CmdArgs[1]),
                parse_mode          = telegram.ParseMode.HTML
            )
            return

        bot.send_message(
            chat_id             = update.message.chat_id,
            reply_to_message_id = update.message.message_id,
            text                = "<b>Error.</b> Include file <em>{}</em> not found.".format(CmdArgs[1]),
            parse_mode          = telegram.ParseMode.HTML
        )

def OnListIncTyped(bot, update):
    bot.send_message(
        chat_id             = update.message.chat_id,
        reply_to_message_id = update.message.message_id,
        text                = "<b>This function not ready for usage!</b>",
        parse_mode          = telegram.ParseMode.HTML
    )

# File Handler
def OnFileReceived(bot, update):
    if not update.message.document.file_name.endswith(".inc"):
        bot.send_message(
            chat_id             = update.message.chat_id,
            reply_to_message_id = update.message.message_id,
            text                = "<b>Incorrect file!</b>\n\nYour include must use <b>.inc</b> file extension!",
            parse_mode          = telegram.ParseMode.HTML
        )
        return

    hMsg = bot.send_message(
        chat_id             = update.message.chat_id,
        reply_to_message_id = update.message.message_id,
        text                = "<b>Process</b>: Requesting URL from Telegram Bot API...",
        parse_mode          = telegram.ParseMode.HTML
    )

    OwnerID = update.message.chat_id
    if update.message.from_user:
        OwnerID = update.message.from_user.id
    BotHelpers.Mkdir("SPComp/user_includes/{}".format(OwnerID))

    try:
        hFile = bot.getFile(file_id = update.message.document.file_id)

        bot.edit_message_text(
            chat_id    = update.message.chat_id,
            message_id = hMsg.message_id,
            text       = "<b>Process</b>: Downloading...",
            parse_mode = telegram.ParseMode.HTML
        )

        if update.message.caption == None:
            hFile.download("SPComp/user_includes/{}/{}".format(OwnerID, update.message.document.file_name))
        else:
            BotHelpers.Mkdir("SPComp/user_includes/{}/{}".format(OwnerID, update.message.caption))
            hFile.download("SPComp/user_includes/{}/{}/{}".format(OwnerID, update.message.caption, update.message.document.file_name))

        bot.edit_message_text(
            chat_id    = update.message.chat_id,
            message_id = hMsg.message_id,
            text       = "<b>Done!</b> Include-file <b>{}</b> ready for usage!".format(update.message.document.file_name.replace(".inc", "")),
            parse_mode = telegram.ParseMode.HTML
        )
    except:
        bot.edit_message_text(
            chat_id    = update.message.chat_id,
            message_id = hMsg.message_id,
            text       = "<b>Error!</b> Something went wrong. Try again later.",
            parse_mode = telegram.ParseMode.HTML
        )


def OnPluginReceived(bot, update):
    if not update.message.document.file_name.endswith(".sp"):
        bot.send_message(
            chat_id             = update.message.chat_id,
            reply_to_message_id = update.message.message_id,
            text                = "<b>Incorrect file!</b>\n\nYour plugin must use <b>.sp</b> file extension!",
            parse_mode          = telegram.ParseMode.HTML
        )
        return

    OwnerID = update.message.chat_id
    if update.message.from_user:
        OwnerID = update.message.from_user.id

    hMsg = bot.send_message(
        chat_id             = update.message.chat_id,
        reply_to_message_id = update.message.message_id,
        text                = "<b>Progress</b>: Downloading file...\nPlease, wait!",
        parse_mode          = telegram.ParseMode.HTML
    )

    #hFile = telegram.File(update.message.document.file_id, bot)
    hFile = bot.getFile(file_id = update.message.document.file_id)
    BotHelpers.Mkdir("UserPlugins/{}".format(OwnerID))

    hFile.download("UserPlugins/{}/{}".format(OwnerID, update.message.document.file_name))

    bot.edit_message_text(
        chat_id    = hMsg.chat_id,
        message_id = hMsg.message_id,
        text       = "<b>Process</b>: Compiling...\nPlease, wait!",
        parse_mode = telegram.ParseMode.HTML
    )

    # Make dir for user includes if not exists
    BotHelpers.Mkdir("SPComp/user_includes/{}".format(OwnerID))

    # Build
    hPlugin = SourcePawnBuilder.Plugin(
        "UserPlugins/{}/{}".format(OwnerID, update.message.document.file_name),
        "UserPlugins/{}/{}".format(OwnerID, update.message.document.file_name.replace(".sp", "")),
        [
            "SPComp/core_includes",
            "SPComp/shared_includes",
            "SPComp/user_includes/{}".format(OwnerID)
        ]
    )

    if hPlugin.ExitCode != 0:
        bot.edit_message_text(
            chat_id    = hMsg.chat_id,
            message_id = hMsg.message_id,
            text       = "<b>Failed!</b>\n\n<pre>{}</pre>".format(hPlugin.CmdResponse),
            parse_mode = telegram.ParseMode.HTML
        )
    else:
        bot.edit_message_text(
            chat_id    = hMsg.chat_id,
            message_id = hMsg.message_id,
            text       = "<b>Success!</b>\n\n<pre>{}</pre>".format(hPlugin.CmdResponse),
            parse_mode = telegram.ParseMode.HTML
        )

        bot.sendChatAction(
            chat_id = hMsg.chat_id,
            action  = telegram.ChatAction.UPLOAD_DOCUMENT
        )

        hFile = open("UserPlugins/{}/{}".format(OwnerID, update.message.document.file_name.replace(".sp", ".smx")), "rb")
        bot.sendDocument(
            chat_id  = hMsg.chat_id,
            document = hFile
        )
        hFile.close()
        BotHelpers.Rm("UserPlugins/{}/{}".format(OwnerID, update.message.document.file_name.replace(".sp", ".smx")))
    BotHelpers.Rm("UserPlugins/{}/{}".format(OwnerID, update.message.document.file_name))

# Commands register
def RegisterMyCommands(DispatcherInstance):
    DispatcherInstance.add_handler(
        CommandHandler(
            'start',
            OnStartTyped
        )
    )

    # Includes
    DispatcherInstance.add_handler(
        CommandHandler(
            'addinc',
            OnAddIncTyped
        )
    )

    DispatcherInstance.add_handler(
        CommandHandler(
            'delinc',
            OnDelIncTyped
        )
    )

    DispatcherInstance.add_handler(
        CommandHandler(
            'listinc',
            OnListIncTyped
        )
    )

    # MsgHandler
    DispatcherInstance.add_handler(
        MessageHandler(
            Filters.document & Filters.reply,
            OnFileReceived
        )
    )

    DispatcherInstance.add_handler(
        MessageHandler(
            Filters.document,
            OnPluginReceived
        )
    )
