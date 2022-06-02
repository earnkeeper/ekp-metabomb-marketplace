from pprint import pprint
from app.features.dashboard.dashboard_activity_service import DashboardActivityService
from app.features.dashboard.dashboard_fusion_service import DashboardFusionService
from app.features.dashboard.dashboard_opens_service import DashboardOpensService
from app.features.dashboard.dashboard_page import page
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path

OPENS_COLLECTION_NAME = "metabomb_dashboard_opens"
ACTIVITY_COLLECTION_NAME = "metabomb_dashboard_activity"
FUSION_COLLECTION_NAME = "metabomb_dashboard_fusion"

class DashboardController:
    def __init__(
        self,
        client_service: ClientService,
        dashboard_activity_service: DashboardActivityService,
        dashboard_opens_service: DashboardOpensService,
        dashboard_fusion_service: DashboardFusionService,
    ):
        self.client_service = client_service
        self.dashboard_activity_service = dashboard_activity_service
        self.dashboard_opens_service = dashboard_opens_service
        self.dashboard_fusion_service = dashboard_fusion_service
        self.path = 'dashboard'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'activity',
            'Dashboard',
            self.path,
            order=100,
            id="metabomb_dashboard"            
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            page(OPENS_COLLECTION_NAME, ACTIVITY_COLLECTION_NAME, FUSION_COLLECTION_NAME),
        )

    async def on_client_state_changed(self, sid, event):

        path = client_path(event)

        if (path != self.path):
            return

        await self.client_service.emit_busy(sid, OPENS_COLLECTION_NAME)
        await self.client_service.emit_busy(sid, FUSION_COLLECTION_NAME)

        currency = client_currency(event)

        # ----------------------------------------------------------------------
        
        opens_documents = await self.dashboard_opens_service.get_documents()

        await self.client_service.emit_documents(
            sid,
            OPENS_COLLECTION_NAME,
            opens_documents
        )
        
        # ----------------------------------------------------------------------

        activity_documents = self.dashboard_activity_service.get_documents()

        await self.client_service.emit_documents(
            sid,
            ACTIVITY_COLLECTION_NAME,
            activity_documents
        )
        
        # ----------------------------------------------------------------------

        fusion_documents = await self.dashboard_fusion_service.get_documents(currency)

        await self.client_service.emit_documents(
            sid,
            FUSION_COLLECTION_NAME,
            fusion_documents
        )

        await self.client_service.emit_done(sid, OPENS_COLLECTION_NAME)
        await self.client_service.emit_done(sid, FUSION_COLLECTION_NAME)
