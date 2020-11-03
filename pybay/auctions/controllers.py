import uuid
import datetime

import users.models
from db import DB
from auctions import models


class Auctions:
    @staticmethod
    async def create(user_id, title, description, start_price, step_price, end_at) -> models.Auction:
        return await models.Auction.create(
            id=uuid.uuid4(),
            user_id=user_id,
            title=title,
            description=description,
            start_price=start_price,
            current_price=start_price,
            step_price=step_price,
            end_at=end_at,
            created_at=datetime.datetime.now(),
        )

    @staticmethod
    async def get_by_id(id) -> models.Auction:
        winner = users.models.User.alias()
        return (
            await models.Auction
                .load(
                    user=users.models.User.on(models.Auction.user_id == users.models.User.id),
                    winner=winner.on(models.Auction.winner_id == winner.id)
                )
                .query.where(models.Auction.id == id).gino.first()
        )

    @staticmethod
    async def get_list(**fetcher):
        q = (
            models.Auction.load(user=users.models.User.on(models.Auction.user_id == users.models.User.id)).query
                .order_by(models.Auction.created_at.desc())
        )
        if fetcher.get('active') is True:
            q = q.where(models.Auction.end_at > datetime.datetime.now())
        elif fetcher.get('active') is False:
            q = q.where(models.Auction.end_at <= datetime.datetime.now())

        if fetcher.get('winner_exists') is True:
            q = q.where(models.Auction.winner_id.isnot(None))
        elif fetcher.get('winner_exists') is False:
            q = q.where(models.Auction.winner_id.is_(None))

        if fetcher.get('limit') is not None:
            q = q.limit(fetcher['limit'])
        if fetcher.get('offset') is not None:
            q = q.offset(fetcher['offset'])

        return await q.gino.all()


class Bids:
    @staticmethod
    async def get_last(auction_id) -> models.Bid:
        return await (
            models.Bid.query.where(models.Bid.auction_id == auction_id).order_by(models.Bid.created_at.desc()).gino
                .first()
        )

    @staticmethod
    async def get_list_by_auction(auction_id) -> list:
        return await (
            models.Bid.load(user=users.models.User.on(models.Bid.user_id == users.models.User.id))
                .query.where(models.Bid.auction_id == auction_id).order_by(models.Bid.created_at.desc()).gino.all()
        )

    @staticmethod
    async def create(auction: models.Auction, user_id) -> models.Bid:
        async with DB.transaction() as tx:
            tx_auction = await (
                models.Auction.query.where(models.Auction.id == auction.id).with_for_update()
                    .gino.first()  # type models.Auction
            )
            if tx_auction.current_price != auction.current_price:
                await tx.rollback()
                raise AuctionPriceAlreadyChanged(auction)
            bid = await models.Bid.create(
                id=uuid.uuid4(),
                auction_id=auction.id,
                user_id=user_id,
                created_at=datetime.datetime.now()
            )
            await auction.update(current_price=auction.current_price + auction.step_price).apply()
            await tx.raise_commit()
        return bid


class AuctionPriceAlreadyChanged(Exception):
    def __init__(self, auction: models.Auction):
        self.auction = auction

    def __str__(self):
        return f'Auction ({self.auction.id}) price already changed'
