from flask import request

def verify_keys():
    data = request.get_json()

    keys = ['title', 'author', 'content', 'tags']

    for key in data:
        if not key in keys:
            raise KeyError
