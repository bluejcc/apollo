import pprint
import json
import os
import re

from flask import Blueprint
from flask import request, render_template, send_file
from flask.ext.classy import FlaskView
from flask import current_app as app

from approot.generators import MusicGenerator

pp = pprint.PrettyPrinter(indent=4)


bp_apollo = Blueprint('apollo', __name__)


class Apollo(FlaskView):
    route_base = '/'

    def index(self):
        ctx = {}
        return render_template('generator.html', **ctx)


class ApolloApi(FlaskView):
    route_base = '/generate/<format_type>'
    generator = MusicGenerator()

    def get(self, format_type):
        chords = request.args.get('chords')
        chords = chords.replace('+',' ')
        self.generator.set_audio_dir(os.path.join('approot',
                                                  app.config['AUDIO_DIR']))
        self.generator.set_cfg({'chord_list': chords})
        if format_type == 'mid':
            file_name = 'output.mid'
            self.generator.get_mid(file_name)
            return send_file(os.path.join(app.config['AUDIO_DIR'],
                                          file_name), as_attachment=True)
        if format_type == 'musicxml':
            return self.generator.get_xml()
        app.logger.warning(
            'Request with unknown format_type: {}'.format(format_type))
        return None


Apollo.register(bp_apollo)
ApolloApi.register(bp_apollo)
