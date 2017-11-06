# -*- coding: utf-8 -*-
"""
Created on Wed Nov 01 08:37:20 2017

@author: Shrey
"""

import os
import time
from slackclient import SlackClient
import discoverynews
import conversations
import unicodedata
import operator



BOT_ID = 'U7T58DENR'
SLACK_BOT_TOKEN='xoxb-265178456773-Y5j4wH0tIfqw2jXSsMlKBwax'


AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
DISCOVERY_COMMAND = "discover"
# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)

def print_response(response, channel):

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=str(response), as_user=True)
    print ('Bot says: '+response)
    

def handle_command(command, channel):

    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    print ('User says: '+command)
    
    #Getting entities in the message 
    response, entity = conversations.get_response(command)
   
    if ('sentiment' in command) or ('feel about' in command):
        command1=command.split(' ')
        response='The sentiments for this topic are:\n'
        a=discoverynews.get_sentiments(command1[-1], 50)
        for i in a.keys():
            b=str(i)+' : '+str(float(a[i])/float(50))
            response=response+b+'\n'
            
    if command.startswith(DISCOVERY_COMMAND):
        a= discoverynews.top_articles(command)
        articles=''
        for i in range(len(a.keys())):
            articles=articles+str(i+1)+'. '+a.keys()[i]+'\n Link: '+a[a.keys()[i]]+'\n \n'
        response = 'The top articles I found right now are: \n'+articles
        response = unicodedata.normalize('NFKD', response).encode('ascii','ignore')

    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # When nothing is specified. General statements.
    if (entity==[]):
        print_response(response, channel)
    
    # When some entity is entered. 
    if (entity!=[]):
        if ('hashtag' in entity):
            command1=command.split(' ')
            response=('You can use the following hashtags: '+str(command1[-1])+'\n \n')
            a= discoverynews.get_hashtags(str(command1[-1]))
            a1= sorted(a.items(), key=operator.itemgetter(1))
            for i in range(5):
                response=response+a1[-i][0]+'\n'
            response = unicodedata.normalize('NFKD', response).encode('ascii','ignore')
                
        if ('news' in entity) and ('hashtag' not in entity):
            print entity
            if (len(entity)==2):
                e=entity[0]
                if e=='news':
                    e=entity[1]
                a= discoverynews.top_articles(str(e))
            else:
                command1=command.split(' ')
                a= discoverynews.top_articles(str(command1[-1]))
            articles=''
            for i in range(len(a.keys())):
                articles=articles+str(i+1)+'. '+a.keys()[i]+'\n Link: '+a[a.keys()[i]]+'\n \n'
            response = 'The top articles I found right now are: \n'+articles
            response = unicodedata.normalize('NFKD', response).encode('ascii','ignore')
        
        print_response(response, channel)



def parse_slack_output(slack_rtm_output):

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
        print("SocialCompanion connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")