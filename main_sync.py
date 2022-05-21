
import asyncio

from decouple import AutoConfig
from ekp_sdk import BaseContainer
from ekp_sdk.db import ContractLogsRepo, ContractTransactionsRepo
from ekp_sdk.services.transaction_sync_service import TransactionSyncService

from db.market_listings_repo import MarketListingsRepo
from db.market_transactions_repo import MarketTransactionsRepo
from db.state_repo import StateRepo
from sync.market_decoder_service import MarketDecoderService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        # DB

        self.contract_transactions_repo = ContractTransactionsRepo(
            mg_client=self.mg_client,
        )

        self.contract_logs_repo = ContractLogsRepo(
            mg_client=self.mg_client,
        )

        self.market_transactions_repo = MarketTransactionsRepo(
            mg_client=self.mg_client,
        )

        self.market_listings_repo = MarketListingsRepo(
            mg_client=self.mg_client,
        )

        self.state_repo = StateRepo(
            mg_client=self.mg_client,
        )

        # Services

        self.sync_service = TransactionSyncService(
            contract_logs_repo=self.contract_logs_repo,
            contract_transactions_repo=self.contract_transactions_repo,
            etherscan_service=self.etherscan_service
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
        '0x2076626437c3bb9273998a5e4f96438abe467f1c',
        '0x1f36bef063ee6fcefeca070159d51a3b36bc68d6',
    ]

    log_addresses = [
        '0x2bad52989afc714c653da8e5c47bf794a8f7b11d',
        '0x96dfbd2c945bca02378ffd8e4593054d098e8bac',
        '0x2076626437c3bb9273998a5e4f96438abe467f1c',
        '0x1f36bef063ee6fcefeca070159d51a3b36bc68d6'
    ]

    futures = []

    for contract_address in contract_addresses:
        futures.append(
            container.sync_service.sync_transactions(contract_address)
        )

    for log_address in log_addresses:
        futures.append(
            container.sync_service.sync_logs(log_address)
        )

    loop.run_until_complete(
        asyncio.gather(*futures)
    )

    loop.run_until_complete(
        container.market_decoder_service.decode_market_trans()
    )
