import hikari
import lightbulb
from dotenv import load_dotenv
import os

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

bot = hikari.GatewayBot(token=TOKEN, intents=hikari.Intents.ALL)
client = lightbulb.client_from_app(bot)
bot.subscribe(hikari.StartingEvent, client.start)

@client.register()
class Meow(
    lightbulb.SlashCommand,
    name="pat",
    description="Give a scritch",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Meow~")


bot.run()
