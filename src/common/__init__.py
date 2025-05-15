'''
`/common` is a folder used to store such parts of `lawd`, that are used 
everywhere: in database, telegram bot etc. (there will be more in the future).

for instance: logger or different managers
'''


from .logger import root_logger, db_logger, api_logger
