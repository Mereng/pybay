import datetime
from aiohttp import web

from core import decorators, errors, tools
from auctions import controllers


class Auctions(web.View):
    def proccess_data(self, data):
        errors_fields = {}

        title = data.get('title')
        if not title or len(title) > 150:
            errors_fields['title'] = 'Title is required and must be less than 150 characters'

        description = data.get("description")
        if description and len(description) > 500:
            errors_fields['title'] = 'Description must be less than 500 characters'

        start_price = data.get('start_price')
        if start_price:
            if not isinstance(start_price, int) and not isinstance(start_price, float):
                errors_fields['start_price'] = 'Incorrect value'
        else:
            errors_fields['start_price'] = 'Start price is required'

        step_price = data.get('step_price')
        if step_price:
            if not isinstance(step_price, int) and not isinstance(step_price, float):
                errors_fields['step_price'] = 'Incorrect value'
        else:
            errors_fields['step_price'] = 'Step price is required'

        end_at = data.get('end_at')
        if end_at:
            try:
                end_at = datetime.datetime.fromisoformat(end_at)
                if end_at.replace(tzinfo=None) < datetime.datetime.now():
                    errors_fields['end_at'] = 'End date must be more than current date'
                data['end_at'] = end_at
            except ValueError:
                errors_fields['end_at'] = 'Invalid format, mast be ISO'
        else:
            errors_fields['end_at'] = '"End at" is required'

        if errors_fields:
            raise errors.HTTP400Fields(errors_fields)

        return data

    @decorators.auth
    @decorators.json_body
    async def post(self):
        data = self.proccess_data(self.request['data'].copy())

        auction = await controllers.Auctions.create(
            self.request['jwt']['user_id'],
            data['title'],
            data['description'],
            data['start_price'],
            data['step_price'],
            data['end_at'],
        )
        return web.json_response({
            'id': str(auction.id),
            'user_id': str(auction.user_id),
            'title': auction.title,
            'description': auction.description,
            'start_price': float(auction.start_price),
            'step_price': float(auction.step_price),
            'current_price': float(auction.current_price),
            'end_at': auction.end_at.isoformat(),
            'created_at': auction.created_at.isoformat(),
        })

    @decorators.auth
    async def get(self):
        data = self.request.query
        limit, offset = tools.limit_offset(data, 50)

        auctions = await controllers.Auctions.get_list(
            active=tools.strbool(data.get('active')),
            limit=limit,
            offset=offset,
        )

        items = [{
            'id': str(a.id),
            'user': {
                'id': str(a.user.id),
                'username': a.user.username,
            },
            'title': a.title,
            'start_price': float(a.start_price),
            'step_price': float(a.step_price),
            'current_price': float(a.current_price),
            'end_at': a.end_at.isoformat(),
            'created_at': a.created_at.isoformat(),
        } for a in auctions]
        return web.json_response({
            'items': items,
            'limit': limit,
            'offset': offset,
            'count': len(items),
        })


class Auction(web.View):
    @decorators.auth
    async def get(self):
        auction_id = self.request.match_info['auction_id']
        auction = await controllers.Auctions.get_by_id(auction_id)
        if not auction:
            raise errors.HTTP404('Auction not found')
        bids = await controllers.Bids.get_list_by_auction(auction.id)

        bids_items = [{
            'id': str(b.id),
            'created_at': b.created_at.isoformat(),
            'user': {
                'id': str(b.user.id),
                'username': b.user.username,
            },
        } for b in bids]

        return web.json_response({
            'id': str(auction.id),
            'user_id': str(auction.user_id),
            'title': auction.title,
            'description': auction.description,
            'start_price': float(auction.start_price),
            'step_price': float(auction.step_price),
            'current_price': float(auction.current_price),
            'end_at': auction.end_at.isoformat(),
            'created_at': auction.created_at.isoformat(),
            'bids': bids_items,
        })


class Bids(web.View):
    @decorators.auth
    async def post(self):
        auction_id = self.request.match_info['auction_id']
        auction = await controllers.Auctions.get_by_id(auction_id)
        if not auction:
            raise errors.HTTP404('Auction not found')
        user_id = self.request['jwt']['user_id']
        if str(auction.user_id) == user_id:
            raise errors.HTTP403('You cannot made bid on your lot')
        if auction.end_at.replace(tzinfo=None) < datetime.datetime.now():
            raise errors.HTTP403('Auction is ended')
        last_bid = await controllers.Bids.get_last(auction_id)
        if last_bid and last_bid.user_id == user_id:
            raise errors.HTTP403('You already made a bed')
        try:
            bid = await controllers.Bids.create(auction, user_id)
        except controllers.AuctionPriceAlreadyChanged:
            raise errors.HTTP409('Price of auction changed, try again')

        return web.json_response({
            'id': str(bid.id),
            'auction_id': auction_id,
            'created_at': bid.created_at.isoformat()
        })
