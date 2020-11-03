import datetime
import time
import asyncio

from auctions.controllers import Auctions, Bids
from auctions.notify import AuctionEnd


class CheckEndedAuction:
    async def _check(self):
        print('Start check ended auction')
        auctions = await Auctions.get_list(active=False, winner_exists=False)
        print(f'Loaded {len(auctions)} auctions')
        for a in auctions:
            bids = await Bids.get_list_by_auction(a.id)
            if bids:
                await a.update(winner_id=bids[0].user_id).apply()
                AuctionEnd(a, bids).send()

    def start(self, args):
        loop = asyncio.get_event_loop()
        while True:
            try:
                loop.run_until_complete(self._check())
                time.sleep(1)
            except KeyboardInterrupt:
                return


if __name__ == '__main__':
    import argparse

    import db

    loop = asyncio.get_event_loop()
    app = {}
    loop.run_until_complete(db.init_pg(app))

    parser = argparse.ArgumentParser(description="CLI workers and helpers")
    subparsers = parser.add_subparsers(help='commands')

    check_end_auctions = subparsers.add_parser('run_check_end_auctions', help='Start check end auctions worker')
    check_end_auctions.set_defaults(func=CheckEndedAuction().start)
    args = parser.parse_args()
    args.func(args)

    loop.run_until_complete(db.close_pg(app))
