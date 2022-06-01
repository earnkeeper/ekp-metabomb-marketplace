from decouple import AutoConfig
from ekp_sdk import BaseContainer

from app.features.boxes_market.boxes_summary_service import BoxesSummaryService
from app.features.boxes_market.history.boxes_history_service import \
    BoxesHistoryService
from app.features.boxes_market.listings.boxes_listings_service import \
    BoxesListingsService
from app.features.boxes_market.boxes_market_controller import BoxesMarketController
from app.features.dashboard.dashboard_activity_service import DashboardActivityService
from app.features.dashboard.dashboard_controller import DashboardController
from app.features.dashboard.dashboard_opens_service import \
    DashboardOpensService
from app.features.heroes_market.heroes_market_controller import HeroesMarketController
from app.features.heroes_market.history.heroes_history_service import HeroesHistoryService
from app.features.heroes_market.listings.heroes_listings_service import HeroListingsService
from app.features.inventory.player.inventory_controller import InventoryController
from app.features.inventory.player.inventory_service import InventoryService
from app.features.inventory.players.players_controller import InventoryPlayersController
from app.features.inventory.players.players_service import InventoryPlayersService
from app.features.heroes_market.heroes_summary_service import HeroesSummaryService
from db.activity_repo import ActivityRepo
from db.box_opens_repo import BoxOpensRepo
from db.market_sales_repo import MarketSalesRepo
from db.hero_listing_timestamp_repo import HeroListingTimestampRepo
from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService
from shared.metabomb_coingecko_service import MetabombCoingeckoService
from shared.metabomb_moralis_service import MetabombMoralisService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        self.metabomb_api_service = MetabombApiService(
            cache_service=self.cache_service
        )

        self.mapper_service = MapperService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
        )
        
        self.metabomb_moralis_service = MetabombMoralisService(
            cache_service=self.cache_service,
            moralis_api_service=self.moralis_api_service
        )

        self.metabomb_coingecko_service = MetabombCoingeckoService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service
        )

        # DB

        self.activity_repo = ActivityRepo(
            mg_client=self.mg_client,
        )

        self.box_opens_repo = BoxOpensRepo(
            mg_client=self.mg_client,
        )

        self.market_sales_repo = MarketSalesRepo(
            mg_client=self.mg_client,
        )

        self.hero_listing_timestamp_repo = HeroListingTimestampRepo(
            mg_client=self.mg_client
        )

        # FEATURES - BOXES MARKET

        self.boxes_listings_service = BoxesListingsService(
            coingecko_service=self.coingecko_service
        )

        self.boxes_history_service = BoxesHistoryService(
            market_sales_repo=self.market_sales_repo,
            coingecko_service=self.coingecko_service
        )

        self.market_summary_service = BoxesSummaryService()

        self.boxes_market_controller = BoxesMarketController(
            client_service=self.client_service,
            boxes_listings_service=self.boxes_listings_service,
            boxes_history_service=self.boxes_history_service,
            boxes_summary_service=self.market_summary_service
        )

        # FEATURES - HEROES MARKET

        self.heroes_listings_service = HeroListingsService(
            coingecko_service=self.coingecko_service,
            metabomb_api_service=self.metabomb_api_service,
            mapper_service=self.mapper_service,
            hero_listing_timestamp_repo=self.hero_listing_timestamp_repo
        )

        self.heroes_history_service = HeroesHistoryService(
            market_sales_repo=self.market_sales_repo,
            coingecko_service=self.coingecko_service,
            mapper_service=self.mapper_service
        )

        self.heroes_summary_service = HeroesSummaryService()

        self.heroes_market_controller = HeroesMarketController(
            client_service=self.client_service,
            heroes_history_service=self.heroes_history_service,
            heroes_listings_service=self.heroes_listings_service,
            heroes_summary_service=self.heroes_summary_service
        )

        # FEATURES - DASHBOARD

        self.dashboard_opens_service = DashboardOpensService(
            box_opens_repo=self.box_opens_repo
        )

        self.dashboard_activity_service = DashboardActivityService(
            activity_repo=self.activity_repo
        )

        self.dashboard_controller = DashboardController(
            client_service=self.client_service,
            dashboard_activity_service=self.dashboard_activity_service,
            dashboard_opens_service=self.dashboard_opens_service,
        )

        # FEATURES - INVENTORY - PLAYERS

        self.inventory_players_service = InventoryPlayersService(
            metabomb_api_service=self.metabomb_api_service,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            metabomb_moralis_service=self.metabomb_moralis_service,
            mapper_service=self.mapper_service
        )

        self.inventory_players_controller = InventoryPlayersController(
            client_service=self.client_service,
            inventory_players_service=self.inventory_players_service
        )

        # FEATURES - INVENTORY

        self.inventory_service = InventoryService(
            metabomb_api_service=self.metabomb_api_service,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            metabomb_moralis_service=self.metabomb_moralis_service,
            mapper_service=self.mapper_service
        )

        self.inventory_controller = InventoryController(
            client_service=self.client_service,
            inventory_service=self.inventory_service
        )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.boxes_market_controller)
    container.client_service.add_controller(container.dashboard_controller)
    container.client_service.add_controller(container.heroes_market_controller)
    container.client_service.add_controller(
        container.inventory_players_controller
    )
    container.client_service.add_controller(
        container.inventory_controller
    )

    container.client_service.listen()
