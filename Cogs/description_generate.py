# Discord bot import
import os
import glob
import ndjson
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# my program import


class description_generate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # /description
    @app_commands.command(name="description",description="ロールのユーザーの情報を概要欄形式で出力します。 / Outputs description format in role users.")
    #@discord.app_commands.guilds(int(os.environ.get('Test_server')))
    @app_commands.guild_only()
    @app_commands.describe(title="敬称（例：さん、様など...） / honorific title (example:Mr., Ms. etc...)")
    @app_commands.describe(display_x="X（Twitter）の表記をON/OFFどちらにするか / X (Twitter) notation ON or OFF")
    @app_commands.choices(display_x=[discord.app_commands.Choice(name="ON",value="on"), discord.app_commands.Choice(name="OFF", value="off")])
    async def description_command(self, interaction: discord.Interaction, role:discord.Role, display_x:str, title:str=None):

        await interaction.response.defer()

        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./data/language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        # サーバーのデータが存在しているかを確認
        files = glob.glob('./data/guild_data/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                #print("一致しました！")
                judge = 1
                break
        
        if judge != 1:
                if language == "ja":
                    embed=discord.Embed(title="エラー！", description=":x:このサーバーのデータが存在していません。:x:", color=0xff0000)
                else:
                    embed=discord.Embed(title="Error!", description=":x:Data for this server does not exist.:x:", color=0xff0000)

                await interaction.followup.send(embed=embed)
                return
        
        # ロールのついているユーザーから、文章を結合していく
        with open('./data/guild_data/' + str(interaction.guild.id) + ".ndjson") as f:
            read_data = ndjson.load(f)

        text = ''
        if title == None:
            if language == "ja":
                text += "※敬称略\n\n"
            
            title = ""
        else:
            if language == "ja":
                title = " " + title
            else:
                title = title + " "

        cut = 10
        count = 0
        followup_send = 0
        for i in range(0, len(read_data)):
            for j in range(0, len(role.members)):
                # Botは無視する
                if role.members[j].bot:
                    continue

                if int(read_data[i]["member"]) == role.members[j].id:
                    #print(role.members[j].id)

                    stream_url = read_data[i]["stream_site_url"]
                    stream_url = stream_url[:5] + "\\" + stream_url[5:]

                    if language == "ja":
                        text += read_data[i]["name"] + title + "\n配信サイト：" + stream_url + "\n"

                        if display_x == "on":
                            text += "X（Twitter）：https\://x.com/" + read_data[i]["x_name"] + "\n" 
                    else:
                        text += title + read_data[i]["name"] + "\nStream Site:" + stream_url + "\n"

                        if display_x == "on":
                            text += "\nX(Twitter):https\://x.com/" + read_data[i]["x_name"] + "\n"

                    text += "\n"

                    count += 1

                    if count == cut:
                        cut = cut + 10

                        #表示させる
                        if followup_send == 0:
                            await interaction.followup.send(text)
                        else:
                            #print(str(interaction.channel_id))
                            channel_sent = interaction.client.get_channel(interaction.channel_id)
                            await channel_sent.send(text)

                        text = "\u200b\n"
                        followup_send += 1

                        await asyncio.sleep(1)

            if i == len(read_data) - 1:
                #表示させる
                if followup_send == 0:
                    await interaction.followup.send(text)
                else:
                    #print(str(interaction.channel_id))
                    channel_sent = interaction.client.get_channel(interaction.channel_id)
                    await channel_sent.send(text)
                
                return

    # /hashtag
    @app_commands.command(name="hashtag",description="ロールのユーザのX（Twitter）IDをハッシュタグ形式で出力します。 / Outputs X(Twitter)IDs hashtag format in role users.")
    #@discord.app_commands.guilds(int(os.environ.get('Test_server')))
    @app_commands.guild_only()
    async def hashtag_command(self, interaction: discord.Interaction, role:discord.Role):

        await interaction.response.defer()

        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./data/language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        # サーバーのデータが存在しているかを確認
        files = glob.glob('./data/guild_data/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                #print("一致しました！")
                judge = 1
                break
        
        if judge != 1:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:このサーバーのデータが存在していません。\n/information addコマンドでユーザーの情報を登録してください！:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:Data for this server does not exist.\nRegister user information with the /information add command!:x:", color=0xff0000)

            await interaction.followup.send(embed=embed)
            return
        
        # ロールのついているユーザーから、文章を結合していく
        with open('./data/guild_data/' + str(interaction.guild.id) + ".ndjson") as f:
            read_data = ndjson.load(f)

        text = ''
        if language == "ja":
            text += "参加者一覧（敬称略）\n\n"
        else:
            text += "List of Participants\n\n"

        cut = 10
        count = 0
        followup_send = 0
        for i in range(0, len(read_data)):
            for j in range(0, len(role.members)):
                # Botは無視する
                if role.members[j].bot:
                    continue
                
                if int(read_data[i]["member"]) == role.members[j].id:
                    #print(role.members[i].id)
                    text += read_data[i]["name"] + " #" + read_data[i]["x_name"] + "\n"

                    count += 1

                    if count == cut:
                        cut = cut + 10

                        #表示させる
                        if followup_send == 0:
                            await interaction.followup.send(text)
                        else:
                            #print(str(interaction.channel_id))
                            channel_sent = interaction.client.get_channel(interaction.channel_id)
                            await channel_sent.send(text)

                        text = ""
                        followup_send += 1

                        await asyncio.sleep(1)

            if i == len(read_data) - 1:
                #表示させる
                if followup_send == 0:
                    await interaction.followup.send(text)
                else:
                    #print(str(interaction.channel_id))
                    channel_sent = interaction.client.get_channel(interaction.channel_id)
                    await channel_sent.send(text)
                
                return

    # /template
    @app_commands.command(name="template",description="アプリ「Output description」の概要欄形式の指定を行います。/ Set description format of the [Output description] apps.")
    #@discord.app_commands.guilds(int(os.environ.get('Test_server')))
    @app_commands.guild_only()
    @app_commands.describe(title="敬称（例：さん、様など...） / honorific title (example:Mr., Ms. etc...)")
    @app_commands.describe(display_x="X（Twitter）の表記をON/OFFどちらにするか / X (Twitter) notation ON or OFF")
    @app_commands.choices(display_x=[discord.app_commands.Choice(name="ON",value="on"), discord.app_commands.Choice(name="OFF", value="off")])
    async def template_command(self, interaction: discord.Interaction, role:discord.Role, display_x:str, title:str=None):

        await interaction.response.defer()

        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./data/language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        # サーバーのデータが存在しているかを確認
        files = glob.glob('./data/guild_config/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                #print("一致しました！")
                judge = 1
                break

        # 入力された内容をndjsonに書き込んでいく        
        if judge == 1:
            os.remove('./data/guild_config/' + str(interaction.guild.id) + ".ndjson")
        
        if title == None:
            title = "no"

        content = {
            "role" : str(role.id),
            "title" : title,
            "display_x" : display_x
        }

        with open('./data/guild_config/' + str(interaction.guild.id) +".ndjson", 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(content)
        
        #Discord上に表示
        if judge == 1:
            if language == "ja":
                embed=discord.Embed(title="登録しました!", description="\n\n入力された情報を登録しました。\nここで指定したテンプレートを使用する場合はBotのアプリ「Output description」から利用してみてください！", color=0x00ff7f) 
            else:
                embed=discord.Embed(title="Registered!", description="\n\nThe entered information has been registered. \nTo use the template specified here, try using it from Bot's application [Output description]!", color=0x00ff7f)      
        else:
            if language == "ja":    
                embed=discord.Embed(title="更新しました!", description="\n\n入力された情報を更新しました。\nここで指定したテンプレートを使用する場合はBotのアプリ「Output description」から利用してみてください！", color=0x00ff7f) 
            else:
                embed=discord.Embed(title="Updated!", description="\n\nThe entered information has been updated. \nTo use the template specified here, try using it from Bot's application [Output description]!", color=0x00ff7f)  


        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(description_generate(bot))