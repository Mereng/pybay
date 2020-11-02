import jwt
from aiohttp import web

import settings


def JWT():
    @web.middleware
    async def middleware(request: web.Request, handler):
        authorization = request.headers.get('Authorization')
        if not (authorization and authorization.startswith('Bearer ')):
            return await handler(request)

        token = authorization[7:]
        try:
            decoded = (
                jwt.decode(token, key=settings.config['jwt']['secret'], algorithms=settings.config['jwt']['algorithm'])
            )
        except jwt.InvalidTokenError:
            return await handler(request)
        request['jwt'] = decoded
        return await handler(request)

    return middleware
