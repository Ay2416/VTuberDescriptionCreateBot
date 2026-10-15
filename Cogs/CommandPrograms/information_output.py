# Discord bot import
import os
import json
import glob
import ndjson
#import asyncio
import discord

# My program import


class output_program:
    async def output_interaction(self, interaction):
        
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

        # サーバーのデータを出力させる処理
        with open('./data/guild_data/' + str(interaction.guild.id) + ".ndjson") as f:
            read_data = ndjson.load(f)

        content = {
            'server_id' : str(interaction.guild.id),
            'server_name' : interaction.guild.name,
            'server_member' : {},
            'server_data' : {}
        }

        # サーバーメンバーデータの保存
        server_member = interaction.guild.members
        count = 0

        for i in range(0, len(server_member)):
            if not server_member[i].bot:
                content['server_member'][count] = {
                    'name' : server_member[i].display_name,
                    'id' : server_member[i].id
                }

                count = count + 1

        # サーバーの登録されている情報を保存
        for j in range(0, len(read_data)):
            content['server_data'][j] = {
                'name' : read_data[j]["name"],
                'member' : read_data[j]["member"],
                'stream_site_url' : read_data[j]["stream_site_url"],
                'x_name' : read_data[j]["x_name"]
            }

        # jsonにして一時ファイルに出力
        with open('./temp_' + str(interaction.guild.id) + '.json', 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        # discordへ送信
        if language == "ja":
            embed=discord.Embed(title="出力に成功しました！", description="Beta", color=0x00ff7f)
        else:
            embed=discord.Embed(title="Output success!", description="Beta", color=0x00ff7f)

        file = discord.File(fp='./temp_' + str(interaction.guild.id) + '.json', filename='dump_data.json', spoiler=False)

        await interaction.followup.send(file=file, embed=embed)
        
        os.remove('./temp_' + str(interaction.guild.id) + '.json')
