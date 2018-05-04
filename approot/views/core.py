from flask import current_app, Blueprint
from flask import render_template
from flask.ext.classy import FlaskView


bp_core = Blueprint('core', __name__)


class Root(FlaskView):
    route_base = '/fakeroot/'

    def index(self):
        return render_template('root.html')


Root.register(bp_core)
