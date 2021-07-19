import quart.flask_patch

from asyncio import get_event_loop
from http import HTTPStatus
from os import getenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from flask_expects_json import expects_json
from quart import Quart, jsonify, request, send_from_directory
from rx.operators import first, to_future

from auth import requires_auth
from random_walker import RandomWalker
from schema import config_schema

load_dotenv()
app = Quart(__name__)
random_walker = RandomWalker()

@app.route('/api/test', methods = ['GET'])
def test():
    return '~(=^..^)'

@app.route('/api/config', methods = ['GET'])
def get_config():
    return random_walker.get_config()

@app.route('/api/config/future', methods = ['GET'])
async def get_future_config():
    config = await random_walker.new_config.pipe(first(), to_future())
    return config

@app.route('/api/config', methods = ['POST'])
@requires_auth
@expects_json(config_schema)
async def set_config():
    config = await request.get_json()
    random_walker.set_config(config)
    return '', HTTPStatus.NO_CONTENT

@app.route('/api/values', methods = ['GET'])
def get_values():
    return jsonify(random_walker.get_values())

@app.route('/api/values/future', methods = ['GET'])
async def get_future_values():
    value = await random_walker.new_values.pipe(first(), to_future())
    return str(value)

# this should really be moved to something more appropriate for serving static content
@app.route('/static/<path:path>', methods = ['GET'])
async def static_files(path):
    return await send_from_directory('static', path)

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func = random_walker.next, trigger = 'interval', seconds = 5)
    scheduler.start()
    loop = get_event_loop()
    loop.run_until_complete(app.run_task(host = getenv('HOST'), port = getenv('PORT')))
