from flask.json import JSONEncoder
import datetime


class DateTimeJSONEncoder(JSONEncoder):
    """Add support for serializing timedeltas"""
    def default(self, o):
        if type(o) == datetime.timedelta:
            return str(o)
        elif type(o) == datetime.datetime:
            return o.isoformat()
        else:
            return super().default(o)
