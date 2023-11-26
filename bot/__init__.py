import logging
from logging import FileHandler, StreamHandler
from config import Config
from firebase_admin import db, credentials, initialize_app
from secrets import token_hex

logging.basicConfig(
    level=logging.INFO,
    handlers=[FileHandler("Bot.log", encoding="utf8"), StreamHandler()],
)

from swibots import Client, BotCommand
from .loader import load_modules

LOG = logging.getLogger("Bot")

Bot = Client(Config.BOT_TOKEN, Config.BOT_DESCRIPTION)

load_modules(Config.MODULES_PATH or "modules")

Bot.set_bot_commands(
    [
        # Anime
        BotCommand("anime", "Search for anime", True),
        BotCommand("randomanime", "Get Random Anime", True),
        BotCommand("topanime", "Get list of top animes", True),
        BotCommand("randommanga", "Get Random Manga", True),
        BotCommand("manga", "Search for manga", True),
        BotCommand("topmanga", "Get top manga", True),
        BotCommand("character", "Search for character", True),
        BotCommand("pat", "Pat a user", True),
        BotCommand("slap", "Slap a user", True),
        BotCommand("waifu", "Get random waifu image", True),
        BotCommand("reverseanime", "Search anime from images", True),
        # [WAIFU PROTECT]
        BotCommand("enableprotecc", "Enable Waifu harem", True),
        BotCommand("disableprotecc", "Disable Waifu harem", True),
        BotCommand("protecc", "capture waifu", True),
        BotCommand("harem", "View your harems", True),
        # [Basic Commands]
        BotCommand("start", "Get Start message", True),
        BotCommand("userinfo", "Get User Info", True),
        BotCommand("json", "Get formatted message info", True),
        # Welcomes
        BotCommand("setwelcome", "Enable welcome in current chat", True),
        BotCommand("deletewelcome", "Disable welcome channel", True),
        # Giveaways
        BotCommand("addgiveaway", "Start Giveaway in the chat", True),
        BotCommand("deletegiveaway", "Delete giveaway in the chat", True),
        BotCommand("participate", "Participate in the giveaway", True),
        # Economy
        BotCommand("economy", "Toggle economy enable/disable status", True),
        BotCommand("addcredit", "Add credit to the user", True),
        # Admins
        BotCommand("del", "Delete message", True),
        BotCommand("ban", "ban an user", True),
        BotCommand("unban", "Unban an user", True),
        BotCommand("restrict", "restrict an user", True),
        BotCommand("unrestrict", "remove restriction from user", True),
        #        BotCommand("promote", "Promote user to the roles.", True),
        #       BotCommand("demote", "Remove user from all roles.", True),
        # Games
        BotCommand("akinator", "Start akinator", True),
        BotCommand("pokemon", "Start pokemon game", True),
        BotCommand("cancelpokemon", "Cancel Pokemon Game", True),
        BotCommand("blackjack", "Play Blackjack", True),
        # Commands
        BotCommand("createrole", "Create post to assign roles to users.", True),

        # Levels
        BotCommand("enablelevel", "Enable leveling system", True),
        BotCommand("disablelevel", "Disable leveling", True),
        # Utility
        BotCommand("carbon", "Generate Carbon", True),
        BotCommand("image", "Process and update Image", True),
        BotCommand("qr", "Generate QR Code from text", True),
        BotCommand("webshot", "Capture web as screenshot", True),
        BotCommand("gadget", "Get gadget info", True),
        BotCommand("meaning", "Get meaning of word", True),
        BotCommand("ipinfo", "Get IP Info", True),

        # Owner Commands
        BotCommand("restart", "Restart Bot", True),
        BotCommand("eval", "Run Eval", True),
    ]
)

if Config.SERVICE_ACCOUNT_FILE and Config.FIREBASE_URL:
    try:
        cred = credentials.Certificate(Config.SERVICE_ACCOUNT_FILE)
        initialize_app(cred, {"databaseURL": Config.FIREBASE_URL})
        DB = db.reference()
    except Exception as er:
        LOG.exception(er)
        exit()


async def start():
    await Bot.start()
    #    print(await Bot.get_bot_info(None))
    from io import BytesIO
    from utils.imagehelper import create_level_thumb
    from swibots import EmbeddedMedia, EmbedInlineField

    thumb = create_level_thumb(
        "Devesh Pal", 12, "Magician", file_name=f"{token_hex(5)}.png"
    )
    await Bot.send_message(
        "Level Upgrade",
        user_id=76,
        embed_message=EmbeddedMedia(
            thumbnail=thumb,
            inline_fields=[[EmbedInlineField(title=" ", key="")]],
            title=Bot.user.name,
            header_name="Level Upgrade",
            description="Devesh Pal got promoted to new level, 🎓 Magician",
            header_icon="https://img.icons8.com/?size=256&id=ZhEeFTxx1s3Z&format=png",
            footer_icon="https://img.icons8.com/?size=256&id=59023&format=png",
            footer_title="Participate in chat to level up more!",
        ),
    )


# Bot._loop.run_until_complete(start())
