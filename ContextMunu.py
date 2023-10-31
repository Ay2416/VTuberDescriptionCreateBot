# discord import
import os
import glob
import ndjson
import asyncio
import discord

# my program import

class ContextMenu:
    async def output_description_program(self, interaction, member):
        print(member.id)

        await interaction.response.defer()

        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./data/language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        # サーバーのデータが存在しているかを確認
        #guild_data
        files = glob.glob('./data/guild_data/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                #print("一致しました！")
                judge = 1
                break

        # 入力された内容をndjsonに書き込んでいく        
        if judge != 1:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:このサーバーのデータが存在していません。\n/information addコマンドでユーザーの情報を登録してください！:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:Data for this server does not exist.\nRegister user information with the /information add command!:x:", color=0xff0000)

            await interaction.followup.send(embed=embed)
            return

        # guild_config
        files = glob.glob('./data/guild_config/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                #print("一致しました！")
                judge = 1
                break

        # 入力された内容をndjsonに書き込んでいく        
        if judge != 1:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:このサーバーのテンプレートデータが存在していません。\n/templateコマンドで登録をしてください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:Data for this server does not exist.\nPlease use the /template command to register.:x:", color=0xff0000)

            await interaction.followup.send(embed=embed)
            return
        
  
        # ロールのついているユーザーから、文章を結合していく
        with open('./data/guild_data/' + str(interaction.guild.id) + ".ndjson") as f:
            read_data1 = ndjson.load(f)

        with open('./data/guild_config/' + str(interaction.guild.id) + ".ndjson") as f:
            read_data2 = ndjson.load(f)

        guild = interaction.guild
        role = guild.get_role(int(read_data2[0]["role"]))
        title = read_data2[0]["title"]
        display_x = read_data2[0]["display_x"]

        text = ''
        if title == "no":
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
        for i in range(0, len(read_data1)):
            for j in range(0, len(role.members)):
                # Botは無視する
                if role.members[j].bot:
                    continue
                
                if int(read_data1[i]["member"]) == role.members[j].id:
                    #print(role.members[i].id)

                    stream_url = read_data1[i]["stream_site_url"]
                    stream_url = stream_url[:5] + "\\" + stream_url[5:]

                    if language == "ja":
                        text += read_data1[i]["name"] + title + "\n配信サイト：" + stream_url + "\n"

                        if display_x == "on":
                            text += "X（Twitter）：https:\//x.com/" + read_data1[i]["x_name"] + "\n" 
                    else:
                        text += title + read_data1[i]["name"] + "\nStream Site:" + stream_url + "\n"

                        if display_x == "on":
                            text += "\nX(Twitter):https:\//x.com/" + read_data1[i]["x_name"] + "\n"

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
                    
            if i == len(read_data1) - 1:
                #表示させる
                if followup_send == 0:
                    await interaction.followup.send(text)
                else:
                    #print(str(interaction.channel_id))
                    channel_sent = interaction.client.get_channel(interaction.channel_id)
                    await channel_sent.send(text)
                
                return