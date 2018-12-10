from telegram.ext import Updater
import argparse

from handlers import conv_handler_save, conv_handler_start, conv_handler_delete, \
    conv_handler_list


parser = argparse.ArgumentParser()
parser.add_argument('--token')


def main():

    args = parser.parse_args()

    updater = Updater(args.token)
    dp = updater.dispatcher

    dp.add_handler(conv_handler_start)
    dp.add_handler(conv_handler_save)
    dp.add_handler(conv_handler_delete)
    dp.add_handler(conv_handler_list)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
