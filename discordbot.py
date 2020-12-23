# インストールした discord.py を読み込む
import discord
from discord.ext import commands
import asyncio

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzkwMzAxNDEwNDc3NzM1OTQ3.X9-niw.fcGeby6_iZH9SQUJEc1PZToLEzo'

# 接続に必要なオブジェクトを生成
client = discord.Client()
client = commands.Bot(command_prefix=".")

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログイン完了！ロックだね！')
    await client.change_presence(activity=discord.Game(name="えりはと新婚生活", type=1))

@client.command()
async def rect(ctx, about = "募集", cnt = 4, settime = 10.0):
    cnt, settime = int(cnt), float(settime)
    reaction_member = [">>>"]
    test = discord.Embed(title=about,colour=0x1e90ff)
    test.add_field(name=f"あと{cnt}人 募集中だよ！\n", value=None, inline=True)
    msg = await ctx.send(embed=test)
    #投票の欄
    await msg.add_reaction('⏫')
    await msg.add_reaction('✖')

    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == '⏫' or emoji == '✖'

    while len(reaction_member)-1 <= cnt:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=settime, check=check)
        except asyncio.TimeoutError:
            await ctx.send('人数足りないっぽいよ...')
            break
        else:
            print(str(reaction.emoji))
            if str(reaction.emoji) == '⏫':
                reaction_member.append(user.name)
                cnt -= 1
                test = discord.Embed(title=about,colour=0x1e90ff)
                test.add_field(name=f"あと__{cnt}__人 募集中だよ！\n", value='\n'.join(reaction_member), inline=True)
                await msg.edit(embed=test)

                if cnt == 0:
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中だよ！\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                    finish = discord.Embed(title=about,colour=0x1e90ff)
                    finish.add_field(name="メンバーが決まったよ！プロデューサー。",value='\n'.join(reaction_member), inline=True)
                    await ctx.send(embed=finish)

            elif str(reaction.emoji) == '✖':
                if user.name in reaction_member:
                    reaction_member.remove(user.name)
                    cnt += 1
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中だよ！\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                else:
                    pass
        # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
        await msg.remove_reaction(str(reaction.emoji), user)

client.run(TOKEN)

