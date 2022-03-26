from os import mkdir, path, walk
from shutil import copy
from sys import platform


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
