from flask import Response, Blueprint, render_template, redirect, url_for, flash, request, session, make_response
#from flask_sse import sse
#from quart import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
import json
from time import time, sleep
from datetime import datetime
import atexit
from siteFrame import SiteFrame
import asyncio
#from flask import app


main_blueprint = Blueprint('main', __name__)


site_frame = SiteFrame()
atexit.register(lambda: site_frame.exit())


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    HTML_args = {}
    HTML_args['graphs'] = []; HTML_args['source'] = {}
    for key in site_frame.pins.keys():
        if key.split('_')[0] not in HTML_args['graphs']:
            HTML_args['graphs'].append(key.split('_')[0])
            HTML_args['source'][key.split('_')[0]] = []
        HTML_args['source'][key.split('_')[0]].append(key.split('_')[1])
        #else:
        #    HTML_args['streams'][key.split('_')[0]] += 1
    return render_template('main.html', args=HTML_args)


@main_blueprint.route('/read', methods=['GET'])
def read():
    start = time(); #site_frame.announcer.announce(site_frame.sse_dat()); print([list(q.queue) for q in site_frame.announcer.listeners])
    #if site_frame.profile_send:
    #    data = site_frame.generate_profile()
    #else:
    data = site_frame.filter_data #site_frame.pull_points()
    now = datetime.now()
    data['time'] = time() - site_frame.start_time #data.append(now.strftime("%S"))
    #[data.append(site_frame.current_read[key]) for key in site_frame.current_read.keys()]
    response = make_response(json.dumps(data)); #print(data)
    response.content_type = 'application/json'; #print(f'Request Time: {time() - start}')
    return response


@main_blueprint.route('/continuous_read', methods=['GET'])
def continuous_read():
    def stream():
        messages = site_frame.announcer.listen()
        while True:
            msg = messages.get()
            #print(msg)
            yield msg

    return Response(stream(), mimetype='text/event-stream')


#@main_blueprint.route('/SSE', methods=['GET'])
#def SSE():
#    while True:
#        sleep(0.1)
#        data = site_frame.filter_data
#        data['time'] = time() - site_frame.start_time
#        sse.publish({"reading": data}, type='reading')


#@main_blueprint.route('/profile_enable/<graph>', methods=['GET'])
#def profile_enable(graph):
#    site_frame.enable_profile(str(graph)); print(f'START: {site_frame.profile_generate}'); return '1'
    #data = site_frame.filter_data #site_frame.pull_points()
    #now = datetime.now()
    #data['time'] = now.strftime("%S") #data.append(now.strftime("%S"))
    #[data.append(site_frame.current_read[key]) for key in site_frame.current_read.keys()]
    #response = make_response(json.dumps(data)); print(data)
    #response.content_type = 'application/json'; print(f'END: {time()}')
    #return response


#@main_blueprint.route('/profile_disable', methods=['GET'])
#def profile_disable():
#    site_frame.disable_profile(); print(f'END: {site_frame.profile_generate}'); return '1'


@main_blueprint.route('/start_profiling', methods=['GET'])
def start_profiling():
    site_frame.start_time = time(); return '1'


#@main_blueprint.route('/current_profiles', methods=['GET'])
#def current_profiles():
#    data = [site_frame.current_profiles[key] for key in site_frame.current_profiles.keys()]
#    response = make_response(json.dumps(data)); #print(data)
#    response.content_type = 'application/json'; #print(f'END: {time()}')
#    return response


@main_blueprint.route('/custom_profile_settings/<id>', methods=['GET'])
def custom_profile_settings(id):
    print((site_frame.profiles.current_custom_profile(str(id).split('_')[0])));
    response = make_response(json.dumps(site_frame.profiles.current_custom_profile(str(id).split('_')[0]))); #print(data)
    response.content_type = 'application/json'; #print(f'END: {time()}')
    return response


#@main_blueprint.route('/profile_change/<graph>/<source>/<id>/<X>', methods=['GET'])
#@main_blueprint.route('/profile_change/<graph>/<source>/<id>', methods=['GET'])
#def profile_change(graph, source, id, X=-1000):
#    if X != -1000:
#        site_frame.profile_generate[id] = X; #print(site_frame.profile_generate)
#    for key in site_frame.current_profiles.keys():
#        if str(graph) in key:
#            if str(source) in key:
#                site_frame.current_profiles[key] = str(id)
#    return '1'


#@main_blueprint.route('/live_graph')
#def live_graph():
#    HTML_args = {}
#    HTML_args['graphs'] = []; HTML_args['source'] = {}
#    for key in site_frame.pins.keys():
#        if key.split('_')[0] not in HTML_args['graphs']:
#            HTML_args['graphs'].append(key.split('_')[0])
#            HTML_args['source'][key.split('_')[0]] = []
#        HTML_args['source'][key.split('_')[0]].append(key.split('_')[1])
#        #else:
 #       #    HTML_args['streams'][key.split('_')[0]] += 1
 #   return render_template('live_graph.html', args=HTML_args)


@main_blueprint.route('/current_custom_profiling/<graph>/<source>', methods=['GET'])
def current_custom_profiling(graph, source):
    response = make_response(json.dumps(site_frame.profiles.current_custom_profile(str(graph),str(source)))); #print(data)
    response.content_type = 'application/json'; #print(f'END: {time()}')
    return response


@main_blueprint.route('/submit_custom_profile/<graph>/<xdat>/<ydat>', methods=['GET'])
def submit_custom_profile(graph, xdat, ydat):
    keys = []
    for key in site_frame.profiles.custom_profiles[str(graph)].keys():
        keys.append(key)
    for idx in range(len(keys)):
        xdata = [float(x) for x in str(xdat).split('|')[idx].split(',') if x]
        ydata = [float(y) for y in str(ydat).split('|')[idx].split(',') if y]
        site_frame.profiles.custom_profiles[str(graph)][keys[idx]] = [xdata,ydata]
    return '1'


@main_blueprint.route('/revert_custom_profile/<graph>', methods=['GET'])
def revert_custom_profile(graph):
    site_frame.profiles.custom_profiles[str(graph)] = site_frame.profiles.backup_profiles[str(graph)]
    return '1'


@main_blueprint.route('/save_custom_profile/<name>/<graph>', methods=['GET'])
def save_custom_profile(name, graph):
    site_frame.profiles.save_current_profiles(str(graph), str(name))
    return '1'


@main_blueprint.route('/get_profile_options/<graph>', methods=['GET'])
def get_profile_options(graph):
    result = {}
    for key in site_frame.profiles.all_profiles.keys():
        if str(graph) in site_frame.profiles.all_profiles[key]['graph']:
            result[key] = key
    return result


@main_blueprint.route('/switch_profile_option/<name>', methods=['GET'])
def switch_profile_options(name):
    site_frame.profiles.set_base(str(name)); return '1'


