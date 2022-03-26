from os import walk

from tinydb import Query, TinyDB

db = TinyDB('base.json')


def insert(uep, box, path):

    db.insert({'box': box, 'imgs': path})


def querry(box: str):

    Box = Query()
    return db.search(Box.box == box)


def mapping():

    for away, _, files in walk('./'):

        if away != './' and away != './photos':

            db.insert(
                {
                    'box': (away.split('./'))[1],
                    'imgs': files,
                    'leng': len(files),
                }
            )
