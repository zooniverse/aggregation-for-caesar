from os import environ
from flask import request
from panoptes_client import Panoptes, User

def userify():
    if request.method == 'GET':
        return 'Usage'
    elif request.method == 'POST':
        find_fields = list(request.args.to_dict().keys())
        target_object = request.get_json()
        Panoptes.connect(endpoint='https://panoptes.zooniverse.org/', client_id=environ['FLASK_PANOPTES_ID'], client_secret=environ['FLASK_PANOPTES_SECRET'])
        stuff_object(target_object, find_fields)
        return str(target_object)

def stuff_object(target_object, find_fields):
    for key in target_object.keys():
        if type(target_object[key]) is dict:
            stuff_object(target_object[key], find_fields)

    if 'user_id' in target_object:
        user_id = target_object['user_id']
        user = retrieve_user(user_id)
        for key in find_fields:
            target_object[key] = user.__getattr__(key)

def retrieve_user(user_id):
    if user_id in users:
        user = users[user_id]
    else:
        user = User.find(user_id)
        users[user_id] = user

    return user

users = {}