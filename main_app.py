from decouple import AutoConfig
from ekp_sdk import BaseContainer

from app.features.market.market_controller import MarketController
from app.features.market.market_service import MarketService
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

        self.market_service = MarketService(
            cache_service=self.cache_service,
        )

        self.market_controller = MarketController(
            client_service=self.client_service,
            market_service=self.market_service
        )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.market_controller)

    container.client_service.listen()
