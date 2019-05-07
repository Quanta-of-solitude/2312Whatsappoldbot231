
'''
Whatsapp bot made just for fun... using Twilio
'''
import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
import urllib
import mqttPush #for nodeMCU
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

     #main commands
    if query.startswith("%21"):
        keyword = query[3:]
        keyword = keyword.lower()
        if keyword == "help":
            val = help_menu()

        elif keyword.startswith("repeat"):
            val = text[len("repeat")+3:]
            val = urllib.parse.unquote(val)

        elif keyword == "joke":
            jk = requests.get("{}".format(os.environ.get("jokesite")))
            soup = BeautifulSoup(jk.content,'lxml')
            val = soup.find("p", {"class": "subtitle"}).get_text()

       #Interact with NODE MCU

        elif keyword.startswith("node"):
            try:
                dataSent = text[len("node")+3:]
                dataSent = urllib.parse.unquote(val)
                data_sender = mqttPush.FruitSent("USERNAME","AIOKEY","FEEDNAME")
                if dataSent == "1":
                    try:
                        data_sender.data_sent(1)
                        val = "Toggle Switch on!"
                    except Exception as e:
                        print(e)
                        val = "```Error API CONTACT```"
                elif dataSent == "0":
                    try:
                        data_sender.data_sent(0)
                        val = "Toggle Switch off!"
                    except Exception as e:
                        print(e)
                        val = "```Error API CONTACT```"

                else:
                    val = "Invalid param, 0 or 1"
            except Exception as e:
                print(e)
                val = "```Contact dev for details```"

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
2. !joke: Get a Random JOKE!
3. !repeat [str]: return what you said.

For Eg: !repeat hey
It will reply: hey

4. !node [0 or 1]: turn led on or off on node MCU/

    to work: add AIOKEY USERNAME and FEEDNAME, also upload code to nodeMCU having the same feeds.
    Currently works only on toggle buttons.

You can talk to the bot like a person without using '!' prefix.
Just text 'hi' to the bot!
```


*Twilio Number - Free Version XD*

*More commands coming soon! I have an idea, and I might make it available soon!*

*Made by  Nyzex*"""
    return help


if __name__ == "__main__":
    app.run()
