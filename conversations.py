# -*- coding: utf-8 -*-
"""
Created on Wed Nov 01 10:34:55 2017

@author: Shrey
"""

import os
import time
from watson_developer_cloud import ConversationV1


conversation = ConversationV1(
  username = 'db44c2aa-7d0d-430c-98c6-27dd9a213e1b',
  password = 'sRxo6q45Kx7s',
  version = '2017-05-26'
)


def get_response(command):
    response = conversation.message(
        workspace_id='09ff211f-5120-428a-ba2e-c51d3b84ba7a',
        message_input={
            'text': command
        }
    )
    
    if (response['entities']==[]):
        return (response['output']['text'][0],[])
    else:
        return (str(response['output']['text'][0]),[str(response['entities'][i]['value']) for i in range(len(response['entities']))])