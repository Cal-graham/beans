from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
import site_frame
import json
from time import time
from datetime import datetime


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/read', methods=['GET'])
def read():
    data = []
    now = datetime.now()
    data.append(now.strftime("%S"))
    [data.append(site_frame.current_read[key]) for key in site_frame.current_read.keys()]
    response = make_response(json.dumps(data)); print(data)
    response.content_type = 'application/json'
    return response

