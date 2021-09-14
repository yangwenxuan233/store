from wxpy.api.bot import Bot

bot = Bot(cache_path=True)
bot.file_helper.send('hello')
