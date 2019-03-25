from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction

tasks = []


# define a command handler. Command handlers usually take two arguments:
# bot and update
def showTasks(bot, update):
    if len(tasks) == 0:
        update.message.reply_text("Nothing to do, here! ")
    else:
        update.message.reply_text(tasks)


def newTask(bot, update,args):
    global tasks
    tasks.append(" ".join(args))
    update.message.reply_text("The new task was successfully added to the list!")


def removeTask(bot, update, args):
    global tasks
    msg = " The task was successfully deleted! "
    try:
        tasks.remove(" ".join(args))
    except ValueError:
        msg = "The task you specified is not in the list!"
    update.message.reply_text(msg)


def removeAllTasks(bot, update, args):
    msg = "The elements "
    global tasks
    to_del = [x for x in tasks if " ".join(args) in x]
    for x in to_del:
        msg = msg + '"' + x + '" '
    msg = msg + "where removed"
    tasks = [x for x in tasks if not " ".join(args) in x]
    print(msg)

    update.message.reply_text(msg)


# the non-command handler
def echo(bot, update):
    # simulate typing from the bot
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)

    # get the message from the user
    # repeat_text = update.message.text
    # send the message back
    update.message.reply_text("Sorry, commands only!")
    # alternative way: bot.sendMessage(update.message.chat_id, repeat_text)


def main():
    updater = Updater("TOKEN")

    # get the dispatcher to register handlers
    dp = updater.dispatcher

    # add the command handler for the "/start" command
    dp.add_handler(CommandHandler("showTasks", showTasks))
    dp.add_handler(CommandHandler("newTask", newTask, pass_args=True))
    dp.add_handler(CommandHandler("removeTask", removeTask, pass_args=True))
    dp.add_handler(CommandHandler("removeAllTasks", removeAllTasks, pass_args=True))
    # another example of CommandHandler...
    # dp.add_handler(CommandHandler("help", help))

    # on non-command textual messages - echo the original message
    dp.add_handler(MessageHandler(Filters.text, echo))

    # start the bot
    updater.start_polling()

    # run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
