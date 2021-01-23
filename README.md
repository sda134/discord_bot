# discord_bot

discord からのメッセージで，Raspberry Pi から赤外線リモコンの信号を送信します。（開発途中）

discord の bot 作成：https://discordapp.com/developers/applications/

discord.py: https://discordpy.readthedocs.io/en/latest/intro.html


irrp.py は aptでインストール＋systemctl のenable(start)が必要
<code>sudo apt install pigpio python3-pigpio</code>
irrp.py: http://abyz.me.uk/rpi/pigpio/examples.html#Python_irrp_py
