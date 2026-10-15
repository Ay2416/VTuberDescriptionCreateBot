# Discord bot import
import os
import glob
import json
import ndjson
import asyncio
import discord
import requests

# My program import


class input_program:
    async def input_interaction(self, interaction, file):

        await interaction.response.defer()

        # 言語の確認
        file_name = str(interaction.guild.id) + ".ndjson"

        with open('./data/language_json/' + file_name) as f:
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
        
        # ファイルをダウンロード
        # 参考：https://qiita.com/sfj1wara/items/19cae19d8bd36fa97b95
        try:
            r = requests.get(file.url)
            r.encoding = 'utf-8'
            # openの中で保存先のパス（ファイル名を指定）
            with open("./temp_" + str(interaction.guild.id), mode='w', encoding='utf-8') as f:
                f.write(r.text)
        except requests.exceptions.RequestException as err:
            #print(err)
            
            # discordへ結果を送信
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:ファイルの受け渡しでエラーが発生しました。\n申し訳ありませんが、時間を空けてお試しください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:An error occurred in passing the file.\nSorry, please try again in a few hours.:x:", color=0xff0000)

            await interaction.followup.send(embed=embed)
            return

        # 一度サーバーデータのファイルを削除
        os.remove('./data/guild_data/' + str(interaction.guild.id) + ".ndjson")

        # このサーバーのファイルかを確認（気休め）
        try:
            with open("./temp_" + str(interaction.guild.id), encoding='utf-8') as f:
                read_data2 = json.load(f)
        except Exception as e:
            # discordへ結果を送信
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:このファイルはjsonファイルではありません！\nアップロードしたファイルをご確認ください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:This file is not a json file!\nPlease check your uploaded file.:x:", color=0xff0000)

            await interaction.followup.send(embed=embed)

            # 受け取ったファイルの削除
            os.remove("./temp_" + str(interaction.guild.id))

            return

        if read_data2["server_id"] != str(interaction.guild.id):
            # discordへ結果を送信
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:このファイルはこのサーバーのファイルではありません！\nアップロードしたファイルをご確認ください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:This file is not a file on this server!\nPlease check your uploaded file.:x:", color=0xff0000)

            await interaction.followup.send(embed=embed)

            # 受け取ったファイルの削除
            os.remove("./temp_" + str(interaction.guild.id))

            return

        # サーバーファイルを作成する
        with open('./data/guild_data/' + str(interaction.guild.id) +".ndjson", 'a', encoding='utf-8') as f:
            for i in range(0, len(read_data2['server_data'])):
                    writer = ndjson.writer(f)
                    writer.writerow(read_data2['server_data'][str(i)])

        # 受け取ったファイルの削除
        os.remove("./temp_" + str(interaction.guild.id))

        # discordへ結果を送信
        if language == "ja":
            embed=discord.Embed(title="ファイルの受け取りに成功しました！", description="Beta", color=0x00ff7f)
        else:
            embed=discord.Embed(title="Recieve file success!", description="Beta", color=0x00ff7f)

        await interaction.followup.send(embed=embed)

        