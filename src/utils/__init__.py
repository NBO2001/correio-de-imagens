from calendar import monthrange
from os import mkdir, path, walk
from shutil import copy
from sys import platform


def getRangeMonth(month, year):
    date = monthrange(year, month)
    return {
        'date_start': f'1/{month}/{year}',
        'data_end': f'{date[1]}/{month}/{year}',
    }


def padronizador(index, cliente):

    client = '0' * (2 - len(cliente)) + f'{cliente}'
    return f'G.01.{client}.' + '0' * (7 - len(index)) + index


def convert_url(value):

    if platform.upper() == 'LINUX':
        return value
    else:
        return '\\'.join(value.split('/'))


def trim(value):
    try:
        return ((value).lstrip()).rstrip()
    except:
        return value


def create_folder(father_code, location='./'):

    if not path.exists(convert_url(f'{location}{father_code}')):
        mkdir(convert_url(f'{location}{father_code}'), 0o777)


def compartor_folders(folder_now, folder_validate):

    try:
        array_folder_now = folder_now.split('.')
        array_folder_validate = folder_validate.split('.')

        if int(array_folder_now[0]) == int(array_folder_validate[0]):
            if int(array_folder_now[1]) == int(array_folder_validate[1]):
                return folder_now
            else:
                if int(array_folder_now[1]) > int(array_folder_validate[1]):
                    return folder_now
                else:
                    return folder_validate
        else:
            if int(array_folder_now[0]) > int(array_folder_validate[0]):
                return folder_now
            else:
                return folder_validate
    except:
        return folder_now


def count_folders():
    count = 0
    ultima_box = '1.1'
    for path, _, _ in walk('./'):
        if path != './':
            count += 1
            inpath = path.removeprefix('./')
            ultima_box = compartor_folders(ultima_box, inpath)

    return (count, ultima_box)


def photos_move():

    create_folder('photos')
    for away, _, files in walk(convert_url('./')):
        if away != convert_url('./') and away != convert_url('./photos'):

            for file in files:
                copy(convert_url(f'{away}/{file}'), convert_url('./photos/'))


def getDayEnd(month, year):
    date = monthrange(year, month)
    return date[1]


def getRangeMonth(month, year):
    date = monthrange(year, month)
    return {
        'date_start': f'1/{month}/{year}',
        'data_end': f'{date[1]}/{month}/{year}',
    }


def trate_only_date(date, reverse=False):

    date_range = date.split('/')

    if len(date_range) == 3:

        return date

    elif len(date_range) == 2:

        return (
            f'1/{date_range[0]}/{date_range[1]}'
            if not reverse
            else f'{getDayEnd(int(date_range[0]),int(date_range[1]))}/{date_range[0]}/{date_range[1]}'
        )

    elif len(date_range) == 1:

        return (
            f'1/1/{date_range[0]}'
            if not reverse
            else f'{getDayEnd(12,int(date_range[0]))}/12/{date_range[0]}'
        )

    else:
        return date


def trate_date(date):

    date_range = (date.upper()).split('A')

    if len(date_range) == 2:
        first_date = trate_only_date(trim(date_range[0]))
        sec_date = trate_only_date(trim(date_range[1]), reverse=True)

        return (first_date, sec_date)
    else:
        first_date = trate_only_date(trim(date_range[0]))
        sec_date = trate_only_date(trim(date_range[0]), reverse=True)

        return (first_date, sec_date)
