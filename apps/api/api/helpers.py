from functools import wraps
from flask import request, abort
from config import ACCESS_TOKEN


def access_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if token := request.args.get('token', None):
            if token == ACCESS_TOKEN:
                return f(*args, **kwargs)
        abort(403)
    return decorated
