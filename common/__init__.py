'''
`/common` is a folder used to store such parts of thatrack, that are used 
everywhere: in database, telegram bot etc. (there will be more in the future).

for instance: logger or different managers
'''


from .logger import db_logger, bot_logger, ShortMessages
