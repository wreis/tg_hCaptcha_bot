"""Main module to run the bot as a script"""

from tg_hCaptcha_bot.settings import TELEGRAM
from tg_hCaptcha_bot import TghCaptchaBot

if __name__ == '__main__':
    bot = TghCaptchaBot(TELEGRAM['token'])
    bot.run()
