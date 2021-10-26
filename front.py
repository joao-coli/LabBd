import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

count = 10

@app.route('/')
def hello():
    return 'Hello World! I have been seen {} times.\n'.format(count)
