from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from app import site_frame
import json
from time import time
from datetime import datetime


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/read', methods=['GET'])
def read():
    data = []
    now = datetime.now()
    data.append(now.strftime("%S"))
    [data.append(x) for x in site_frame.data[-1]]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

