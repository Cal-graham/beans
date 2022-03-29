from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
import json
from time import time
from datetime import datetime
import atexit
from siteFrame import SiteFrame
#from flask import app


main_blueprint = Blueprint('main', __name__)


site_frame = SiteFrame()
atexit.register(lambda: site_frame.exit())


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    HTML_args = {}
    HTML_args['graphs'] = [] #; HTML_args['streams'] = {}
    for key in site_frame.pins.keys():
        if key.split('_')[0] not in HTML_args['graphs']:
            HTML_args['graphs'].append(key.split('_')[0]) #; HTML_args['streams'][key.split('_')[0]] = 0
        #else:
        #    HTML_args['streams'][key.split('_')[0]] += 1
    return render_template('main.html', args=HTML_args)


@main_blueprint.route('/read', methods=['GET'])
def read():
    print(f'START: {time()}')
    data = site_frame.filter_data #site_frame.pull_points()
    now = datetime.now()
    data['time'] = now.strftime("%S") #data.append(now.strftime("%S"))
    #[data.append(site_frame.current_read[key]) for key in site_frame.current_read.keys()]
    response = make_response(json.dumps(data)); print(data)
    response.content_type = 'application/json'; print(f'END: {time()}')
    return response

