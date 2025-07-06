import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from handlers.mongo_handler import MongoDBHandler
load_dotenv()

class RoleplayBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.reactions = True
        
        super().__init__(command_prefix='!', intents=intents)
        
        self.db = MongoDBHandler()

    async def setup_hook(self):
        await self.db.initialize()
        # Sincronizar comandos slash
        await self.load_extension('cogs.dni')
        await self.load_extension('cogs.server_voting')
        await self.load_extension('cogs.environment')
        await self.load_extension('cogs.staff_rating')
        await self.tree.sync()
        print("Comandos slash sincronizados")

bot = RoleplayBot()


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name}")

if __name__ == '__main__':
    bot.run(os.getenv("TOKEN"))
