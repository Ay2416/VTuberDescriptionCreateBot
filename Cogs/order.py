# Discord bot import
import discord
from discord.ext import commands
from discord import app_commands

# My program import
from Cogs.CommandPrograms.order_change import order_change_program

#@discord.app_commands.guilds(int(os.environ.get('Test_server')))
class order(app_commands.Group):
    def __init__(self, bot: commands.Bot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
    
    # /order *
    # /order change
    @app_commands.command(name="change",description="指定した番号と番号を入れ替えます。 / Swaps the number with the specified number.")
    @app_commands.guild_only()
    async def information_add_command(self, interaction: discord.Interaction):
        
        await order_change_program().order_change_interaction(interaction)
        

async def setup(bot: commands.Bot):
    bot.tree.add_command(order(bot, name="order"))