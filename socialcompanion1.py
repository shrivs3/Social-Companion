# -*- coding: utf-8 -*-
"""
Created on Wed Nov 01 08:37:20 2017

@author: Shrey
"""

import os
import time
from watson_developer_cloud import ConversationV1
from slackclient import SlackClient

conversation = ConversationV1(
  username = 'db44c2aa-7d0d-430c-98c6-27dd9a213e1b',
  password = 'sRxo6q45Kx7s',
  version = '2017-05-26'
)

BOT_ID = 'U7T58DENR'
SLACK_BOT_TOKEN='xoxb-265178456773-Y5j4wH0tIfqw2jXSsMlKBwax'


AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)



def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    # response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
    #            "* command with numbers, delimited by spaces."


    print ('User says: '+command)
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    print(response["text"])
    slack_client.api_call("chat.postMessage", channel=channel,
                          text= response["text"], as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")