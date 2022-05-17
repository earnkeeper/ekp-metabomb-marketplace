from ekp_sdk.services import ClientService
from app.features.market.market_page import page
from app.features.market.market_service import MarketService

COLLECTION_NAME = "metabomb_listings"


class MarketController:
    def __init__(
        self,
        client_service: ClientService,
        market_service: MarketService
    ):
        self.client_service = client_service
        self.market_service = market_service
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
            page(COLLECTION_NAME)
        )

    async def on_client_state_changed(self, sid, event):
        await self.client_service.emit_busy(sid, COLLECTION_NAME)

        listings = await self.market_service.get_documents()

        await self.client_service.emit_documents(
            sid,
            COLLECTION_NAME,
            listings
        )

        await self.client_service.emit_done(sid, COLLECTION_NAME)
