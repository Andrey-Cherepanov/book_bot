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

# Command /help
@router.message(Command(commands='help'))
async def process_help_command(message):
    await message.answer(LEXICON['/help'])

# Command /beginning
# sending user first page
@router.message(Command(commands='beginning'))
async def process_beginning_command(message):
    text = book[1]
    id = message.from_user.id
    await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{database.get_current_page(id)}/{len(book)}',
                'forward'
            )
    )
