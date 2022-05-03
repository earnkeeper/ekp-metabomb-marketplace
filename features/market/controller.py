from features.market.documents import documents
from features.market.page import page

listings_collection_name = "metabomb_listings"

class MarketController:
    def __init__(self, client_service):
        self.client_service = client_service
        self.path = 'marketplace'

    def on_connect(self, sid):
        self.client_service.emit_menu(
            sid,
            'cil-cart',
            'Marketplace',
            self.path
        )
        self.client_service.emit_page(
            sid,
            self.path,
            page(listings_collection_name)
        )

    def on_client_state_changed(self, sid, event):
        self.client_service.emit_busy(sid, listings_collection_name)

        listings = documents()

        self.client_service.emit_documents(
            sid,
            listings_collection_name,
            listings
        )

        self.client_service.emit_done(sid, listings_collection_name)
