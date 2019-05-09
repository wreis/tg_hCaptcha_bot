"""Bot for Telegram groups using hCaptcha

A bot to end spam on telegram.
"""

import logging
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
from tg_hCaptcha_bot.settings import LOG, RESTRICT, BOT_MSGS

logging.basicConfig(
    format=LOG['format'],
    level=LOG['level'],
)

class TghCaptchaBot(Updater):
    """This bot is based on python-telegram-bot

This is an extension on Updater which fetches messages from telegram api
and dispatch to handlers accordingly."""

    def unknown(self, bot, update):
        """Handle unknown command messages received"""

        message = update.message
        if message.from_user.is_bot:
            logging.info('Message from a bot, noop')
            return
        message.reply_text(BOT_MSGS['unknown'])

    def thb_add_restrict(self, bot, update):
        """Restrict the user and forward to the captcha callenge"""

        message = update.message
        if len(message.new_chat_members) > 0:
            member = message.from_user
            logging.info('New member joined')
            bot.restrict_chat_member(
                message.chat_id, member.id,
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
            )
            logging.info('Restricted, forwarding captcha')
            bot.send_message(
                message.chat_id,
                BOT_MSGS['captcha'].format(member.name),
                parse_mode=ParseMode.HTML,
                reply_markup=json.dumps({
                    'inline_keyboard': [ [
                        {
                            'text': RESTRICT['url_text'],
                            'url': RESTRICT['url']
                                + '/'.join(
                                    [
                                        str(urlarg) for urlarg in
                                        [message.chat_id, member.id, member.name]
                                    ]
                                )
                        },
                    ] ],
                }),
            )

    def thb_remove_restrict(self, chat_id, member_id, member_name):
        """Remove user restricted giving it voice to chat"""

        bot = self.bot
        logging.info('User is human')
        bot.restrict_chat_member(
            chat_id, member_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
        bot.send_message(
            chat_id,
            BOT_MSGS['allowed'].format(member_name),
            parse_mode=ParseMode.HTML,
        )

    def thb_add_handlers(self):
        """Attach handlers to the dispatcher component"""

        self.dispatcher.add_handler(
            MessageHandler(
                Filters.status_update.new_chat_members, self.thb_add_restrict
            )
        )
        self.dispatcher.add_handler(
            MessageHandler(Filters.command, self.unknown)
        )

    def run(self):
        """Main bot method, run!"""

        logging.info('Adding handlers')
        self.thb_add_handlers()
        self.start_polling()
        logging.info('Watching...')
        self.idle()
