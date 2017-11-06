# -*- coding: utf-8 -*-
"""
Created on Wed Nov 01 08:20:20 2017

@author: Shrey
"""

import os
from slackclient import SlackClient


BOT_NAME = 'socialcompanion'
SLACK_BOT_TOKEN='xoxb-265178456773-Y5j4wH0tIfqw2jXSsMlKBwax'

slack_client = SlackClient(SLACK_BOT_TOKEN)


if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    print 1
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)