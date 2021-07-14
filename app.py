from http import HTTPStatus

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, g, jsonify, send_from_directory
from flask_expects_json import expects_json

from random_walker import RandomWalker

app = Flask(__name__)
random_walker = RandomWalker()

@app.route('/api/test', methods = ['GET'])
def test():
    return '~(=^..^)'

@app.route('/api/values', methods = ['GET'])
def get_values():
    return jsonify(random_walker.get_values())

@app.route('/api/config', methods = ['GET'])
def get_config():
    return random_walker.get_config()

@app.route('/api/config', methods = ['POST'])
@expects_json({
    'type': 'object',
    'properties': {
        'skew': { 'type': 'number' },
        'volatility': { 'type': 'number' },
        'minimum': { 'type': 'number' },
        'target_price': { 'type': 'number' }
    },
    'required': []
})
def set_config():
    random_walker.set_config(g.data)
    return ('', HTTPStatus.NO_CONTENT)

# this should really be moved to something more appropriate for serving static content
@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func = random_walker.next, trigger = 'interval', seconds = 5)
    scheduler.start()
    app.run(host = '127.0.0.1', port = 5000)
