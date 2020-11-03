from core import email

from users.controllers import Users
from auctions import models, controllers


class NewAuction(email.Notificator):
    subject = 'Новый аукцион'

    def __init__(self, auction: models.Auction):
        self._auction = auction

    async def get_emails(self):
        return [u.email for u in await Users.get_list(exclude_users=[self._auction.user_id])]

    async def get_message(self):
        return f'Начался новый аукцион: {self._auction.title}'


class AuctionEnd(email.Notificator):
    subject = 'Аукцион завершен'

    def __init__(self, auction: models.Auction, bids: list):
        self._auction = auction
        self._bids = bids

    async def get_emails(self):
        return [b.user.email for b in self._bids]

    async def get_message(self):
        return f'Аукцион "{self._auction.title}" завершен, победитель определен.'


class NewBid(email.Notificator):
    subject = 'Новая ставка'

    def __init__(self, auction: models.Auction, bid: models.Bid):
        self._auction = auction
        self._bid = bid

    async def get_emails(self):
        return [bid.user.email for bid in await controllers.Bids.get_list_by_auction(self._auction.id)
                if self._bid.id != bid.id]

    async def get_message(self):
        return (
            f'На аукционе {self._auction.title} была произведена ставка, теперь цена этого аукциона составляет '
            f'{self._auction.current_price} рублей'
        )
