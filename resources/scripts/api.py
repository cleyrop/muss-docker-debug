from ast import arg
from plistlib import load
from flask import Flask, request, jsonify, g as app_ctx

import logging
import time
from markupsafe import escape

from muss.simplify import init_simplifier, simplify_sentences
from muss.utils.helpers import read_lines

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.before_request
def logging_before():
    app_ctx.start_time = time.perf_counter()


@app.after_request
def logging_after(response):
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response

@app.route('/healthcheck', methods=['GET'])
def health_check():
    return 'alive'

@app.route('/muss/<string:input>/<string:model>', methods=['GET'])
def muss(input, model):
    try:
        app.logger.info(f'simplify sentences for {escape(input)}')
        text = read_lines(f'{escape(input)}')
        result = simplify_sentences(text, model_name=model)
        return jsonify(result)
    except:
        return jsonify([])

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.access')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.logger.info('Loading the model...')
    init_simplifier('muss_fr_mined')
    app.logger.info('Model loaded.')

    app.logger.info('Simplifying a sentence...')
    simplify_sentences('Il fait un temps radieux.', model_name='muss_fr_mined')
    app.logger.info('Sentence simplified.')
