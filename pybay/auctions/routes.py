from aiohttp import web

from auctions import views


def init(app: web.Application):
    app.add_routes((
        web.view('/auctions', views.Auctions),
        web.view('/auctions/{auction_id}', views.Auction),
        web.view('/auctions/{auction_id}/bids', views.Bids),
    ))
