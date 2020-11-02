import json
from aiohttp import web

from core import errors


def json_body(handler):
    async def wrapper(self):
        if self is None or not isinstance(self, web.View):
            raise Exception('Decorator json body must be accepted only method of class view')
        try:
            self.request["data"] = await self.request.json()
        except json.decoder.JSONDecodeError:
            raise web.HTTPBadRequest(text='invalid json')
        return await handler(self)

    return wrapper


def auth(handler):
    async def wrapper(self):
        if self is None or not isinstance(self, web.View):
            raise Exception('Decorator auth must be accepted only method of class view')
        if 'jwt' not in self.request:
            raise errors.HTTP401
        return await handler(self)

    return wrapper