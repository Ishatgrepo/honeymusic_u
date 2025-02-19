
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = "21966961" # integer value, dont use ""
    API_HASH = "fcc0f58560bc9f5ebc9c4207b3d26f2d"
    TOKEN = "7597078204:AAFB5Ku0T6G3Ku5XHDvo3TPdFrZKjTR65sU"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 1094941160 # If you dont know, run the bot and do /id in your private chat with it, also an integer
    
    SUPPORT_CHAT = "aspirantDiscuss"  # Your own group for support, do not add the @
    START_IMG = ""
    EVENT_LOGS = ()  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    MONGO_DB_URI= "mongodb+srv://as1:PUMJvPgRUPEOR0Rz@as1.nam95.mongodb.net/"
    # RECOMMENDED
BOT_USERNAME = getenv("BOT_USERNAME" , "Honeymusics_bot")
    #DATABASE_URL = getenv("DATABASE_URL", "")
    #CASH_API_KEY = (
     #   ""  # Get your API key from https://www.alphavantage.co/support/#api-key
    #)
    #TIME_API_KEY = ""
    # Get your API key from https://timezonedb.com/api

    # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8
    

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
