import uuid

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    ConversationHandler

from constants import FIELDS, NAME
from utilities import merge_sort, validate_field, generate_message
from dao import get_default_redis_dao_object


dao = get_default_redis_dao_object()


STATE_MOVE_TO_NEXT_STEP = 1
REQUESTED_FIELD = 'requested_field'


def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="I am test bot"
    )


def list_users(bot, update):
    try:
        users = dao.get_users()
    except Exception as e:
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Some problems accessing DB. Please, try again later...'
        )
        return ConversationHandler.END

    user_ids = merge_sort(users.keys())

    if len(user_ids) > 0:

        for u in user_ids:
            bot.sendMessage(
                chat_id=update.message.chat_id,
                text="user id: {}\nuser data: {}".format(u, users[u])
            )
    else:
        bot.sendMessage(
                chat_id=update.message.chat_id,
                text='No users'
            )

    return ConversationHandler.END


def request_delete_user(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Enter id of the user you want to delete"
    )
    return STATE_MOVE_TO_NEXT_STEP


def process_delete_user(bot, update):

    user_id = update.message.text
    try:
        exists = dao.get_user(user_id)

        msg = "User doesn't exist"

        if exists:
            dao.delete_user(user_id)
            msg = "User {} deleted".format(user_id)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=msg
        )
    except Exception as e:
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Smth went wrong while accessing DB. Deletion was not completed. "
                 "Please again try later..."
        )
    finally:
        return ConversationHandler.END


def start_saving(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="You start adding user! Enter your name, please"
    )
    return STATE_MOVE_TO_NEXT_STEP


def add_person_field(bot, update, user_data):

    # name is requested immediately after /save command
    if NAME not in user_data:
        user_data[NAME] = update.message.text
    # some fields can be restricted to a specific format (e.g., age - int)
    elif validate_field(user_data[REQUESTED_FIELD], update.message.text):
        user_data[user_data[REQUESTED_FIELD]] = update.message.text
    else:
        update.message.reply_text(
            "Wrong input for field {}\nPlease try again"
                .format(user_data['requested_field'])
        )

        return STATE_MOVE_TO_NEXT_STEP

    # reuse this for all fields
    for field in FIELDS:
        if field not in user_data:
            user_data[REQUESTED_FIELD] = field
            generate_message(bot, update, field)

            return STATE_MOVE_TO_NEXT_STEP

    object_to_save = {i: user_data[i] for i in FIELDS}
    user_data.clear()  # forget added user info

    id_ = uuid.uuid4().hex
    try:
        dao.save_user(id_, object_to_save)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="User {} saved".format(object_to_save)
        )
    except Exception as e:
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Smth went wrong while saving ):"
        )
    finally:
        return ConversationHandler.END


def cancel(bot, update):
    update.message.reply_text('Saving canceled',
                              reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END


conv_handler_start = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={},
    fallbacks=[CommandHandler('cancel', cancel)]
)


conv_handler_save = ConversationHandler(
    entry_points=[CommandHandler('save', start_saving)],
    states={
        STATE_MOVE_TO_NEXT_STEP: [
            MessageHandler(
                Filters.text,
                add_person_field,
                pass_user_data=True
            )
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)


conv_handler_delete = ConversationHandler(
    entry_points=[CommandHandler('delete', request_delete_user)],
    states={
        STATE_MOVE_TO_NEXT_STEP: [
            MessageHandler(
                Filters.text,
                process_delete_user
            )
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)


conv_handler_list = ConversationHandler(
    entry_points=[CommandHandler('list', list_users)],
    states={},
    fallbacks=[CommandHandler('cancel', cancel)]
)
