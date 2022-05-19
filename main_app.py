from decouple import AutoConfig
from ekp_sdk import BaseContainer

from app.features.market.market_controller import MarketController
from app.features.market.market_history_service import MarketHistoryService
from app.features.market.market_listings_service import MarketListingsService
from db.market_transactions_repo import MarketTransactionsRepo


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        # DB

        self.market_transactions_repo = MarketTransactionsRepo(
            mg_client=self.mg_client,
        )

        # FEATURES - MARKET

        self.market_listings_service = MarketListingsService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service
        )

        self.market_history_service = MarketHistoryService(
            market_transactions_repo=self.market_transactions_repo,
            coingecko_service=self.coingecko_service
        )

        self.market_controller = MarketController(
            client_service=self.client_service,
            market_listings_service=self.market_listings_service,
            market_history_service=self.market_history_service
        )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.market_controller)

    container.client_service.listen()
