from aiohttp import web

from users import views


def init(app: web.Application):
    app.add_routes((
        web.view('/users/register', views.Register),
        web.view('/users/login', views.Login),
    ))
