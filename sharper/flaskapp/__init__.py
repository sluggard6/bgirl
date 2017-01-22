import json
from flask import current_app, request

__author__ = '"linnchord gao" <linnchord@gmail.com>'


def jsonify(*args, **kwargs):
    return current_app.response_class(json.dumps(dict(*args, **kwargs),
                                                 indent=None if request.is_xhr else 2), mimetype='application/json')