from app.features.market.market_history_service import MarketHistoryService
from app.features.market.market_listings_service import MarketListingsService
from app.features.market.market_page import page
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency

LISTINGS_COLLECTION_NAME = "metabomb_market_listings"
HISTORY_COLLECTION_NAME = "metabomb_market_history"


class MarketController:
    def __init__(
        self,
        client_service: ClientService,
        market_listings_service: MarketListingsService,
        market_history_service: MarketHistoryService
    ):
        self.client_service = client_service
        self.market_listings_service = market_listings_service
        self.market_history_service = market_history_service
        self.path = 'marketplace'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'cil-cart',
            'Marketplace',
            self.path
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            page(LISTINGS_COLLECTION_NAME, HISTORY_COLLECTION_NAME)
        )

    async def on_client_state_changed(self, sid, event):
        await self.client_service.emit_busy(sid, LISTINGS_COLLECTION_NAME)
        await self.client_service.emit_busy(sid, HISTORY_COLLECTION_NAME)
        
        currency = client_currency(event)
        
        # History
        history_documents = await self.market_history_service.get_documents(currency)

        await self.client_service.emit_documents(
            sid,
            HISTORY_COLLECTION_NAME,
            history_documents
        )
        
        # Listings
        
        listing_documents = await self.market_listings_service.get_documents()

        await self.client_service.emit_documents(
            sid,
            LISTINGS_COLLECTION_NAME,
            listing_documents
        )

        await self.client_service.emit_done(sid, LISTINGS_COLLECTION_NAME)
        await self.client_service.emit_done(sid, HISTORY_COLLECTION_NAME)
