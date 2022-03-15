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


@main_blueprint.route('/read', methods=['GET'])
def read():
    data = site_frame.pull_points() #[]
    now = datetime.now()
    data['time'] = now.strftime("%S") #data.append(now.strftime("%S"))
    #[data.append(site_frame.current_read[key]) for key in site_frame.current_read.keys()]
    response = make_response(json.dumps(data)); print(data)
    response.content_type = 'application/json'
    return response

