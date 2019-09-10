#!/usr/bin/python3
# coding: utf-8
import discord
import tasukaru
import time

client = discord.Client()

retry_count = 3
ecosystem = tasukaru.tasukaru()

@client.event
async def on_ready():
    print('Botを起動しました。')

@client.event
async def on_message(message):
    msg = message.content
    if msg.startswith('https://twitter.com'):
        for i in range(retry_count):
            try:
                r = ecosystem._tasukaru(str(message.content),str(message.author))
                if r == 0:
                    await message.channel.send("助かる") # rewrite版
                else:
                    await message.channel.send("助かるな") # rewrite版
                break
            except Exception as x:
                await message.channel.send("Error!\n{}".format(x)) # rewrite版
                if i+1 != retry_count:
                    await message.channel.send(f"[{i+1}/{retry_count}] 終わった　10秒後にリトライするよ")
                    time.sleep(10)
                else:
                    await message.channel.send(f"[{i+1}/{retry_count}] tasukaru is failed.\n悲しい")
    
    if msg == '出す' or msg == "dasu":
        try:
            send_message = ecosystem._dasu()
            await message.channel.send(send_message)

        except Exception as x:
            await message.channel.send("Error!\n{}".format(x))

#ここにbotのアクセストークンを入力
client.run('***')

