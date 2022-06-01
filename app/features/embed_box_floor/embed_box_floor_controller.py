from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency

from app.features.embed_box_floor.embed_box_floor_tile import tile

OPENS_COLLECTION_NAME = "metabomb_dashboard_opens"
ACTIVITY_COLLECTION_NAME = "metabomb_dashboard_activity"

class EmbedBoxFloorController:
    def __init__(
        self,
        client_service: ClientService,
    ):
        self.client_service = client_service

    async def on_connect(self, sid):
        pass


    async def on_client_state_changed(self, sid, event):
        
        currency = client_currency(event)

        documents = [{
            "id": 'metabomb-box-tile',
            "size": 'tile',
            "element": tile(),
            "data": [],
            "page": 'boxes',            
        }]
        
        await self.client_service.emit_documents(
            sid,
            "embeds",
            documents
        )
        
