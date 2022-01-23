from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from app import site_frame
import json
from time import time
from datetime import date


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/read', methods=['GET'])
def read():
    data = []; today = date.today()
    data.append(today.strftime("%H:%M:%S")); [data.append(x) for x in site_frame.analog_read()]
    #for x in range(4):
    #    data.append(site_frame.current_read[x])
    print(data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

