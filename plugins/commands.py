import os
import sys
import asyncio 
import datetime
import psutil
from pyrogram.types import Message
from database import db, mongodb_version
from config import Config, temp
from platform import python_version
from translation import Translation
from pyrogram import Client, filters, enums, __version__ as pyrogram_version
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument
import pytz
from datetime import datetime

TIMEZONE = "Asia/Kolkata"

main_buttons = [[
        InlineKeyboardButton('❗️ʜᴇʟᴘ', callback_data='help')
        ],[
        InlineKeyboardButton('📜 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/CloneV2Support'),
        InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/Crazybotz')
        ],[
        InlineKeyboardButton('💳 ᴅᴏɴᴀᴛᴇ', callback_data='donate')
        ]]
#===================Start Function===================#

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user

    if Config.FORCE_SUB_ON:
        try:
            member = await client.get_chat_member(Config.FORCE_SUB_CHANNEL, user.id)
            if member.status == "kicked":
                await client.send_message(
                    chat_id=message.chat.id,
                    text="You are banned from using this bot.",
                )
                return
        except Exception:
            try:
                f_link = await client.export_chat_invite_link(Config.FORCE_SUB_CHANNEL)
                join_button = [
                    [InlineKeyboardButton("⛔ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ⛔", url=f"{f_link}")],
                    [InlineKeyboardButton("↻ ᴛʀʏ ᴀɢᴀɪɴ", url=f"https://t.me/{client.username}?start=start")]
                ]
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo="https://telegra.ph/file/db2ea1a910dd7f83572f7.jpg",
                    caption="<b>⚠️ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ ᴍᴇ, ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ.</b>",
                    reply_markup=InlineKeyboardMarkup(join_button)
                )
                return
            except Exception:
                await client.send_message(
                    chat_id=message.chat.id,
                    text="⚠️ Unable to fetch the join link. Please contact the admin.",
                )
                return

    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, message.from_user.mention)
        await client.send_message(
            chat_id=Config.LOG_CHANNEL,
            text=f"#Forwrad_NewUser\n\nIᴅ - {user.id}\nNᴀᴍᴇ - {message.from_user.mention}"
        )
    
    reply_markup = InlineKeyboardMarkup(main_buttons)
    current_time = datetime.now(pytz.timezone(TIMEZONE))
    curr_time = current_time.hour        
    if curr_time < 12:
        gtxt = "ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ 🌞" 
    elif curr_time < 17:
        gtxt = "ɢᴏᴏᴅ ᴀғᴛᴇʀɴᴏᴏɴ 🌗" 
    elif curr_time < 21:
        gtxt = "ɢᴏᴏᴅ ᴇᴠᴇɴɪɴɢ 🌘"
    else:
        gtxt = "ɢᴏᴏᴅ ɴɪɢʜᴛ 🌑"
    await client.send_message(
        chat_id=message.chat.id,
        text=Translation.START_TXT.format(message.from_user.mention, gtxt),
        reply_markup=reply_markup
    )

#==================Restart Function==================#

@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER_ID))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>ᴛʀʏɪɴɢ ᴛᴏ ʀᴇsᴛᴀʀᴛ...</i>"
    )
    await asyncio.sleep(5)
    await msg.edit("<i>sᴇʀᴠᴇʀ ʀᴇsᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
#==================Callback Functions==================#

@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    await query.message.edit_text(
        text=Translation.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('• ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ❓', callback_data='how_to_use')
            ],[
            InlineKeyboardButton('• sᴇᴛᴛɪɴɢs ', callback_data='settings#main'),
            InlineKeyboardButton('• sᴛᴀᴛᴜs ', callback_data='status')
            ],[
            InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='back'),
            InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about')
            ]]
        ))

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    await query.message.edit_text(
        text=Translation.HOW_USE_TXT,
             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='help')]]),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query):
    reply_markup = InlineKeyboardMarkup(main_buttons)
    current_time = datetime.now(pytz.timezone(TIMEZONE))
    curr_time = current_time.hour        
    if curr_time < 12:
        gtxt = "ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ 🌞" 
    elif curr_time < 17:
        gtxt = "ɢᴏᴏᴅ ᴀғᴛᴇʀɴᴏᴏɴ 🌗" 
    elif curr_time < 21:
        gtxt = "ɢᴏᴏᴅ ᴇᴠᴇɴɪɴɢ 🌘"
    else:
        gtxt = "ɢᴏᴏᴅ ɴɪɢʜᴛ 🌑"
    await query.message.edit_text(
       reply_markup=reply_markup,
       text=Translation.START_TXT.format(
                query.from_user.first_name, gtxt))

@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    await query.message.edit_text(
        text=Translation.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='back')]]),
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.HTML,
    )

@Client.on_callback_query(filters.regex(r'^donate'))
async def donate(bot, query):
    await query.message.edit_text(
        text=Translation.DONATE_TXT,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='back')]]),
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.HTML,
    )

START_TIME = datetime.datetime.now()

def format_uptime():
    uptime = datetime.datetime.now() - START_TIME
    total_seconds = uptime.total_seconds()

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    uptime_components = []
    if int(days) > 0:
        uptime_components.append(f"{int(days)} D" if int(days) == 1 else f"{int(days)} D")
    if int(hours) > 0:
        uptime_components.append(f"{int(hours)} H" if int(hours) == 1 else f"{int(hours)} H")
    if int(minutes) > 0:
        uptime_components.append(f"{int(minutes)} M" if int(minutes) == 1 else f"{int(minutes)} M")
    if int(seconds) > 0:
        uptime_components.append(f"{int(seconds)} Sec" if int(seconds) == 1 else f"{int(seconds)} Sec")

    uptime_str = ', '.join(uptime_components)
    return uptime_str

    uptime_str = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
    return uptime_str

@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query):
    users_count, bots_count = await db.total_users_bots_count()
    total_channels = await db.total_channels()

    # Calculate bot uptime
    uptime_str = format_uptime()

    await query.message.edit_text(
        text=Translation.STATUS_TXT.format(users_count, bots_count, temp.forwardings, total_channels),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='help'),
             InlineKeyboardButton('• sᴇʀᴠᴇʀ sᴛᴀᴛs', callback_data='server_status')
]]),
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

#Dont Remove My Credit @Silicon_Bot_Update 
#This Repo Is By @Silicon_Official 
# For Any Kind Of Error Ask Us In Support Group @Silicon_Botz 

@Client.on_callback_query(filters.regex(r'^server_status'))
async def server_status(bot, query):
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()

    await query.message.edit_text(
        text=Translation.SERVER_TXT.format(cpu, ram),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='status')]]),
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

#===================Donate Function===================#

@Client.on_message(filters.private & filters.command(['donate']))
async def restart(client, message):
    await message.reply_text(
        text="<b><u>💖 ᴛʜᴀɴᴋ ʏᴏᴜ ᴛʜᴀᴛ ʏᴏᴜ ᴀʀᴇ ᴄᴏɴꜱɪᴅᴇʀɪɴɢ ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴏᴜʀ ʙᴏᴛ.</u>\n\n"
             "<code>» ᴅᴏɴᴀᴛᴇ ᴜꜱ ᴛᴏ ᴋᴇᴇᴘ ᴏᴜʀ ꜱᴇʀᴠɪᴄᴇꜱ ᴄᴏɴᴛɪɴᴏᴜꜱʟʏ ᴀʟɪᴠᴇ "
             "ʏᴏᴜ ᴄᴀɴ ꜱᴇɴᴅ ᴀɴʏ ᴀᴍᴏᴜɴᴛ ᴅᴏɴᴀᴛᴇ ᴏɴʟʏ ᴏɴᴇ ʀᴜᴘᴇᴇ.</code>\n\n"
             "<u>᚜ ᴘᴀʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅs ᚛</u>\n\n"
             "💳 ᴜᴘɪ ɪᴅ: <code>shivamnamdev01@axl</code>\n\n"
             "ᴏʀ ᴅᴏɴᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇ ᴍᴇ <a href=https://t.me/heartlesssn>Cʀᴀᴢʏ</a></b>"
    )
