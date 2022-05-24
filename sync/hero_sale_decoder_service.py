from ast import literal_eval
from datetime import datetime
from typing import List

from db.market_sale_model import MarketSaleModel
from db.market_sales_repo import MarketSalesRepo
from ekp_sdk.db import ContractTransactionsRepo
from ekp_sdk.services import CacheService, CoingeckoService
from shared.domain.market_listing import MarketListing
from shared.mapper_service import MapperService
from web3 import Web3

from shared.metabomb_api_service import MetabombApiService

HERO_CONTRACT_ADDRESS = "0x05f0d89931eb06d4596af209de4a9779cef73cde"
MTB_CONTRACT_ADDRESS = "0x2bad52989afc714c653da8e5c47bf794a8f7b11d"


class HeroSaleDecoderService:
    def __init__(
        self,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        contract_transactions_repo: ContractTransactionsRepo,
        mapper_service: MapperService,
        market_sales_repo: MarketSalesRepo,
        metabomb_api_service: MetabombApiService,
    ):
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.contract_transactions_repo = contract_transactions_repo
        self.mapper_service = mapper_service
        self.market_sales_repo = market_sales_repo
        self.metabomb_api_service = metabomb_api_service
        
        self.page_size = 2000

    async def decode_hero_sales(self):
        latest_block = self.market_sales_repo.find_latest_block_number("hero")

        dtos = await self.cache_service.wrap(
            "metabomb_market_heroes",
            lambda: self.metabomb_api_service.get_market_heroes(),
            ex=60
        )

        current_listings: List[MarketListing] = await self.mapper_service.map_market_hero_dtos_to_domain(dtos)

        current_listings_map = {}

        for listing in current_listings:
            current_listings_map[listing["token_id"]] = listing

        while True:
            next_trans = self.contract_transactions_repo.find_since_block_number(
                latest_block,
                self.page_size,
                "0xc010adef",
            )

            if not len(next_trans):
                break

            sales = []

            for next_tran in next_trans:
                block_number = next_tran["blockNumber"]

                sale = await self.__decode_hero_sale(next_tran, current_listings_map)
                
                if sale:
                    sales.append(sale)

                latest_block = block_number

            if len(sales):
                self.market_sales_repo.save(sales)

            if len(next_trans) < self.page_size:
                break
            
        print("✅ Finished hero sales..")

    async def __decode_hero_sale(self, tran, current_listings_map):
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
            if address == HERO_CONTRACT_ADDRESS and topics[0] == "0xc6d6dcdcf9baa723dfb3d8bba95a720bb298f9ebda5de8e18d0859dab3db8632":
                token_id = literal_eval(topics[1])

        distributions.sort()

        bnb_cost = Web3.fromWei(tran["gasUsed"] * tran["gasPrice"], 'ether')
        price = sum(distributions)
        fees = price - distributions[-1]

        hero = current_listings_map[str(token_id)]

        sale: MarketSaleModel = {
            "bnbCost": float(bnb_cost),
            "bnbCostUsd": float(bnb_cost) * bnb_usd_price,
            "blockNumber": block_number,
            "buyer": tran["from"],
            "fees": float(fees),
            "feesUsd": float(fees) * mtb_usd_price,
            "hash": hash,
            "hero": hero,
            "nftType": "hero",
            "price": float(price),
            "priceUsd": float(price) * mtb_usd_price,
            "seller": seller,
            "timestamp": timestamp,
            "tokenId": str(token_id),
        }

        return sale