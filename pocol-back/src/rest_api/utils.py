from flask import request


class ParamNotFound(Exception): pass


def getRequestParam(name, default=None, type=str):
    if name not in request.args:
        if default != None:
            return default
        else:
            raise ParamNotFound
    return request.args.get(name, type=type)
