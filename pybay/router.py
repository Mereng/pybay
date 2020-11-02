from aiohttp import web

import users
import auctions


def setup_router(app: web.Application):
    users.routes.init(app)
    auctions.routes.init(app)
