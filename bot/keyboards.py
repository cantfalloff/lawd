from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


session_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='make a break', callback_data='sk:make_a_break')],
    [InlineKeyboardButton(text='finish the session', callback_data='sk:finish_the_session')]
])


break_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='continue', callback_data='bk:continue')],
    [InlineKeyboardButton(text='finish the session', callback_data='sk:finish_the_session')]
])
