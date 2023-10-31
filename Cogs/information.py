# Discord bot import
import discord
from discord.ext import commands
from discord import app_commands

# My program import
from Cogs.CommandPrograms.information_add import add_program
from Cogs.CommandPrograms.information_delete import delete_program
from Cogs.CommandPrograms.information_list import list_program

#@discord.app_commands.guilds(int(os.environ.get('Test_server')))
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

async def setup(bot: commands.Bot):
    bot.tree.add_command(information(bot, name="information"))