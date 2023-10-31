# Discord bot import
import os
import glob
import ndjson
import asyncio
import discord

# My program import


class list_program:
    async def list_interaction(self, interaction):
        
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

        # サーバーのデータを表示させる処理
        with open('./data/guild_data/' + str(interaction.guild.id) + ".ndjson") as f:
            read_data = ndjson.load(f)

        if language == "ja":
            embed=discord.Embed(title="登録されているユーザー", color=0x00ff7f)
        else:
            embed=discord.Embed(title="Registered Users", color=0x00ff7f)


        cut = 10
        count = 0
        followup_send = 0
        for j in range(0, len(read_data)):

            if language == "ja":
                embed.add_field(name=str(j+1) + "." + read_data[j]["name"], 
                                value="\n関連Discordユーザー：<@" + read_data[j]["member"] + ">\n配信サイトURL：" + 
                                read_data[j]["stream_site_url"] + "\n X（旧Twitter）URL：" + "https://x.com/" + read_data[j]["x_name"], inline=False)
            else:
                embed.add_field(name=str(j+1) + "." + read_data[j]["name"],
                                value="\nRelated Discord users:<@" + read_data[j]["member"] + ">\nStream site URL:" + 
                                read_data[j]["stream_site_url"] + "\nX(Twitter) URL:" + "https://x.com/" + read_data[j]["x_name"], inline=False)

            count += 1
            
            if j == len(read_data) - 1:
                #表示させる
                if followup_send == 0:
                    await interaction.followup.send(embed=embed)
                else:
                    #print(str(interaction.channel_id))
                    channel_sent = interaction.client.get_channel(interaction.channel_id)
                    await channel_sent.send(embed=embed)
                
                return
            
            if count + 1 == cut:
                cut = cut + 25

                #表示させる
                if followup_send == 0:
                    await interaction.followup.send(embed=embed)
                else:
                    #print(str(interaction.channel_id))
                    channel_sent = interaction.client.get_channel(interaction.channel_id)
                    await channel_sent.send(embed=embed)
                
                embed=discord.Embed(title="", color=0x00ff7f)
                
                followup_send += 1

                # DiscordのWebhook送信制限に引っかからないための対策　※効果があるかは不明
                await asyncio.sleep(2)