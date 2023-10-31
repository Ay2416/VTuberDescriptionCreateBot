# Discord bot import
import os
import glob
import ndjson
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# my program import


class other(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # /help
    @app_commands.command(name="help",description="コマンドの一覧と説明を出します。 / List and explain the commands.")
    #@discord.app_commands.guilds(int(os.environ.get('Test_server')))
    @app_commands.guild_only()
    async def help_command(self, interaction: discord.Interaction):

        await interaction.response.defer()

        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./data/language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]
        
        #Discord上にヘルプを表示
        if language == "ja":
            embed=discord.Embed(title="コマンドリスト")
            embed.add_field(name="/inforaction add name:[表示させたい名前] member:[どのDiscordユーザーに結びつけるか] stream_site_url[配信しているサイトのURL] x_url:[X（Twitter）のURL] number_interrupt:[登録されている番号のどこに割り込ませたいか]", 
                            value="概要欄生成に使う情報を登録します。\n※URLは全て「https\://~」となるように入力してください。\n※「member」については任意入力です。入力がない場合は自分になります。\n※「number_interrupt」については任意入力です。順番を指定する番号は/information listで見ることのできる順番と見比べて指定してください。", inline=False)
            embed.add_field(name="/information delete", value="概要欄生成に使う情報を削除します。", inline=False)
            embed.add_field(name="/information list", value="概要欄生成に使う情報を一覧表示します。", inline=False)
            embed.add_field(name="/order change", value="指定した番号と番号を入れ替える処理を行います。", inline=False)
            embed.add_field(name="/description role:[概要欄生成をさせたいユーザーのロール] display_x:[X（Twitter）の欄を表示させるかどうか（ON/OFF）] title:[敬称の指定]",
                            value="指定したロールがついているユーザー全員の情報を概要欄形式で表示します。\n※「title」については任意入力です。入力がない場合は何もつかない状態で表示されます。", inline=False)
            embed.add_field(name="/hashtag role:[ハッシュタグ生成をさせたいユーザーのロール]", value="指定したロールがついているユーザー全員のX（Twitter）IDから「名前 #X（Twitter）ID」の形で情報を表示します。", inline=False)
            embed.add_field(name="/template role:[概要欄生成をさせたいユーザーのロール] display_x:[X（Twitter）の欄を表示させるかどうか（ON/OFF）] title:[敬称の指定]",
                            value="アプリ「Output Description」での概要欄生成の書式を指定します。\n※「title」については任意入力です。入力がない場合は何もつかない状態で表示されるようになります。", inline=False)
            embed.add_field(name="/language language:[言語の選択（ja/en）]", value="このBotのコマンドの言語を変更します。", inline=False)
            embed.add_field(name="/help", value="このBotのコマンドの簡単な使い方を出します。", inline=False)
        else:
            embed=discord.Embed(title="Command list")
            embed.add_field(name="/inforaction add name:[name you want to display] member:[which Discord user to link to] stream_site_url[URL of the site you are distributing] x_url:[X (Twitter)] number_interrupt:[where in the registered number you want to interrupt]",
                            value="Register the information used to generate the summary field. \n※Please enter all URLs so that they are all [https\://~].\n※About [member], it is an optional input. If there is no input, it will be you. \n※It is optional to input about [number_interrupt]. The number to specify the order should be compared with the order that can be seen in the /information list." , inline=False)
            embed.add_field(name="/information delete", value="Delete the information used to generate the summary field.", inline=False)
            embed.add_field(name="/information list", value="List the information used to generate the summary field.", inline=False)
            embed.add_field(name="/order change", value="Swap the number with the specified number." , inline=False)
            embed.add_field(name="/description role:[Role of the user for whom you want the summary field generation] display_x:[Whether to display the X (Twitter) field (ON/OFF)] title:[Respected title designation]",
                            value="Displays information about all users with the specified role in a summary column format. \n※About [title], it is an optional input. If there is no input, it will be displayed with nothing attached.", inline=False)
            embed.add_field(name="/hashtag role:[the role of the user you want to have hashtag generation]", value="Displays information in the form of [name #X (Twitter) ID] from the X (Twitter) ID of all users with the specified role. ", inline=False)
            embed.add_field(name="/template role:[role of user you want to have summary field generation] display_x:[whether to display X (Twitter) field (ON/OFF)] title:[specify honorific title]",
                            value="Specify the format of the summary column generation in the apps [Output Description]. \n*About [title], it is an optional input. If there is no input, it will be displayed with nothing attached.", inline=False)
            embed.add_field(name="/language language:[Select language (ja/en)]", value="Change the language of this bot's command." , inline=False)
            embed.add_field(name="/help", value="Give a brief usage of this Bot's command." , inline=False)
        #embed.add_field(name="", inline=False)

        await interaction.followup.send(embed=embed)

        if language == "ja":
            embed=discord.Embed(title="アプリ「Output Description」とは？")
            embed.add_field(name="", 
                            value="スマートフォンの場合はユーザーを押し、PCの場合はユーザーを右クリックで出てくる「アプリ」という部分に出てくる所から使うことのできる機能です。\nこれを使用することで「/description」コマンドを打たなくてもすぐに概要欄生成を行うことができます。\n※この機能を使用するには「/template」コマンドで指定をしている必要があります。", inline=False)
            fname="why_output_description_ja.png"
            file = discord.File(fp="./images/why_output_description_ja.png",filename=fname,spoiler=False)
            embed.set_image(url=f"attachment://{fname}")
        else:
            embed=discord.Embed(title="What is the app [Output Description]?")
            embed.add_field(name="", 
                            value="This is a function that can be used by pressing the [User] button on a smartphone, or by right-clicking on the [User] button on a PC, where it appears in the [Apps] section. \nUsing this, you can immediately perform description generation without having to type the [/description] command. \n*To use this feature, you must have specified it in the [/template] command.", inline=False)
            fname="why_output_description_en.png"
            file = discord.File(fp="./images/why_output_description_en.png",filename=fname,spoiler=False)
            embed.set_image(url=f"attachment://{fname}")

        channel_sent = interaction.client.get_channel(interaction.channel_id)
        await channel_sent.send(file=file, embed=embed)
    
    # /language
    @app_commands.command(name="language",description="言語を変更します。（jaまたはen） / Change language. (ja or en)")
    #@discord.app_commands.guilds(int(os.environ.get('Test_server')))
    @app_commands.guild_only()
    @app_commands.choices(language=[discord.app_commands.Choice(name="ja",value="ja"),discord.app_commands.Choice(name="en",value="en")])
    async def language_command(self, interaction: discord.Interaction,language:str):
        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./data/language_json/' + file) as f:
            read_data = ndjson.load(f)

        now_language = read_data[0]["language_mode"]

        # 登録されている言語かどうかの確認
        if language == "ja" or language == "en":
            print("成功！:登録されている言語です！")
        else:
            print("エラー！:コマンドの言語の設定が間違っています！ご確認ください。")
            if now_language == "ja":
                embed=discord.Embed(title="エラー！", description="コマンドの言語指定が間違っています！\nご確認ください。", color=0xff0000)
            elif now_language == "en":
                embed=discord.Embed(title="Error!", description="Command language setting error!\nCheck typing keyword. ([ja] or [en])", color=0xff0000)
            await interaction.response.send_message(embed=embed)
            return
        
        # 既にファイルが存在しているかの判定
        files = glob.glob('./data/language_json/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                print("一致しました！")
                judge = 1
                break
            else:
                judge = 0
        
        file = str(interaction.guild.id) + ".ndjson"

        if(judge == 1):
            os.remove("./data/language_json/" + file)

        content = {
            "language_mode" : language
        }

        with open('./data/language_json/' + file, 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(content)

        # メッセージ表示
        if language == "ja":
            print(str(interaction.guild.id) + "の言語を日本語に変更しました。")
            embed=discord.Embed(title="成功しました!", description="日本語に変更しました。", color=0x00ff40)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        elif language == "en":
            print(str(interaction.guild.id) + "の言語を英語に変更しました。")
            embed=discord.Embed(title="Success!", description="Change to English.", color=0x00ff40)
            await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(other(bot))