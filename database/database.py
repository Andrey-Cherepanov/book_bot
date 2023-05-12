from pony.orm import *
from database.models import *

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables = True)

@db_session
def extract_bookmarks(id):
    bookmarks = list(select(
                bm for bm in Bookmarks if bm.id_user == id))[0].bookmarks
    if bookmarks == '':
        return set()
    bookmarks = set(map(int, bookmarks.split(',')))
    return bookmarks

@db_session
def add_user(id, page=1):
    if _is_user_in_db(id):
        return
    user = Bookmarks(id_user=id,
                     curr_page=page,
                     bookmarks='')
    commit()

@db_session
def set_current_page(id, page):
    user = list(select(bm for bm in Bookmarks
                        if bm.id_user==id))[0]
    user.curr_page = page
    commit()

@db_session
def add_bookmark(id, bookmark):
    user = list(select(bm for bm in Bookmarks
                        if bm.id_user==id))[0]
    new_bookmarks = extract_bookmarks(id)
    new_bookmarks.add(bookmark)
    new_bookmarks = ','.join(list(map(str, new_bookmarks)))
    user.bookmarks = new_bookmarks

    commit()

@db_session
def _is_user_in_db(id):
    ids = [usr.id_user for usr in list(select(usr for usr in Bookmarks))]
    return id in ids

@db_session
def get_current_page(id):
    user = list(select(bm for bm in Bookmarks
                        if bm.id_user==id))[0]
    return user.curr_page

@db_session
def remove_bookmark(id, bookmark):
    user = list(select(bm for bm in Bookmarks
                        if bm.id_user==id))[0]
    new_bookmarks = extract_bookmarks(id)
    if bookmark in new_bookmarks:
        new_bookmarks.remove(bookmark)
    if new_bookmarks:
        new_bookmarks = ','.join(list(map(str, new_bookmarks)))
    else:
        new_bookmarks = ''
    user.bookmarks = new_bookmarks

    commit()
