from app.features.dashboard.dashboard_opens_service import DashboardOpensService
from app.features.inventory.player.inventory_page import page
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path

from app.features.inventory.player.inventory_service import InventoryService

HEROES_COLLECTION_NAME = "metabomb_inventory_heroes"
BOXES_COLLECTION_NAME = "metabomb_inventory_boxes"


class InventoryController:
    def __init__(
        self,
        client_service: ClientService,
        inventory_service: InventoryService,
    ):
        self.client_service = client_service
        self.inventory_service = inventory_service
        self.path = 'inventory/:playerAddress'

    async def on_connect(self, sid):
        await self.client_service.emit_page(
            sid,
            self.path,
            page(HEROES_COLLECTION_NAME, BOXES_COLLECTION_NAME),
        )

    async def on_client_state_changed(self, sid, event):

        path = client_path(event)

        if not path or not path.startswith("inventory/"):
            return

        await self.client_service.emit_busy(sid, HEROES_COLLECTION_NAME)

        currency = client_currency(event)
        
        address = path.replace("inventory/", "")
        
        inventory_documents = await self.inventory_service.get_hero_documents(address, currency)

        await self.client_service.emit_documents(
            sid,
            HEROES_COLLECTION_NAME,
            inventory_documents
        )

        await self.client_service.emit_done(sid, HEROES_COLLECTION_NAME)
