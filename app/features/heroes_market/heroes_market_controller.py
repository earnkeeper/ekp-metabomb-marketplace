from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path

from app.features.heroes_market.heroes_page import heroes_page
from app.features.heroes_market.history.heroes_history_service import HeroesHistoryService
from app.features.heroes_market.listings.heroes_listings_service import HeroListingsService

HERO_LISTINGS_COLLECTION_NAME = "metabomb_hero_listings"
HERO_HISTORY_COLLECTION_NAME = "metabomb_hero_history"
HERO_SUMMARY_COLLECTION_NAME = "metabomb_hero_summary"


class HeroesMarketController:
    def __init__(
        self,
        client_service: ClientService,
        heroes_history_service: HeroesHistoryService,
        heroes_listings_service: HeroListingsService,
    ):
        self.client_service = client_service
        self.heroes_history_service = heroes_history_service
        self.heroes_listings_service = heroes_listings_service
        self.path = 'heroes'
        self.short_link = 'metabomb-hero-market'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'shopping-bag',
            'Hero Market',
            self.path,
            short_link=self.short_link,
            order=200,
            id="metabomb_hero_market"
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            heroes_page(
                HERO_HISTORY_COLLECTION_NAME,
                HERO_LISTINGS_COLLECTION_NAME
            )
        )

    async def on_client_state_changed(self, sid, event):
        path = client_path(event)

        if (path != self.path):
            return

        await self.client_service.emit_busy(sid, HERO_HISTORY_COLLECTION_NAME)
        await self.client_service.emit_busy(sid, HERO_LISTINGS_COLLECTION_NAME)

        currency = client_currency(event)


        # History
        history_documents = await self.heroes_history_service.get_documents(currency)

        await self.client_service.emit_documents(
            sid,
            HERO_HISTORY_COLLECTION_NAME,
            history_documents
        )

        # Listings

        listing_documents = await self.heroes_listings_service.get_documents(currency, history_documents)

        await self.client_service.emit_documents(
            sid,
            HERO_LISTINGS_COLLECTION_NAME,
            listing_documents
        )


        await self.client_service.emit_done(sid, HERO_HISTORY_COLLECTION_NAME)
        await self.client_service.emit_done(sid, HERO_LISTINGS_COLLECTION_NAME)