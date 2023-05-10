book: dict[int, str] = {}
PAGE_SIZE = 1050
BOOK_PATH = 'book/book.txt'

def _get_part_text(text, start, page_size):
    marks = ',.!?:;'
    text = text[start:]
    if page_size > len(text):
        page_size = len(text)
    if (page_size + 1 <= len(text)) and (text[page_size-1] in marks) and (text[page_size] in marks):
        text = text[:page_size]
        while text[-1] in marks:
            text = text[:-1]
    else:
        text = text[:page_size]
    while text and text[-1] not in marks:
        text = text[:-1]
    return text, len(text)

def prepare_book(path: str) -> None:
    with open(path, encoding='utf-8') as file:
        text = file.read()
    global PAGE_SIZE, book
    start = counter = 0
    while start < len(text):
        counter += 1
        prepared_page = _get_part_text(text, start, PAGE_SIZE)
        if not prepared_page[0].lstrip():
            print(prepared_page[0])
            break
        book[counter] = prepared_page[0].lstrip()
        start += prepared_page[1]

prepare_book(BOOK_PATH)
