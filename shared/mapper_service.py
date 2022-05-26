import asyncio
from datetime import datetime
from typing import List

from ekp_sdk.services import BaseMapperService, CacheService, CoingeckoService

from shared.domain.hero import Hero
from shared.domain.hero_box import HeroBox
from shared.domain.market_listing import MarketListing
from shared.dto.box_market_listing_dto import BoxMarketListingDto
from shared.dto.hero_dto import HeroDto
from shared.dto.hero_market_listing_dto import HeroMarketListingDto


class MapperService(BaseMapperService):
    def __init__(
        self,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
    ):
        self.coingecko_service = coingecko_service
        self.cache_service = cache_service

    async def get_mtb_rate(self):
        rate = await self.cache_service.wrap("latest_price_metabomb_usd", lambda: self.coingecko_service.get_latest_price("metabomb", "usd"), ex=60)
        return rate

    def map_hero_dto_to_domain(self, dto: HeroDto) -> Hero:
        hero: Hero = {
            'bomb_num': dto['bomb_num'],
            'bomb_range': dto['bomb_range'],
            'display_id': dto['display_id'],
            'health': dto['health'],
            'hero_class': dto['hero_class'],
            'hero_class_name': self.HERO_CLASS_TO_NAME[dto['hero_class']],
            'id': dto['id'],
            'level': dto['level'],
            'name': dto['name'],
            'power': dto['power'],
            'rarity': dto['rarity'],
            'rarity_name': self.HERO_RARITY_TO_NAME[dto['rarity']],
            'speed': dto['speed'],
            'stamina': dto['stamina'],
        }

        return hero

    def get_hero_image_url(self, display_id):
        return f"https://app.metabomb.io/gifs/char-gif/{display_id}.gif"

    def get_hero_box_url(self, box_type):
        return self.HERO_BOX_TYPE_TO_IMAGE_URL[box_type]

    def map_hero_name(self, rarity_name, level):
        return f'{rarity_name} Lv {int(level) + 1} Hero'
    
    async def map_market_box_dtos_to_domain(self, dtos: List[BoxMarketListingDto]) -> List[MarketListing]:
        mtb_rate = await self.get_mtb_rate()

        futures = []

        for dto in dtos:
            futures.append(self.map_market_box_dto_to_domain(dto, mtb_rate))

        listings = await asyncio.gather(*futures)

        return listings

    def map_box_type_to_domain(self, box_type: int) -> HeroBox:
        box: HeroBox = {
            'type': box_type,
            'name': self.HERO_BOX_TYPE_TO_NAME[box_type]
        }
        
        return box
        
    async def map_market_box_dto_to_domain(self, dto: BoxMarketListingDto, mtb_rate: int = None) -> MarketListing:
        box = self.map_box_type_to_domain[dto["box_type"]]

        if mtb_rate is None:
            mtb_rate = await self.get_mtb_rate()

        market_listing: MarketListing = {
            'box': box,
            'for_sale': dto['for_sale'] == 1,
            'id': dto['id'],
            'price_mtb': dto['price'],
            'price_usdc': dto['price'] * mtb_rate,
            'seller': dto['user']['wallet_address'],
            'token_id': dto['token_id'],
            'updated': datetime.now().timestamp(),
        }

        return market_listing

    async def map_market_hero_dtos_to_domain(self, dtos: List[HeroMarketListingDto]) -> List[MarketListing]:
        mtb_rate = await self.get_mtb_rate()

        futures = []

        for dto in dtos:
            futures.append(self.map_market_hero_dto_to_domain(dto, mtb_rate))

        listings = await asyncio.gather(*futures)

        return listings

    async def get_hero_map(self, hero_list):
        hero_map = {}
        
        for hero in hero_list:
            token_id = str(hero["id"])
            hero_map[token_id] = hero
            
        return hero_map
    
    async def get_hero_price_map(self, hero_list):
        hero_price_map = {}
        
        for hero in hero_list:
            if not hero["for_sale"]:
                continue
            
            rarity = str(hero["rarity"])
            level = str(hero["level"])
            price = int(hero["price"])
            
            if rarity not in hero_price_map:
                hero_price_map[rarity] = {}
            
            if (level not in hero_price_map[rarity]) or (hero_price_map[rarity][level] > price):
                hero_price_map[rarity][level] = price
                
        return hero_price_map    

    def get_hero_price(self, rarity, level, hero_price_map):
        if str(rarity) not in hero_price_map:
            return None

        if str(level) not in hero_price_map[str(rarity)]:
            return None

        return hero_price_map[str(rarity)][str(level)]

    async def map_market_hero_dto_to_domain(self, dto: HeroMarketListingDto, mtb_rate: int = None) -> MarketListing:
        hero: Hero = {
            'id': dto['id'],
            'display_id': dto['display_id'],
            'hero_class': dto['hero_class'],
            'hero_class_name': self.HERO_CLASS_TO_NAME[dto['hero_class']],
            'level': dto['level'],
            'rarity': dto['rarity'],
            'rarity_name': self.HERO_RARITY_TO_NAME[dto['rarity']],
        }

        if mtb_rate is None:
            mtb_rate = await self.get_mtb_rate()

        market_listing: MarketListing = {
            'hero': hero,
            'for_sale': dto['for_sale'] == 1,
            'id': dto['id'],
            'price_mtb': dto['price'],
            'price_usdc': dto['price'] * mtb_rate,
            'token_id': dto['id'],
            'updated': datetime.now().timestamp(),
        }

        return market_listing

    HERO_BOX_TYPE_TO_NAME = {
        0: "Common Box",
        1: "Premium Box",
        2: "Ultra Box"
    }

    HERO_CLASS_TO_NAME = {
        0: "Warrior",
        1: "Assassin",
        2: "Mage",
        3: "Support",
        4: "Ranger",
    }

    HERO_RARITY_TO_NAME = {
        0: "Common",
        1: "Rare",
        2: "Epic",
        3: "Legend",
        4: "Mythic",
        5: "Meta",
    }

    HERO_BOX_TYPE_TO_IMAGE_URL = {
        0: "https://app.metabomb.io/gifs/herobox-gif/normal-box.gif",
        1: "https://app.metabomb.io/gifs/herobox-gif/premium-box.gif",
        2: "https://app.metabomb.io/gifs/herobox-gif/ultra-box.gif"
    }
