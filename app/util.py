from flask import Blueprint, render_template, session, request, redirect, url_for
import requests

def get(arg):
    #   GET information using Microsoft Graph
    print('GET')
    return requests.get(
        arg,
        headers={'x-api-key': '69ce5946-1ace-412e-ad5c-f654c45f70ec', 'Content-Type': 'application/json'},
    ).json()


def post(arg, fields):
    #   POST information using Microsoft Graph
    print('POST')
    return requests.post(
        arg,
        headers={'x-api-key': '69ce5946-1ace-412e-ad5c-f654c45f70ec', 'Content-Type': 'application/json'},
        json=fields,
    ).json()


def patch(arg, fields):
    #   PATCH information using Microsoft Graph
    print('PATCH')
    return requests.patch(
        arg,
        headers={'x-api-key': '69ce5946-1ace-412e-ad5c-f654c45f70ec', 'Content-Type': 'application/json'},
        json=fields,
    ).json()

