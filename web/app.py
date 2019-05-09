"""Web app for hCaptcha verification

Simple webapp to challenge the user with captcha and remove its restriction
in telegram chats through the bot class.
"""

from flask import Flask, render_template, request
import urllib.request
import urllib.parse
import json
from tg_hCaptcha_bot.settings import TELEGRAM, HCAPTCHA
from tg_hCaptcha_bot import TghCaptchaBot

app = Flask(__name__)

@app.route('/<chat_id>/<member_id>/<member_name>')
def show(chat_id=None, member_id=None, member_name=None):
    """Present webpage with the hCaptcha widget"""

    return render_template(
        'show.html',
        chat_id=chat_id, member_id=member_id, member_name=member_name
    )

@app.route('/<chat_id>/<member_id>/<member_name>/verify', methods=['POST'])
def verify(chat_id=None, member_id=None, member_name=None):
    """Verify the captcha"""

    error = None
    token = request.form['h-captcha-response']
    params = urllib.parse.urlencode({
        'secret': HCAPTCHA['secret'],
        'response': token
    })
    with urllib.request.urlopen(HCAPTCHA['post_uri'], params.encode('ascii')) as f:
        json_res = json.loads( f.read().decode('utf-8') )
        if json_res['success']:
            bot = TghCaptchaBot(TELEGRAM['token'])
            bot.thb_remove_restrict(chat_id, member_id, member_name)
            return 'Success'
        else:
            return 'Error'
