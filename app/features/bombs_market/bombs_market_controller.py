from pprint import pprint

from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path

from app.features.bombs_market.bombs_page import bombs_page
from app.features.bombs_market.bombs_summary_service import BombsSummaryService
from app.features.bombs_market.history.bombs_history_service import BombsHistoryService
from app.features.bombs_market.listings.bombs_listings_service import BombsListingsService

BOMBS_LISTINGS_COLLECTION_NAME = "metabomb_bomb_listings"
BOMBS_HISTORY_COLLECTION_NAME = "metabomb_bomb_history"
BOMBS_SUMMARY_COLLECTION_NAME = "metabomb_bomb_summary"


class HeroesMarketController:
    def __init__(
            self,
            client_service: ClientService,
            bombs_history_service: BombsHistoryService,
            bombs_listings_service: BombsListingsService,
            bombs_summary_service: BombsSummaryService,
    ):
        self.client_service = client_service
        self.bombs_history_service = bombs_history_service
        self.bombs_listings_service = bombs_listings_service
        self.bombs_summary_service = bombs_summary_service
        self.path = 'bombs'
        self.short_link = 'mtb-market'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'shopping-bag',
            'Bomb Market',
            self.path,
            short_link=self.short_link,
            order=200,
            id="metabomb_bomb_market"
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            bombs_page(
                BOMBS_HISTORY_COLLECTION_NAME,
                BOMBS_LISTINGS_COLLECTION_NAME,
                BOMBS_SUMMARY_COLLECTION_NAME
            )
        )

    async def on_client_state_changed(self, sid, event):
        path = client_path(event)

        if (path != self.path):
            return

        # await self.client_service.emit_busy(sid, BOMBS_HISTORY_COLLECTION_NAME)
        # await self.client_service.emit_busy(sid, BOMBS_LISTINGS_COLLECTION_NAME)
        await self.client_service.emit_busy(sid, BOMBS_SUMMARY_COLLECTION_NAME)

        currency = client_currency(event)

        # History
        # history_documents = await self.heroes_history_service.get_documents(currency)
        #
        # await self.client_service.emit_documents(
        #     sid,
        #     BOMBS_HISTORY_COLLECTION_NAME,
        #     history_documents
        # )

        # Listings

        # listing_documents = await self.heroes_listings_service.get_documents(currency, history_documents)
        # # pprint(listing_documents)
        #
        # await self.client_service.emit_documents(
        #     sid,
        #     BOMBS_LISTINGS_COLLECTION_NAME,
        #     listing_documents
        # )

        summary_documents = self.heroes_summary_service.get_documents(
            listing_documents, history_documents, currency
        )

        await self.client_service.emit_documents(
            sid,
            BOMBS_SUMMARY_COLLECTION_NAME,
            summary_documents
        )

        # await self.client_service.emit_done(sid, BOMBS_HISTORY_COLLECTION_NAME)
        # await self.client_service.emit_done(sid, BOMBS_LISTINGS_COLLECTION_NAME)
        await self.client_service.emit_done(sid, BOMBS_SUMMARY_COLLECTION_NAME)
