import discord
import msgcheck                         # msgcheck.py 簡単な言語認識を行う

# -- 事前に irrp.py を手に入れ，赤外線信号のデータを./codes に保存しておく --

TOKEN = 'yourtoken'                     # botのアクセストークン
client = discord.Client()               # discord のインスタンス


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
            subprocess.call(['python3', 'irrp.py', '-p', '-g17', '-f', 'codes', 'aircon:on'])
            await message.channel.send('エアコンを点けました。')
        elif verb == 'けす':
            subprocess.call(['python3', 'irrp.py', '-p', '-g17', '-f', 'codes', 'aircon:off'])
            await message.channel.send('エアコンを消しました。')
        else:
            await message.channel.send('理解できません。')
    else:
        # シンプルに単語認証する場合
        if message.content == '環境':
            await message.channel.send('全部表示(ダミー)')
        elif message.content == '温度' or message.content == 'おんど':
            await message.channel.send('現在温度 18℃(ダミー)')
        elif message.content == '湿度' or message.content == 'しつど':
            await message.channel.send('現在湿度 40%(ダミー)')
        elif message.content == '気圧' or message.content == 'きあつ':
            await message.channel.send('現在気圧 1000hPa(ダミー)')
        else:
            await message.channel.send('理解できません')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
