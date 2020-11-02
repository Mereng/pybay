from aiohttp import web

import settings
import db
import router
import middlewares

app = web.Application()
app['config'] = settings.config

app.on_startup.append(db.init_pg)
app.on_cleanup.append(db.close_pg)

app.middlewares.append(middlewares.JWT())

router.setup_router(app)

web.run_app(app)
