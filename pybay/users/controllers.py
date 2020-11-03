import uuid

from core import security
from users import models


class Users:
    @staticmethod
    async def register(email, password, username) -> models.User:
        u = await models.User.create(
            id=uuid.uuid4(),
            email=email,
            hash_password=security.generate_password_hash(password),
            username=username
        )
        return u

    @staticmethod
    async def get_list(**fetcher):
        q = models.User.query

        if 'exclude_users' in fetcher:
            q = q.where(~models.User.id.in_(fetcher['exclude_users']))
        return await q.gino.all()

    @staticmethod
    async def get_by_id(id):
        return await models.User.get(id)

    @staticmethod
    async def get_by_email(email) -> models.User:
        return await models.User.query.where(models.User.email == email).gino.first()

    @staticmethod
    async def get_by_username(username) -> models.User:
        return await models.User.query.where(models.User.username == username).gino.first()
