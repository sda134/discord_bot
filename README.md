# discord_bot

discord からのメッセージで，Raspberry Pi から赤外線リモコンの信号を送信します。（開発途中）<br>
discord の bot 作成：https://discordapp.com/developers/applications/<br>
discord.py: https://discordpy.readthedocs.io/en/latest/intro.html<br>


irrp.py は aptでインストール＋systemctl のenable(start)が必要<br>
<code>sudo apt install pigpio python3-pigpio</code><br>
#venv を使うときは，当然だが仮想環境にインストールする<br>
irrp.py: http://abyz.me.uk/rpi/pigpio/examples.html#Python_irrp_py<br>
