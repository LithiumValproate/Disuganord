import hikari
import lightbulb
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

bot = hikari.GatewayBot(token=token, logs={"version": 1, "incremental": True,
                                             "loggers": {"hikari": {"level": "INFO"},
                                             "hikari.ratelimits": {"level": "TRACE_HIKARI"},
                                             "lightbulb": {"level": "DEBUG"}}})
client = lightbulb.client_from_app(bot)
bot.subscribe(hikari.StartingEvent, client.start)

@ client.register()


class Ping(
    lightbulb.SlashCommand,
    name="ping",
    description="checks the bot is alive",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Pong!")


bot.run()
