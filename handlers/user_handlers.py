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

# Command /continue
# sending user their current page
@router.message(Command(commands='continue'))
async def process_continue_command(message):
    id = message.from_user.id
    text = book[database.get_current_page(id)]
    await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{database.get_current_page(id)}/{len(book)}',
                'forward'
            )
    )

# Command /bookmarks
# sending user a list of bookmarks
@router.message(Command(commands='bookmarks'))
async def process_continue_command(message):
    bookmarks = database.extract_bookmarks(message.from_user.id)
    if bookmarks:
        await message.answer(
            text=LEXICON['/bookmarks'],
            reply_markup=create_bookmarks_keyboard(*bookmarks)
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])

# Key Forward on inline kb
# sending user next page
@router.callback_query(Text(text='forward'))
async def process_forward_press(callback):
    id = callback.from_user.id
    page = database.get_current_page(id) + 1
    if page < len(book):
        database.set_current_page(id=id, page=page)
        text = book[page]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{database.get_current_page(id)}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()
