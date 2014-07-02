import os
import datetime
__author__ = 'tasyrkin'

_separator = '\n'
_file_prefix = 'storage_current'
_directory = './storage'

def _get_path(dir_name, file_name):
    return dir_name + '/' + file_name

def _get_file_name(file_name, postfix):
    return _file_prefix + '__' + file_name + '__' + postfix

class PersistData:
    def __init__(self, list, set):
        self.list = list
        self.set = set

def store(persist_data, start_url_domain):
    """
    Persists the data for a start_url_domain
    """

    list_file_name = _get_path(_directory, _get_file_name(start_url_domain, 'LIST'))
    store_collection(persist_data.list, list_file_name)

    set_file_name = _get_path(_directory, _get_file_name(start_url_domain, 'SET'))
    store_collection(persist_data.set, set_file_name)

def load(start_url_domain):
    set_to_return = set()

    file_path = _get_path(_directory, _get_file_name(start_url_domain))

    file_to_restore = open(file_path, 'r')

    string_in_file = ''

    for line in file_to_restore.readlines():
        string_in_file += line

    file_to_restore.close()

    os.rename(file_path, file_path + str(datetime.datetime.now()))

    while len(string_in_file) > 0:
        separation_result = string_in_file.partition(_separator)
        set_to_return.add(separation_result[0])
        string_in_file = separation_result[2]

    return set_to_return

def store_collection(collection, file_path):

    file_to_store = open(file_path, 'w')

    string_to_store = ''

    for item in collection:
        if len(string_to_store) > 0:
            string_to_store += _separator
        string_to_store += item

    file_to_store.write(string_to_store)
    file_to_store.flush()
    file_to_store.close()
