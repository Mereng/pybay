from sqlalchemy.dialects.postgresql import UUID, NUMERIC

from db import DB


class Auction(DB.Model):
    __tablename__ = 'auctions'

    id = DB.Column('id', UUID, primary_key=True)
    user_id = DB.Column('user_id', UUID, DB.ForeignKey('users.id'))
    title = DB.Column('title', DB.String(150))
    description = DB.Column('description', DB.String(500))
    start_price = DB.Column('start_price', NUMERIC)
    step_price = DB.Column('step_price', NUMERIC)
    current_price = DB.Column('current_price', NUMERIC)
    end_at = DB.Column('end_time', DB.DateTime(timezone=True))
    winner_id = DB.Column('winner_id', UUID, DB.ForeignKey('users.id'), nullable=True)
    created_at = DB.Column('created_at', DB.DateTime(timezone=True))

    _user = None
    _winner = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, value):
        self._winner = value


class Bid(DB.Model):
    __tablename__ = 'bids'

    id = DB.Column('id', UUID, primary_key=True)
    auction_id = DB.Column('auction_id', UUID, DB.ForeignKey('auctions.id'))
    user_id = DB.Column('user_id', UUID, DB.ForeignKey('users.id'))
    created_at = DB.Column('created_at', DB.DateTime(timezone=True))

    _user = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value
