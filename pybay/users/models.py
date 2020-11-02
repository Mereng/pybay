from sqlalchemy.dialects.postgresql import UUID

from db import DB


class User(DB.Model):
    __tablename__ = 'users'

    id = DB.Column('id', UUID, primary_key=True)
    email = DB.Column('email', DB.String, unique=True, nullable=False)
    hash_password = DB.Column('hash_password', DB.String, nullable=False)
    username = DB.Column('username', DB.String(20), unique=True, nullable=False)
