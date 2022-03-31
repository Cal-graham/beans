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
    #print(f'START: {time()}')
    if site_frame.profile_send:
        data = site_frame.generate_profile()
    else:
        data = site_frame.filter_data #site_frame.pull_points()
    now = datetime.now()
    data['time'] = now.strftime("%S") #data.append(now.strftime("%S"))
    #[data.append(site_frame.current_read[key]) for key in site_frame.current_read.keys()]
    response = make_response(json.dumps(data)); #print(data)
    response.content_type = 'application/json'; #print(f'END: {time()}')
    return response


@main_blueprint.route('/profile_enable/<type>', methods=['GET'])
def profile_enable(type):
    site_frame.enable_profile(str(type)); print(f'START: {site_frame.profile_generate}'); return '1'
    #data = site_frame.filter_data #site_frame.pull_points()
    #now = datetime.now()
    #data['time'] = now.strftime("%S") #data.append(now.strftime("%S"))
    #[data.append(site_frame.current_read[key]) for key in site_frame.current_read.keys()]
    #response = make_response(json.dumps(data)); print(data)
    #response.content_type = 'application/json'; print(f'END: {time()}')
    #return response


@main_blueprint.route('/profile_disable', methods=['GET'])
def profile_disable():
    site_frame.disable_profile(); print(f'END: {site_frame.profile_generate}'); return '1'


@main_blueprint.route('/profile_start', methods=['GET'])
def profile_start():
    site_frame.start_profile(); print(f'START: {site_frame.profile_generate}'); return '1'


@main_blueprint.route('/profile_settings/<type>', methods=['GET'])
def profile_settings(type):
    response = make_response(json.dumps(site_frame.pull_profile_settings(str(type)))); #print(data)
    response.content_type = 'application/json'; #print(f'END: {time()}')
    return response

