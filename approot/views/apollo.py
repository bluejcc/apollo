import pprint
import json
import os
import re

from flask import Blueprint
from flask import request, render_template, send_file
from flask.ext.classy import FlaskView
from flask import current_app as app

pp = pprint.PrettyPrinter(indent=4)


bp_apollo = Blueprint('apollo', __name__)


class Apollo(FlaskView):
    route_base = '/'

    def index(self):
        ctx = {}
        return render_template('generator.html', **ctx)


class ApolloApi(FlaskView):
    route_base = '/gen_midi/'

    def get(self):
        file_name = 'a.mid'
        return send_file(os.path.join(app.config['AUDIO_DIR'], file_name), as_attachment=True)


Apollo.register(bp_apollo)
ApolloApi.register(bp_apollo)
