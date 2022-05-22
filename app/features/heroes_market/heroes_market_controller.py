from app.features.boxes_market.boxes_page import boxes_page
from app.features.boxes_market.boxes_summary_service import BoxesSummaryService
from app.features.boxes_market.history.boxes_history_service import \
    BoxesHistoryService
from app.features.boxes_market.listings.boxes_listings_service import \
    BoxesListingsService
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path

from app.features.heroes_market.heroes_page import heroes_page

HERO_LISTINGS_COLLECTION_NAME = "metabomb_hero_listings"
HERO_HISTORY_COLLECTION_NAME = "metabomb_hero_history"
HERO_SUMMARY_COLLECTION_NAME = "metabomb_hero_summary"


class HeroesMarketController:
    def __init__(
        self,
        client_service: ClientService,
    ):
        self.client_service = client_service
        self.path = 'heroes'
        self.short_link = 'metabomb-hero-market'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'cil-cart',
            'Hero Market',
            self.path,
            short_link=self.short_link
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            heroes_page(
                
            )
        )

    async def on_client_state_changed(self, sid, event):
        pass