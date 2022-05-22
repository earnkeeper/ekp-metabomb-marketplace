from app.features.dashboard.dashboard_opens_service import DashboardOpensService
from app.features.dashboard.dashboard_page import page
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path

OPENS_COLLECTION_NAME = "metabomb_dashboard_opens"

class DashboardController:
    def __init__(
        self,
        client_service: ClientService,
        dashboard_opens_service: DashboardOpensService,
    ):
        self.client_service = client_service
        self.dashboard_opens_service = dashboard_opens_service
        self.path = 'dashboard'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'box',
            'Dashboard',
            self.path
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            page(OPENS_COLLECTION_NAME)
        )

    async def on_client_state_changed(self, sid, event):

        path = client_path(event)

        if (path != self.path):
            return

        await self.client_service.emit_busy(sid, OPENS_COLLECTION_NAME)

        currency = client_currency(event)

        opens_documents = await self.dashboard_opens_service.get_documents()

        await self.client_service.emit_documents(
            sid,
            OPENS_COLLECTION_NAME,
            opens_documents
        )

        await self.client_service.emit_done(sid, OPENS_COLLECTION_NAME)
