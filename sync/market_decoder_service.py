import sys
from ast import literal_eval
from datetime import datetime
from decimal import Decimal

from db.contract_logs_repo import ContractLogsRepo
from db.contract_transactions_repo import ContractTransactionsRepo
from db.market_transactions_repo import MarketTransactionsRepo
from ekp_sdk.services import (CacheService, CoingeckoService, EtherscanService,
                              Web3Service)
from web3 import Web3
from bson.decimal128 import Decimal128

COMMON_BOX_CONTRACT_ADDRESS = "0x1f36bef063ee6fcefeca070159d51a3b36bc68d6"
PREMIUM_BOX_CONTRACT_ADDRESS = "0x2076626437c3bb9273998a5e4f96438abe467f1c"
MTB_CONTRACT_ADDRESS = "0x2bad52989afc714c653da8e5c47bf794a8f7b11d"
TOKEN_TRANSFER_TOPIC = "0xd61e22991e1ab43a17e1ba8ddb78b72a4ffc0d7f455c8536073a6b8a9ffc0c4e"


class MarketDecoderService:
    def __init__(
        self,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        contract_logs_repo: ContractLogsRepo,
        contract_transactions_repo: ContractTransactionsRepo,
        etherscan_service: EtherscanService,
        market_transactions_repo: MarketTransactionsRepo,
        web3_service: Web3Service,
    ):
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.contract_logs_repo = contract_logs_repo
        self.contract_transactions_repo = contract_transactions_repo
        self.etherscan_service = etherscan_service
        self.market_transactions_repo = market_transactions_repo
        self.web3_service = web3_service
        self.page_size = 2000

    async def decode_market_trans(self):
        print("✨ Decoding market transactions..")

        latest_block = self.market_transactions_repo.find_latest_block_number()

        while True:
            next_trans = self.contract_transactions_repo.find_since_block_number(
                latest_block,
                self.page_size
            )

            if not len(next_trans):
                break

            buys = []            
            
            for next_tran in next_trans:
                input = next_tran["input"]
                block_number = next_tran["blockNumber"]

                if (len(input) < 10):
                    latest_block = block_number
                    continue


                if input.startswith("0x38edf988"):
                    buy = await self.__decode_market_buy(next_tran)
                    if buy:
                        buys.append(buy)

                latest_block = block_number
            
            if len(buys):
                self.market_transactions_repo.save(buys)
            
            if len(next_trans) < self.page_size:
                break

        

        print("✅ Finished decoding market transactions..")

    async def __decode_market_buy(self, tran):
        if "logs" not in tran:
            return None

        hash = tran["hash"]
        timestamp = tran["timeStamp"]
        block_number = tran["blockNumber"]
        date_str = datetime.utcfromtimestamp(timestamp).strftime("%d-%m-%Y")

        bnb_cache_key = f"bnb_price_{date_str}"
        bnb_usd_price = await self.cache_service.wrap(bnb_cache_key, lambda: self.coingecko_service.get_historic_price("binancecoin", date_str, "usd"))

        mtb_cache_key = f"mtb_price_{date_str}"
        mtb_usd_price = await self.cache_service.wrap(mtb_cache_key, lambda: self.coingecko_service.get_historic_price("metabomb", date_str, "usd"))

        distributions = []
        name = None
        price = 0
        seller = None
        token_id = 0

        logs = tran["logs"].values()

        for log in logs:
            address = log["address"]
            data = log["data"]
            topics = log["topics"]

            if address == MTB_CONTRACT_ADDRESS:
                dec = Web3.fromWei(literal_eval(data), 'ether')
                distributions.append(dec)
            if address == COMMON_BOX_CONTRACT_ADDRESS and topics[0] == TOKEN_TRANSFER_TOPIC:
                token_id = literal_eval(topics[1])
                name = "Common Box"
            if address == PREMIUM_BOX_CONTRACT_ADDRESS and topics[0] == TOKEN_TRANSFER_TOPIC:
                token_id = literal_eval(topics[1])
                name = "Premium Box"

        if name is None:
            print(f'🚨 missing name here {hash}', file=sys.stderr)

        distributions.sort()

        bnb_cost = Web3.fromWei(tran["gasUsed"] * tran["gasPrice"], 'ether')
        price = sum(distributions)
        fees = price - distributions[-1]

        return {
            "bnbCost": float(bnb_cost),
            "bnbCostUsd": float(bnb_cost) * bnb_usd_price,
            "blockNumber": block_number,
            "buyer": tran["from"],
            "fees": float(fees),
            "feesUsd": float(fees) * mtb_usd_price,
            "hash": hash,
            "nftName": name,
            "nftType": "Hero Box",
            "price": float(price),
            "priceUsd": float(price) * mtb_usd_price,
            "seller": seller,
            "timestamp": timestamp,
            "tokenId": token_id,
        }