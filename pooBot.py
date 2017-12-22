#pooBot
#By DracoRanger
import asyncio
import re
from datetime import date
from datetime import datetime
import math
import statistics
import random
import discord
from discord.ext import commands

#import logging

client = discord.Client()
bot = commands.Bot(command_prefix="!", description="")
config = open('config.txt','r')
conf = config.readlines() #push to array or do directly
token = conf[0][:-1]
channelNum = conf[1][:-1]

'''
Calculate probability
"2016-03-24T23:15:59.605000+00:00"

def generateEstimate():
    #Previous poos = list of "timestamp": "2016-03-24T23:15:59.605000+00:00"
    global channelNum
    timeDifference = []
    last = 0

    #messages = yield from client.logs_from(channelNum, limit=500)
    async for messages in client.logs_from(channelNum, limit=500):
    #print("hit")
    #messages = yield from client.logs_from(client.get_channel(channelNum), limit=500)
    print(messages)
    for message in messages:
        print(message)
        #message = messages.next()
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
    lowerBound = median - (upperBound - median)#need to change to specific dates
    print('why this fail?')
    ret = "Aaron uses the bathroom every "+ str(median) +"units with a standard deviation of "+ str(stdev)+"\nThe upper bound for the next one is " +str(upperBound)+", the lower bound is "+ str(lowerBound)+". \nI predict "+str(random.randrange(lowerBound,upperBound,1))+'.'
    print(ret)
    return ret
'''

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print(client.user.id)
    print('------')
    message = client.user.name + " is up and running!"
    await client.send_message(client.get_channel(channelNum), message)

@client.event
@asyncio.coroutine
async def on_message(message):
    global channelNum
    if message.author == client.user:
        return
    if message.channel == client.get_channel(channelNum) and not message.author == client.user:
        '''
        Post result
        '''
        #Previous poos = list of "timestamp": "2016-03-24T23:15:59.605000+00:00"
        timeDifference = []
        last = 0
        async for message in client.logs_from(client.get_channel(channelNum), limit=500):
            if not message.author == client.user:
                if last == 0:
                    last = (message.timestamp - datetime.utcfromtimestamp(0)).total_seconds()
                else:
                    timeDif = (message.timestamp - datetime.utcfromtimestamp(0)).total_seconds() - last#convert time string into time num
                    if(math.fabs(timeDif)<300000):
                        timeDifference.append(math.fabs(timeDif))
                    last = (message.timestamp - datetime.utcfromtimestamp(0)).total_seconds()
        timeDifference = sorted(timeDifference)
        median = int(timeDifference[math.floor(len(timeDifference)/2)])
        stdev = int(statistics.stdev(timeDifference))
        upperBound = int((median + 2*stdev) + (datetime.now() - datetime.utcfromtimestamp(0)).total_seconds())
        lowerBound = int((median - 2*stdev) + (datetime.now() - datetime.utcfromtimestamp(0)).total_seconds())#need to change to specific dates
        if lowerBound < (datetime.now() - datetime.utcfromtimestamp(0)).total_seconds():
            lowerBound = int((datetime.now() - datetime.utcfromtimestamp(0)).total_seconds())
        dateUB = datetime.fromtimestamp(upperBound)
        dateLB = datetime.fromtimestamp(lowerBound)
        dateGuess = datetime.fromtimestamp(random.randrange(lowerBound,upperBound,1))
        ret = "Aaron uses the bathroom every "+ str(median) +" seconds with a standard deviation of "+ str(stdev)+ " seconds.\nThe upper bound for the next one is " +str(dateUB)+", the lower bound is "+ str(dateLB)+". \nI predict "+str(dateGuess)+'.'

        #temp = generateEstimate()
        await client.send_message(message.channel, ret)
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
