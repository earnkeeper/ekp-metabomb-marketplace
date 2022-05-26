import asyncio
from ekp_sdk.services import MoralisApiService, CacheService, CoingeckoService
from app.utils.lists import flatten
from datetime import datetime

from shared.constants import COMMON_BOX_CONTRACT_ADDRESS, HERO_CONTRACT_ADDRESS, PREMIUM_BOX_CONTRACT_ADDRESS, ULTRA_BOX_CONTRACT_ADDRESS
from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService

BOX_CONTRACT_ADDRESSES = [
    COMMON_BOX_CONTRACT_ADDRESS,
    PREMIUM_BOX_CONTRACT_ADDRESS,
    ULTRA_BOX_CONTRACT_ADDRESS
]


class InventoryPlayersService:
    def __init__(
        self,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        mapper_service: MapperService,
        metabomb_api_service: MetabombApiService,
        moralis_api_service: MoralisApiService,
    ):
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.mapper_service = mapper_service
        self.metabomb_api_service = metabomb_api_service
        self.moralis_api_service = moralis_api_service

    async def get_documents(self, currency, form_values):
        documents = []

        hero_list = await self.metabomb_api_service.get_market_heroes()
        hero_map = await self.mapper_service.get_hero_map(hero_list)
        hero_price_map = await self.mapper_service.get_hero_price_map(hero_list)
        mtb_rate = await self.coingecko_service.get_latest_price('metabomb', currency["id"])
        
        for form_value in form_values:
            address = form_value["address"]

            document = await self.__get_document(address, currency, hero_map, hero_price_map, mtb_rate)

            documents.append(document)

        return documents

    async def __get_document(self, address, currency, hero_map, hero_price_map, mtb_rate):

        box_nfts = await self.__get_box_nfts(address)
        hero_nfts = await self.__get_hero_nfts(address)

        total_price = 0
        for hero_nft in hero_nfts:
            token_id = hero_nft["token_id"]

            if token_id not in hero_map:
                continue

            hero = hero_map[token_id]

            rarity = str(hero["rarity"])
            
            level = str(hero["level"])

            price = self.mapper_service.get_hero_price(rarity, level, hero_price_map)
            
            if price:
                total_price += price

        document = {
            "id": address,
            "updated": datetime.now().timestamp(),
            "fiat_symbol": currency["symbol"],
            "boxes": len(box_nfts),
            "heroes": len(hero_nfts),
            "market_value_fiat": total_price * mtb_rate
        }

        return document
    
        
        

    

    

    async def __get_hero_nfts(self, address):
        return await self.cache_service.wrap(
            f"metabomb_nfts_{address}_{HERO_CONTRACT_ADDRESS}",
            lambda: self.moralis_api_service.get_nfts_by_owner_and_token_address(
                address,
                HERO_CONTRACT_ADDRESS,
                'bsc',
            ),
            ex=60
        )

    async def __get_box_nfts(self, address):
        futures = []

        for contract_address in BOX_CONTRACT_ADDRESSES:
            futures.append(
                self.cache_service.wrap(
                    f"metabomb_nfts_{address}_{contract_address}",
                    lambda: self.moralis_api_service.get_nfts_by_owner_and_token_address(
                        address,
                        contract_address,
                        'bsc',
                    ),
                    ex=60
                )
            )

        gathered = await asyncio.gather(*futures)

        return flatten(gathered)
