from tinydb import TinyDB

db = TinyDB('base.json')


def insert(uep, box, path):

    db.insert({'uep': uep, 'box': box, 'path': path})
