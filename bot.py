import asyncio
import logging 
import logging.config
from database import db 
from config import Config  
from pyrogram import Client, __version__
from pyrogram.raw.all import layer 
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait 
from aiohttp import web
from plugins import web_server 

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

class Bot(Client): 
    def __init__(self):
        super().__init__(
            Config.BOT_SESSION,
            api_hash=Config.API_HASH,
            api_id=Config.API_ID,
            bot_token=Config.BOT_TOKEN,   
            sleep_threshold=10,
            workers=200,
            plugins={"root": "plugins"}
        )
        self.log = logging

    async def start(self):
        await super().start()
        me = await self.get_me()
        logging.info(f"{me.first_name} with for pyrogram v{__version__} (Layer {layer}) started on @{me.username}.")
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Config.PORT).start()
        self.id = me.id
        self.username = me.username
        self.first_name = me.first_name
        self.set_parse_mode(ParseMode.DEFAULT)
        text = "<b>๏[-ิ_•ิ]๏ ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ !</b>"
        logging.info(text)
        for owner_id in Config.BOT_OWNER_ID:
            try:
                await self.send_message(owner_id, f"<b>@{me.username} Is Restarted ✅️</b>")
                logging.info(f"Notification sent to owner {owner_id}")
            except Exception as e:
                logging.error(f"Failed to notify owner {owner_id}: {e}")
        success = failed = 0

        users = await db.get_all_frwd()
        async for user in users:
           chat_id = user['user_id']
           try:
              await self.send_message(chat_id, text)
              success += 1
           except FloodWait as e:
              await asyncio.sleep(e.value + 1)
              await self.send_message(chat_id, text)
              success += 1
           except Exception:
              failed += 1 
        if (success + failed) != 0:
           await db.rmve_frwd(all=True)
           logging.info(f"Restart message status"
                 f"success: {success}"
                 f"failed: {failed}")

    async def stop(self, *args):
        msg = f"@{self.username} stopped. Bye."
        await super().stop()
        logging.info(msg)

app = Bot()
app.run()
