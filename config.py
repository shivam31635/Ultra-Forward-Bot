import datetime
from os import environ 

class Config:
    API_ID = environ.get("API_ID", "27499182")
    API_HASH = environ.get("API_HASH", "9c58142ef6abed28808a50e3e983c39c")
    BOT_TOKEN = environ.get("BOT_TOKEN", "7969829411:AAHSfw299OHm1R-0_aZLBfhtx6APWJLOnOs") 
    BOT_SESSION = environ.get("BOT_SESSION", "Auto_Forward") 
    DATABASE_URI = environ.get("DATABASE", "mongodb+srv://Ultaforward:Ultaforward@cluster0.sjxy7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DATABASE_NAME = environ.get("DATABASE_NAME", "Telegram_files")
    BOT_OWNER_ID = [int(id) for id in environ.get("BOT_OWNER_ID", '6133992240').split()]
    LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1001876507111'))
    FORCE_SUB_CHANNEL = environ.get("FORCE_SUB_CHANNEL", "https://t.me/Crazybotz") 
    FORCE_SUB_ON = environ.get("FORCE_SUB_ON", "True")
    PORT = environ.get('PORT', '8080')
   
class temp(object): 
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []
    
#Dont Remove My Credit @Silicon_Bot_Update 
#This Repo Is By @Silicon_Official 
# For Any Kind Of Error Ask Us In Support Group @Silicon_Botz 
