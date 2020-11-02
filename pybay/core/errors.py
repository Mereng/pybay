import json

from aiohttp import web


class HTTP401(web.HTTPUnauthorized):
    def __init__(self):
        super().__init__(text=json.dumps({'message': 'Authorization is required'}), content_type='application/json')


class HTTP403(web.HTTPForbidden):
    def __init__(self, message=None):
        if message:
            text = message
        else:
            text = "Access is forbidden"
        super().__init__(text=json.dumps({'message': text}), content_type='application/json')


class HTTP404(web.HTTPForbidden):
    def __init__(self, message=None):
        if message:
            text = message
        else:
            text = 'Item not found'
        super().__init__(text=json.dumps({'message': text}), content_type='application/json')


class HTTP409(web.HTTPConflict):
    def __init__(self, message=None):
        if message:
            text = json.dumps({'message': message})
        else:
            text = None
        super().__init__(text=text, content_type='application/json')


class HTTP400Fields(web.HTTPBadRequest):
    def __init__(self, fields_messages: dict):
        super().__init__(
            text=json.dumps({'message': 'fields is invalid', 'fields': fields_messages}),
            content_type='application/json',
        )

