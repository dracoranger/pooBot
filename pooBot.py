#pooBot
#By DracoRanger
import asyncio
import re
from datetime import datetime
from datetime import timedelta
import math
import statistics
import random
import discord
from discord.ext import commands

#import logging

client = discord.Client()
bot = commands.Bot(command_prefix="!", description="")

BOT_FOLDER=""

config = open('config.txt','r')
conf = config.readlines() #push to array or do directly
token = conf[0][:-1]
channelNum = conf[1][:-1]
userComp = conf[2][:-1]

'''
Calculate probability
"2016-03-24T23:15:59.605000+00:00"
'''
def generateEstimate():
    #Previous poos = list of "timestamp": "2016-03-24T23:15:59.605000+00:00"
    global channelNum
    timeDifference = []
    last = 0
    for message in client.logs_from(channelNum, limit=500):
        if not message.author == client.user:
            if last == 0:
                last = message.timestamp
            else:
                timeDif = message.timestamp - last#convert time string into time num
                timeDifference.append(timeDif)
    timeDifference = sorted(timeDifference)
    median = timeDifference[math.floor(len(timeDifference)/2)]
    stdev = statistics.stdev(timeDifference)
    upperBound = median * stdev
    lowerBound = median - (upperBound - median)
    ret = "Aaron uses the bathroom every "+ str(median) +"units with a standard deviation of "+ str(stdev)+"\nThe upper bound for the next one is " +str(upperBound)+", the lower bound is "+ str(lowerBound)+". \nI predict "+str(random.randrange(lowerBound,upperBound,1))+'.'
    return ret

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print(client.user.id)
    print('------')
    message = client.user.name + " is up and running!"
    await client.send_message(client.get_channel(channelNum), message)

@client.event
async def on_message(message):
    global channelNum
    if message.author == client.user:
        return
    if message.channel == client.get_channel(channelNum) and not message.author == client.user:
        '''
        Post result
        '''
        temp = generateEstimate()
        await client.send_message(message.channel, temp)
    '''
        {
    "id": "162701077035089920",
    "channel_id": "131391742183342080",
    "author": {},
    "content": "Hey guys!",
    "timestamp": "2016-03-24T23:15:59.605000+00:00",
    "edited_timestamp": null,
    "tts": false,
    "mention_everyone": false,
    "mentions": [],
    "mention_roles": [],
    "attachments": [],
    "embeds": [],
    "reactions": []
}
    '''

client.run(token)
