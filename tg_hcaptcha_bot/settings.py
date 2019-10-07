"""
General Settings for Telegram hCaptcha Bot

This provides general settings bits for the bot modules.
"""

from logging import INFO as LOG_LEVEL

TELEGRAM = {
    'token': 'foobarbugs',
    'id': 0000000000,
    'username': 'bot',
}

HCAPTCHA = {
    'secret': 'foobarbogus',
    'post_uri': 'https://hcaptcha.com/siteverify',
}

LOG = {
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'level': LOG_LEVEL,
}

RESTRICT = {
    'url_text': 'Go to verification page',
    'url': 'http://mysitebogus.com/',
}

BOT_MSGS = {
    'captcha': "<b>Welcome {}! With our Anti-SPAM policy, we kindly inform you that you need to click the following button to prove your human identity.</b>",
    'allowed': "<b>Thanks {}! You are now allowed to chat.</b>",
    'unknown': "Sorry, I don't know this command.",
}
