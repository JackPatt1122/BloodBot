from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import json
import csv
from datetime import datetime
import numpy
import pandas as pd

tokens = {}
with open('configs.json') as json_data:
    tokens = json.load(json_data)

slack_events_adapter = SlackEventAdapter(tokens.get("slack_signing_secret"), "/slack/events")
slack_client = SlackClient(tokens.get("slack_bot_token"))


@slack_events_adapter.on("message")
def handle_message(event_data):
    today = datetime.now()
    dt_string = today.strftime("%d/%m/%Y %H:%M:%S")
    message = event_data["event"]
    if message.get("subtype") is None and "blood" in message.get('text'):
        input_file = open("total.csv","r+")
        reader_file = csv.reader(input_file)
        value = int(len(list(reader_file)))
        input_file.write('\n' + str(value+1))
        channel = message["channel"]
        messagestr = "Bartch's Nose bled "
        send_message =  "%s%s%s" % (messagestr, value+1, ' times since December 4th')
        slack_client.api_call("chat.postMessage", channel=channel, text=send_message)
    elif message.get("subtype") is None and "blall" in message.get('text'):
        input_file1 = open("total.csv","r+")
        reader_file1 = csv.reader(input_file1)
        value1 = int(len(list(reader_file1)))
        messagestr1 = "Bartch's Nose bled "
        channel = message["channel"]
        send_message =  "%s%s%s" % (messagestr1, value1, ' times since December 4th')
        slack_client.api_call("chat.postMessage", channel=channel, text=send_message)
    


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


slack_events_adapter.start(port=3000)