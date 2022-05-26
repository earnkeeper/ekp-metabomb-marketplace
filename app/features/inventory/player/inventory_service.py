
from ekp_sdk.services import MoralisApiService, CacheService, CoingeckoService

from shared.constants import HERO_CONTRACT_ADDRESS
from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService

from datetime import datetime

class InventoryService:
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

    async def get_hero_documents(self, address, currency):
        documents = []

        hero_list = await self.metabomb_api_service.get_market_heroes()
        hero_map = await self.mapper_service.get_hero_map(hero_list)
        hero_price_map = await self.mapper_service.get_hero_price_map(hero_list)
        mtb_rate = await self.coingecko_service.get_latest_price('metabomb', currency["id"])
        
        hero_nfts = await self.moralis_api_service.get_nfts_by_owner_and_token_address(
            address,
            HERO_CONTRACT_ADDRESS,
            'bsc'
        )
        
        documents = []
        
        for hero_nft in hero_nfts:
            
            token_id = str(hero_nft["token_id"])
            
            if token_id not in hero_map:
                continue
            
            hero = hero_map[token_id]
            rarity = hero["rarity"]
            rarity_name = self.mapper_service.HERO_RARITY_TO_NAME[rarity]
            level = hero["level"]
            hero_class = hero["hero_class"]

            price = self.mapper_service.get_hero_price(rarity, level, hero_price_map)
            price_fiat = None
            if price:
                price_fiat = price * mtb_rate
            document = {
                "id": token_id,
                "updated": datetime.now().timestamp(),
                "display_id": hero['display_id'],
                "name": self.mapper_service.map_hero_name(rarity_name, level),
                "rarity_name": rarity_name,
                "level": level + 1,
                "hero_class": hero_class,
                "fiat_symbol": currency["symbol"],
                "price": price,
                "price_fiat": price_fiat
            }   
            
            documents.append(document)

        return documents