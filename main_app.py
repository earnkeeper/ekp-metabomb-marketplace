from decouple import AutoConfig
from ekp_sdk import BaseContainer

from app.features.boxes_market.boxes_summary_service import BoxesSummaryService
from app.features.boxes_market.history.boxes_history_service import \
    BoxesHistoryService
from app.features.boxes_market.listings.boxes_listings_service import \
    BoxesListingsService
from app.features.boxes_market.boxes_market_controller import BoxesMarketController
from app.features.dashboard.dashboard_controller import DashboardController
from app.features.dashboard.dashboard_opens_service import \
    DashboardOpensService
from app.features.heroes_market.heroes_market_controller import HeroesMarketController
from db.box_opens_repo import BoxOpensRepo
from db.box_ import MarketTransactionsRepo


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        # DB

        self.box_opens_repo = BoxOpensRepo(
            mg_client=self.mg_client,
        )

        self.market_transactions_repo = MarketTransactionsRepo(
            mg_client=self.mg_client,
        )

        # FEATURES - BOXES MARKET

        self.market_listings_service = BoxesListingsService(
            coingecko_service=self.coingecko_service
        )

        self.market_history_service = BoxesHistoryService(
            market_transactions_repo=self.market_transactions_repo,
            coingecko_service=self.coingecko_service
        )

        self.market_summary_service = BoxesSummaryService()

        self.boxes_market_controller = BoxesMarketController(
            client_service=self.client_service,
            boxes_listings_service=self.market_listings_service,
            boxes_history_service=self.market_history_service,
            boxes_summary_service=self.market_summary_service
        )

        # FEATURES - HEROES MARKET


        self.heroes_market_controller = HeroesMarketController(
            client_service=self.client_service,
        )
        # FEATURES - DASHBOARD

        self.dashboard_opens_service = DashboardOpensService(
            box_opens_repo=self.box_opens_repo
        )

        self.dashboard_controller = DashboardController(
            client_service=self.client_service,
            dashboard_opens_service=self.dashboard_opens_service,
        )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.boxes_market_controller)
    container.client_service.add_controller(container.dashboard_controller)
    container.client_service.add_controller(container.heroes_market_controller)

    container.client_service.listen()
