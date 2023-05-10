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


# Key Backward on inline kb
# sending user previous page
@router.callback_query(Text(text='forward'))
async def process_forward_press(callback):
    id = callback.from_user.id
    page = database.get_current_page(id) - 1
    if page >= 1:
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

# Key with current page on inline kb
# add a new bookmark
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback):
    id = callback.from_user.id
    curr_page = database.get_current_page(id)
    database.add_bookmark(id, curr_page)
    await callback.answer(LEXICON['new_bookmark'])


# Key with bookmark
# sending user a page from bookmark
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback):
    text = book[int(callback.data)]
    database.set_current_page(callback.from_user.id, int(callback.data))
    await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{int(callback.data)}/{len(book)}',
                    'forward'))
    await callback.answer()

# Key Edit
# sending user an edit keyboard
@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *database.extract_bookmarks(callback.from_user.id)
        )
    )
    await callback.answer()

# Key Cancel
@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()
