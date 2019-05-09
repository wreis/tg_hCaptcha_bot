"""Test script"""

import unittest
from telegram import Update, Chat, Message, User
from unittest.mock import MagicMock
from tg_hCaptcha_bot.settings import TELEGRAM
from tg_hCaptcha_bot import TghCaptchaBot

class TestGetMe(unittest.TestCase):
    """TestGetMe unit tests"""

    bot = TghCaptchaBot(TELEGRAM['token']).bot
    bot_info = bot.get_me()

    def test_id(self):
        """Assert bot id"""

        self.assertEqual( TestGetMe.bot_info['id'], TELEGRAM['id'] )

    def test_is_bot(self):
        """Assert is_bot attr"""

        self.assertTrue( TestGetMe.bot_info['is_bot'] )

    def test_username(self):
        """Assert username attr"""

        self.assertEqual( TestGetMe.bot_info['username'], TELEGRAM['username'] )

class TestBotUpdates(unittest.TestCase):
    """TestBotUpdates unit test"""

    def _fetch_updates(self, bot):
        chat = Chat(
            id=626525644,
            type='private',
            first_name='Wallace',
            last_name='Reis'
        )
        user = User(
            id=626525644,
            first_name='Wallace',
            last_name='Reis',
            is_bot=False,
            language_code='pt-br'
        )
        return [
            Update(
                update_id=704571537,
                message=Message(
                    message_id=22,
                    date=None,
                    chat=chat,
                    text='/hello',
                    delete_chat_photo=False,
                    group_chat_created=False,
                    supergroup_chat_created=False,
                    channel_chat_created=False,
                    from_user=user,
                    bot=bot,
                )
            ),
            Update(
                update_id=704571545,
                message=Message(
                    message_id=7,
                    date=None,
                    chat=chat,
                    new_chat_members=[user],
                    from_user=user,
                    bot=bot,
                ),
            ),
        ]

    def test_unknown(self):
        """Assert unknown handler"""

        updater = TghCaptchaBot(TELEGRAM['token'])
        bot = updater.bot

        # mock the start_polling()
        bot.get_updates = MagicMock(return_value=self._fetch_updates(bot))
        update_event = bot.get_updates().pop(0)
        bot.get_updates.assert_called()

        # mock the reply sending
        update_event.message.reply_text = MagicMock(return_value='Replied')
        updater.unknown(bot, update_event)
        update_event.message.reply_text.assert_called()

        # assertions

    def test_restrict(self):
        """Assert (un)restrict handlers"""

        updater = TghCaptchaBot(TELEGRAM['token'])
        bot = updater.bot

        # mock the start_polling()
        bot.get_updates = MagicMock(return_value=self._fetch_updates(bot))
        update_event = bot.get_updates().pop(1)
        bot.get_updates.assert_called()

        # mock the add_restrict
        bot.restrict_chat_member = MagicMock(return_value=None)
        bot.send_message = MagicMock(return_value=None)
        updater.thb_add_restrict(bot, update_event)
        bot.restrict_chat_member.assert_called()
        bot.send_message.assert_called()

        # mock the remove_restrict
        updater.thb_remove_restrict(
            update_event.message.chat.id,
            update_event.message.from_user.id,
            update_event.message.from_user.name,
        )
        bot.restrict_chat_member.assert_called()
        bot.send_message.assert_called()

if __name__ == '__main__':
    unittest.main()
