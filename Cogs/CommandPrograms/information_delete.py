# Discord bot import
import os
import glob
import ndjson
import asyncio
import discord

# My program import


class delete_program:
    async def delete_interaction(self, interaction):
        
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

        # ボタン
        view = discord.ui.View()
        delete_button = DeleteButton(interaction.user)  # コマンドを呼んだユーザを渡す
        view.add_item(delete_button)  
        with open('./data/guild_data/' + str(interaction.guild.id) + ".ndjson") as f:
            read_data = ndjson.load(f)
        
        # embedを出すための処理
        if language == "ja":
            embed=discord.Embed(title="登録されているユーザー", color=0x00ff7f)
        else:
            embed=discord.Embed(title="Registered Users", color=0x00ff7f)

        global count
        followup_send = 0
        count = 0
        cut = 10
        for j in range(0, len(read_data)):

            if language == "ja":
                embed.add_field(name=str(j+1) + "." + read_data[j]["name"], 
                                value="\n関連Discordユーザー：<@" + read_data[j]["member"] + ">\n配信サイトURL：" + 
                                read_data[j]["stream_site_url"] + "\n X（旧Twitter）URL：" + "https://x.com/" + read_data[j]["x_name"], inline=False)
            else:
                embed.add_field(name=str(j+1) + "." + read_data[j]["name"],
                                value="\nRelated Discord users:<@" + read_data[j]["member"] + ">\nStream site URL:" + 
                                read_data[j]["stream_site_url"] + "\nX(Twitter) URL:" + "https://x.com/" + read_data[j]["x_name"], inline=False)

            count = count + 1
            
            if j == len(read_data) - 1:
                #表示させる
                if followup_send == 0:
                    await interaction.followup.send(embed=embed,view=view)
                else:
                    #print(str(interaction.channel_id))
                    channel_sent = interaction.client.get_channel(interaction.channel_id)
                    await channel_sent.send(embed=embed, view=view)
                
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

# モーダルボタンのクラス
class DeleteButton(discord.ui.Button):
    # コンストラクタの引数に user を追加
    def __init__(self, user: discord.User, style=discord.ButtonStyle.green, label='Next >>', **kwargs):
        self.user_id = user.id  # クラス変数にユーザ ID を保存
        super().__init__(style=style, label=label, **kwargs)

    async def callback(self, interaction: discord.Interaction):
        # 保存したユーザとボタンを押したユーザが同じかどうか
        if self.user_id == interaction.user.id:

            # 番号を入力するためのウィンドウを表示する
            await interaction.response.send_modal(answer_input())

            #await interaction.message.delete()

# モーダルウィンドウ用のクラス
class answer_input(discord.ui.Modal, title='削除したい番号を入力してください。 / Select delete number.'):

    answer_number = discord.ui.TextInput(
        label='Number',
        placeholder='例：1 / Example: 1',
    )

    async def on_submit(self, interaction: discord.Interaction):

        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./data/language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        # 入力されたものが数字であるかどうか
        try:
            answer = int(self.answer_number.value)
            #print(answer)
        except Exception as e:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:入力されたものが数字ではありません。\nもう一度コマンドを実行しなおしてください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:What was entered is not a number. \nPlease execute the command again.:x:", color=0xff0000)
            #await interaction.message.delete()
            await interaction.response.send_message(embed=embed)
            return
        
        # 入力された数字が範囲内にあるか
        #print(count)
        if answer < 1 or answer > count:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:入力された数字が有効ではありません。\nもう一度コマンドを実行しなおしてください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:The number entered is not valid. \nPlease execute the command again.:x:", color=0xff0000)

            #await interaction.message.delete()
            await interaction.response.send_message(embed=embed)
            return

        # guild_dataから削除する
        with open('./data/guild_data/' + str(interaction.guild.id) + ".ndjson") as f:
                read_data = ndjson.load(f)
        
        name = read_data[answer-1]["name"]
        
        # もしguild_dataの中身が1つだけだったらファイルごと削除をする
        if len(read_data) == 1:
            os.remove('./data/guild_data/' + str(interaction.guild.id) + ".ndjson")
        else:
            for j in range(0, len(read_data)):
                if j == answer-1:
                    del read_data[j]
                    break
            
            os.remove('./data/guild_data/' + str(interaction.guild.id) + ".ndjson")

            for k in range(0, len(read_data)):
                with open('./data/guild_data/' + str(interaction.guild.id) + ".ndjson", 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(read_data[k])

        #await interaction.message.delete()

        if language == "ja":
            embed=discord.Embed(title="削除が完了しました！", description= name + "を削除しました！", color=0x00ff7f)
        else:
            embed=discord.Embed(title="Delete completed!", description= "Deleted " + name + "!", color=0x00ff7f)

        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:

        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./data/language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        if language == "ja":
            await interaction.response.send_message('エラーが発生しました。', ephemeral=False)
        else:
            await interaction.response.send_message('An error has occurred.' , ephemeral=False)

        #traceback.print_exception(type(error), error, error.__traceback__)