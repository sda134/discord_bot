#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import discord
import msgcheck
from bme280 import Bme280, Bme280Mode

TOKEN = 'ODAwMjI0NDUyODkzNjA1OTM5.YAPBGQ.pJCquT3VAGpEMsIHTlTHtOMWBjs'   # botのアクセストークン
client = discord.Client()               # discord のインスタンス

def get_bme_data():
    #Bme280 setup
    bme = Bme280()
    bme.mode = Bme280Mode.NORMAL
    bme.open()
    return bme.get_data()

@client.event                           # 起動イベント
async def on_ready():
    print('Login')

@client.event                           # メッセージ受信イベント
async def on_message(message):    
    if message.author == client.user:   # 送信者がBotだった場合は無視
        return
    
    # メッセージ確認（不要ならコメントアウトしても良い）
    print('Message from {0.author}: {0.content}'.format(message))

    # 送信メッセージの認識
    target, verb = msgcheck.checkup_msg(message.content)

    # メッセージごとに処理を行う
    if target == 'エアコン':
        if verb == 'つける':
            subprocess.call(['python3', 'irrp.py', '-p', '-g17', '-f', 'codes', "aircon:on"])
            await message.channel.send('エアコンを点けました。')
        elif verb == 'けす':
            subprocess.call(['python3', 'irrp.py', '-p', '-g17', '-f', 'codes', "aircon:off"])
            await message.channel.send('エアコンを消しました。')
        else:
            await message.channel.send('理解できません。')
    elif target == '照明':
        if verb == 'つける':
            subprocess.call(['python3', 'irrp.py', '-p', '-g17', '-f', 'codes', "light:on"])
            await message.channel.send('照明を点けました。')
        elif verb == 'けす':
            subprocess.call(['python3', 'irrp.py', '-p', '-g17', '-f', 'codes', "light:off"])
            await message.channel.send('照明を消しました。')
        else:
            await message.channel.send('理解できません。')
    else:

        # シンプルに単語認証する場合
        if message.content == '環境':
            press,temp,humid = get_bme_data()
            await message.channel.send('温度 %.2f℃　湿度 %.0f%%　気圧 %.0fhPa' % (temp, humid, press))
        elif message.content == '温度' or message.content == 'おんど':
            press,temp,humid = get_bme_data()
            await message.channel.send('現在温度  %.2f℃' % (temp))
        elif message.content == '湿度' or message.content == 'しつど':
            press,temp,humid = get_bme_data()
            await message.channel.send('現在湿度 %.0f%%' % (humid))
        elif message.content == '気圧' or message.content == 'きあつ':
            press,temp,humid = get_bme_data()
            await message.channel.send('現在気圧 %.0fhPa' % (press))
        else:
            await message.channel.send('理解できません。')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)