book: dict[int, str] = {}
PAGE_SIZE = 1050

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
    while text[-1] not in marks:
        text = text[:-1]
    return text, len(text)

def prepare_book(path: str) -> None:
    with open(path, 'r') as f:
        text = f.read()
        page = 1
        start = 0
        size = 0
        while start < len(text):
            page_text, size = _get_part_text(text, start, PAGE_SIZE)
            book[page] = page_text.lstrip()
            page += 1
            start += size

prepare_book('book/book.txt')
