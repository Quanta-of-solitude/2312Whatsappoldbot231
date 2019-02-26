
'''
Whatsapp bot made just for fun... using Twilio
'''
import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
import urllib
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

__author__ = "Nyzex"


@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    resp = MessagingResponse()
    query = urllib.parse.quote(request.form["Body"])
    text = query.replace(' ', '+')

    if query.startswith("%21"):
        keyword = query[3:]
        keyword = keyword.lower()
        if keyword == "help":
            val = help_menu()
        elif keyword.startswith("repeat"):
            val = text[len("repeat")+3:]
            val = urllib.parse.unquote(val)
        else:
            val = "Invalid '!' command, use !help for info! "

        resp.message(val)

    else:
        try:
            r = requests.get("{}".format(os.environ.get("libbot"))+"&message={}&application={}&offensive=false".format(text, os.environ.get("appid")))
            soup = BeautifulSoup(r.content, 'lxml')
            f_data = soup.find("message")
            resp.message("{}".format(f_data.text))
        except Exception as e:
            resp.message("I wont reply to this!")
            print(e)

    return str(resp)



def help_menu():
    '''Help Menu'''
    help = """*The Help menu for the bot is:*
```
1. !commands: Get this help menu.
2. !repeat [str]: return what you said.

For Eg: !repeat hey
It will reply: hey


You can talk to the bot like a person without using '!' prefix.
Just text 'hi' to the bot!
```


*Twilio Number - Free Version XD*

*More commands coming soon! I have an idea, and I might make it available soon!*

*Made by  Nyzex*""")
    return help


if __name__ == "__main__":
    app.run()
