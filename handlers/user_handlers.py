from aiogram import Router
from aiogram.filters import Text, Command, CommandStart
from aiogram.types import CallbackQuery, Message

from database import database
from filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book

router = Router()

# Command /start
@router.message(CommandStart())
async def process_start_command(message):
    await message.answer(LEXICON['/start'])
    database.add_user(message.from_user.id)
