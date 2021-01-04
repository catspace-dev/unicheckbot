from gevent import monkey
monkey.patch_all()

from api.app import app
