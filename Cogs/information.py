# Discord bot import
import os
import discord
from discord.ext import commands
from discord import app_commands

# My program import
from Cogs.CommandPrograms.information_add import add_program
from Cogs.CommandPrograms.information_delete import delete_program
from Cogs.CommandPrograms.information_list import list_program
from Cogs.CommandPrograms.information_input import input_program
# ベータ版機能判定用のデコレータ
def beta_check(func):
    guilds = []
    if os.environ.get('Beta_server') != None and os.environ.get('Beta_server') != "0":
        for s in os.environ.get('Beta_server').split(','):
            s = s.strip()
            if s != "" and s != "0":
                if int(s) not in guilds:
                    guilds.append(int(s))
    if os.environ.get('Test_server') != None and os.environ.get('Test_server') != "0":
        for s in os.environ.get('Test_server').split(','):
            s = s.strip()
            if s != "" and s != "0":
                if int(s) not in guilds:
                    guilds.append(int(s))

    if len(guilds) > 0:
        return discord.app_commands.guilds(*guilds)(func)
    else:
        return discord.app_commands.guilds(0)(func)

class information(app_commands.Group):
    def __init__(self, bot: commands.Bot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
    
    # /information *
    # /information add
    @app_commands.command(name="add",description="概要の情報を追加します。 / Add description.")
    @app_commands.describe(name="配信者の名前 / streamer name")
    @app_commands.describe(stream_site_url="YouTube Channel URL, Twitch User page etc...")
    @app_commands.describe(x_url="x(Twitter) URL")
    @app_commands.describe(member="Discordユーザーの指定 / Discord User Designation")
    @app_commands.describe(member="登録されている順番のどこに割り込ませるか / Where to interrupt the registered order")
    @app_commands.guild_only()
    async def information_add_command(self, interaction: discord.Interaction, name:str, stream_site_url:str, x_url:str, member:discord.Member=None, number_interrupt:int=None):
        
        if member == None:
            member = interaction.user.id
        else:
            member = member.id

        await add_program().add_interaction(interaction, name, member, stream_site_url, x_url, number_interrupt)

    # /information delete
    @app_commands.command(name="delete",description="概要の情報を削除します。 / Delete description.")
    @app_commands.guild_only()
    async def information_delete_command(self, interaction: discord.Interaction):

        await delete_program().delete_interaction(interaction)

    # /information list
    @app_commands.command(name="list",description="このサーバーの登録されている概要の一覧を表示します。 / View description list on the this server.")
    @app_commands.guild_only()
    async def information_list_command(self, interaction: discord.Interaction):

        await list_program().list_interaction(interaction)

    # /information input
    @app_commands.command(name="input",description="このサーバーの登録されている概要データをCSVファイルから一括で追加登録します。 / Add data for this server from a CSV file.")
    @app_commands.guild_only()
    @beta_check
    async def information_input_command(self, interaction: discord.Interaction, file:discord.Attachment):

        await input_program().input_interaction(interaction, file)

    # /information output
    @app_commands.command(name="output",description="このサーバーの登録されている概要データをCSVファイルで出力します。 / Outputs the registered data in a CSV file.")
    @app_commands.guild_only()
    @beta_check
    async def information_output_command(self, interaction: discord.Interaction):

        await output_program().output_interaction(interaction)

async def setup(bot: commands.Bot):
    bot.tree.add_command(information(bot, name="information"))