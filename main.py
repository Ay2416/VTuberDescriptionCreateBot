# Discord bot import
import os
import glob
import ndjson
import discord
from discord.ext import commands
from dotenv import load_dotenv

# my program import
from ContextMunu import ContextMenu

# main program
load_dotenv()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Botが起動したら実行
@bot.event
async def on_ready():
    print("接続しました！")

    await bot.change_presence(activity=discord.Game(name="create description"))

    # スラッシュコマンドを同期
    await bot.load_extension("Cogs.order")
    await bot.load_extension("Cogs.information")
    await bot.load_extension("Cogs.description_generate")
    await bot.load_extension("Cogs.other")

    await bot.tree.sync()
    print("グローバルコマンド同期完了！")

    #await bot.tree.sync(guild=discord.Object(os.environ.get('Test_server')))
    #print("ギルドコマンド同期完了！")

    # dataフォルダがあるかの確認
    files = glob.glob('./*')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == "data"):
            print("dataファイルを確認しました！")
            judge = 1
            break

    if judge != 1:
        os.mkdir('data')
        print("dataファイルがなかったため作成しました！")

    files = glob.glob('./data/*')

    # guild_dataフォルダがあるかの確認
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == "guild_data"):
            print("guild_dataファイルを確認しました！")
            judge = 1
            break

    if judge != 1:
        os.mkdir('./data/guild_data')
        print("guild_dataファイルがなかったため作成しました！")

    # guild_configフォルダがあるかの確認
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == "guild_config"):
            print("guild_configファイルを確認しました！")
            judge = 1
            break

    if judge != 1:
        os.mkdir('./data/guild_config')
        print("guild_configファイルがなかったため作成しました！")

    # language_jsonフォルダがあるかの確認
    judge = 0
    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == "language_json"):
            print("language_jsonファイルを確認しました！")
            judge = 1
            break

    if judge != 1:
        os.mkdir('./data/language_json')
        print("language_jsonファイルがなかったため作成しました！")

# サーバーに招待された場合に特定の処理をする
@bot.event
async def on_guild_join(guild):
    file = str(guild.id) + ".ndjson"

    content = {
        "language_mode" : "ja"
    }

    with open('./data/language_json/' + file, 'a') as f:
        writer = ndjson.writer(f)
        writer.writerow(content)
    
    print("招待されたため" + str(guild.id) + "のlanguage jsonを作成しました。")

# サーバーからキック、BANされた場合に特定の処理をする
@bot.event
async def on_guild_remove(guild):
    file = str(guild.id) + ".ndjson"

    # language_jsonの削除
    files = glob.glob('./data/language_json/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(guild.id) + ".ndjson":
            judge = 1
            break
    
    if judge == 1:
        os.remove("./data/language_json/" + file)
        print("キックまたはBANされたため、" + str(guild.id) + "のlanguage jsonを削除しました。")

    # guild_dataの削除
    files = glob.glob('./data/guild_data/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(guild.id) + ".ndjson":
            judge = 1
            break
    
    if judge == 1:
        os.remove("./data/guild_data/" + file)
        print("キックまたはBANされたため、" + str(guild.id) + "のguild dataを削除しました。")

    # guild_configの削除
    files = glob.glob('./data/guild_config/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(guild.id) + ".ndjson":
            judge = 1
            break
    
    if judge == 1:
        os.remove("./data/guild_config/" + file)
        print("キックまたはBANされたため、" + str(guild.id) + "のguild configを削除しました。")

# Context Menu コマンド
@bot.tree.context_menu(name='Output Description')
#@discord.app_commands.guilds(int(os.environ.get('Test_server')))
async def output_description(interaction: discord.Interaction, member:discord.User):
    await ContextMenu().output_description_program(interaction, member)

bot.run(os.environ.get('token'))