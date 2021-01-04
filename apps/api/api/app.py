from flask import Flask, request, abort, jsonify
from gevent.pywsgi import WSGIServer
from helpers import access_token_required
import config

from checkers import HttpChecker, ICMPChecker, TCPPortChecker

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


@app.route('/tcp_port')
@access_token_required
def tcp_port_check():
    target = request.args.get("target", None)
    port = int(request.args.get("port", None))

    if not target or not port:
        abort(400)

    checker = TCPPortChecker(target, port)

    return jsonify(checker.check())


@app.route('/icmp')
@access_token_required
def icmp_check():
    target = request.args.get("target", None)

    if not target:
        abort(400)

    checker = ICMPChecker(target)

    return jsonify(checker.check())


def main():
    http = WSGIServer(('', config.APP_PORT), app.wsgi_app)
    http.serve_forever()


if __name__ == '__main__':
    main()
