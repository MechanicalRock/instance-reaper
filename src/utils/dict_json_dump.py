''' converts a dict to json and dumps it into a json file '''
import json
from src.utils.date_time_handler import datetime_handler


def dump_dict_in_json_file(data):
    ''' takes a dict and dumps it in a json file '''
    with open('new_json_file.json', 'w') as json_file:
        json.dump(data, json_file, default=datetime_handler)
