
import asyncio

from decouple import AutoConfig
from ekp_sdk import BaseContainer
from ekp_sdk.db import ContractLogsRepo, ContractTransactionsRepo
from ekp_sdk.services import TransactionSyncService
from db.box_opens_repo import BoxOpensRepo

from db.market_listings_repo import MarketListingsRepo
from db.box_ import MarketTransactionsRepo
from db.state_repo import StateRepo
from shared.metabomb_api_service import MetabombApiService
from sync.box_open_decoder_service import BoxOpenDecoderService
from sync.market_decoder_service import MarketDecoderService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        # DB

        self.market_transactions_repo = MarketTransactionsRepo(
            mg_client=self.mg_client,
        )

        self.market_listings_repo = MarketListingsRepo(
            mg_client=self.mg_client,
        )

        self.box_opens_repo = BoxOpensRepo(
            mg_client=self.mg_client,
        )

        self.state_repo = StateRepo(
            mg_client=self.mg_client,
        )
        
        # Services
        
        self.metabomb_api_service = MetabombApiService(
            coingecko_service=self.coingecko_service
        )

        self.box_open_decoder_service = BoxOpenDecoderService(
            box_opens_repo=self.box_opens_repo,
            contract_transactions_repo=self.contract_transactions_repo,
            metabomb_api_service=self.metabomb_api_service
        )

        self.market_decoder_service = MarketDecoderService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            contract_logs_repo=self.contract_logs_repo,
            contract_transactions_repo=self.contract_transactions_repo,
            etherscan_service=self.etherscan_service,
            market_transactions_repo=self.market_transactions_repo,
            market_listings_repo=self.market_listings_repo,
            web3_service=self.web3_service,
        )


if __name__ == '__main__':
    container = AppContainer()

    print("🚀 Application Start")

    loop = asyncio.get_event_loop()

    contract_addresses = [
        "0x05f0d89931eb06d4596af209de4a9779cef73cde", # MetaBombHero
        '0x1f36bef063ee6fcefeca070159d51a3b36bc68d6', # Common Box
        '0x2076626437c3bb9273998a5e4f96438abe467f1c', # Premium Box
        '0x9341faed0b86208c64ae6f9d62031b1f8a203240', # Ultra Box
    ]

    log_addresses = [
        "0x05f0d89931eb06d4596af209de4a9779cef73cde", # MetaBombHero
        '0x1f36bef063ee6fcefeca070159d51a3b36bc68d6', # Common Box
        '0x2076626437c3bb9273998a5e4f96438abe467f1c', # Premium Box
        '0x9341faed0b86208c64ae6f9d62031b1f8a203240', # Ultra Box
        '0x2bad52989afc714c653da8e5c47bf794a8f7b11d', # MetaBombToken
    ]

    futures = []

    for contract_address in contract_addresses:
        futures.append(
            container.transaction_sync_service.sync_transactions(contract_address, 17394713)
        )

    for log_address in log_addresses:
        futures.append(
            container.transaction_sync_service.sync_logs(log_address, 17394713)
        )

    loop.run_until_complete(
        asyncio.gather(*futures)
    )

    loop.run_until_complete(
        container.market_decoder_service.decode_market_trans()
    )

    loop.run_until_complete(
        container.box_open_decoder_service.decode_box_openings()
    )
    
