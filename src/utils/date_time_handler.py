''' converts datetime objects to useable values for json '''
from datetime import datetime


def datetime_handler(candidate):
    ''' handles date object when converting to JSON '''
    if isinstance(candidate, datetime):
        return candidate.isoformat()
    raise TypeError("Unknown type")
