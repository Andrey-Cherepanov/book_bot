from pony.orm import *

db = Database()

class Bookmarks(db.Entity):
    id_user = PrimaryKey(int)
    curr_page = Requred(int)
    bookmarks = Optional(str)
