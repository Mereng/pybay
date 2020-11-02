import gino

import settings

DB = gino.Gino()


async def init_pg(app):
    dsn = 'postgresql://{user}:{password}@{host}:{port}/{database}'
    await DB.set_bind(dsn.format(**settings.config['db']))
    app['db'] = DB


async def close_pg(app):
    await app['db'].pop_bind().close()


if __name__ == '__main__':
    import asyncio
    import users.models
    import auctions.models

    async def main():
        dsn = 'postgresql://{user}:{password}@{host}:{port}/{database}'
        await DB.set_bind(dsn.format(**settings.config['db']))
        await DB.gino.create_all(tables=(
            users.models.User.__table__,
            auctions.models.Auction.__table__,
            auctions.models.Bid.__table__,
        ))
        await DB.pop_bind().close()

    asyncio.get_event_loop().run_until_complete(main())
