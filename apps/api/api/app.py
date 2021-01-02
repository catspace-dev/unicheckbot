from flask import Flask, request, abort, jsonify
from gevent.pywsgi import WSGIServer
from gevent import monkey
from helpers import access_token_required
import config

monkey.patch_all()
# Monkey patch SSL in requests to prevent RecursionError! DO NOT REMOVE OR MOVE!
from checkers.http import HttpChecker

app = Flask(__name__)


@app.route('/http')
@access_token_required
def http_check():
    target = request.args.get("target", None)
    port = int(request.args.get("port", 80))

    if not target:
        abort(400)

    checker = HttpChecker(target, port)

    return jsonify(checker.check())


def main():
    http = WSGIServer(('', config.APP_PORT), app.wsgi_app)
    http.serve_forever()


if __name__ == '__main__':
    main()
