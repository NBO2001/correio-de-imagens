from os import walk
import pandas as pd
from tinydb import Query, TinyDB
from utils import photos_move

db = TinyDB('base.json')
db_plan = TinyDB('base_plan.json')

def create_table():
    try:
        plan = pd.DataFrame(db_plan.all())
        plan["data_de_Inicio"] = pd.to_datetime(plan["data_de_Inicio"])
        plan["data_Final"] = pd.to_datetime(plan["data_Final"])
        plan.to_excel('pre_inv.xlsx', index=False, sheet_name='Geral')
        photos_move()
        return True
    except Exception as e:
        print(e)
        return False

def insert(uep, box, path):

    db.insert({'box': box, 'imgs': path})


def insert_plan(
    index, setor, descricao, chaveA, chaveB, data_de_Inicio, data_Final
):
    try:

        db_plan.insert(
            {
                'index': index,
                'setor': setor,
                'descricao': descricao,
                'chaveA': chaveA,
                'chaveB': chaveB,
                'data_de_Inicio': data_de_Inicio,
                'data_Final': data_Final,
            }
        )
        return True
    except Exception as e:
        print(e)
        return False


def querry(box: int):

    return db.get(doc_id=box)


def mapping():
    try:

        wl_resul = tuple(walk('./'))[0][1]
        wl_resul.sort()

        for path in wl_resul:
            if path != './' and path != './photos':
                files = tuple(walk(f'./{path}'))[0][2]

                for file in files:

                    if len(db.search(Query().imgs.search(file))) == 0:
                        db.insert({'box': path, 'imgs': file})

    except Exception as e:
        print(e)
        breakpoint()
