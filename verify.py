import dotenv
import hikari
import lightbulb
import os

dotenv.load_dotenv(".env")
_TOKEN_ = os.getenv("TOKEN")
_GUILD_ID_ = int(os.getenv("GUILD_ID"))
_CHANNEL_V_ = int(os.getenv("V_CHAN_ID"))
_CHANNEL_W_ = int(os.getenv("W_CHAN_ID"))
ROLE_0 = "news"
ROLE_1 = "tukas"

intents = hikari.Intents.GUILDS | hikari.Intents.GUILD_MEMBERS
b_giveNewRole = hikari.GatewayBot(_TOKEN_, intents=intents)


@b_giveNewRole.listen(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent):
    guild = event.guild_id
    member = event.member
    roles = await b_giveNewRole.rest.fetch_roles(guild)
    role_0 = next((role for role in roles if role.name == ROLE_0), None)
    if role_0:
        await b_giveNewRole.rest.add_role_to_member(guild, member, role_0)
        await b_giveNewRole.rest.create_message(
            _CHANNEL_W_,
            f"Welcome {member.mention} to the server!"
        )


b_verify = lightbulb.client_from_app(b_giveNewRole)
b_giveNewRole.subscribe(hikari.StartedEvent, b_verify.start)


@b_verify.register()
class Verify(
    lightbulb.SlashCommand,
    name="verify",
    description="Verified as human"
):
    @lightbulb.invoke
    async def verify(self, ctx: lightbulb.Context) -> None:
        if ctx.channel_id != _CHANNEL_V_:
            await ctx.respond(
                "This command can only be used in the designated channel.",
                flags=hikari.MessageFlag.EPHEMERAL
            )
            return
        buttons = hikari.impl.MessageActionRowBuilder()
        buttons.add_interactive_button(
            hikari.ButtonStyle.SECONDARY,
            "answer_2",
            label="2",
        )
        buttons.add_interactive_button(
            hikari.ButtonStyle.SECONDARY,
            "answer_3",
            label="3",
        )
        buttons.add_interactive_button(
            hikari.ButtonStyle.SECONDARY,
            "answer_4",
            label="4",
        )
        await ctx.respond(
            "🤖 Q: 2 + 2 = ?",
            components=[buttons]
        )


@b_verify.app.listen(hikari.ComponentInteractionCreateEvent)
async def on_button_click(event: hikari.ComponentInteractionCreateEvent) -> None:
    if event.interaction.channel_id != _CHANNEL_V_:
        return
    if event.interaction.component_type is not hikari.InteractionType.MESSAGE_COMPONENT:
        return
    custom_id = event.interaction.custom_id

    if custom_id == "answer_4":
        await event.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            content="Bingo! You're already verified!"
        )
        guild_id = event.interaction.guild_id
        member_id = event.interaction.user.id
        roles = await b_verify.rest.fetch_roles(guild_id)
        role_1 = next((role for role in roles if role.name == ROLE_1), None)
        if role_1:
            await b_verify.rest.add_role_to_member(guild_id, member_id, role_1)
    else:
        await event.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            content="I'm bot, you're bot as well."
        )


b_giveNewRole.run()
