
from ekp_sdk.services import CoingeckoService
from shared.metabomb_coingecko_service import MetabombCoingeckoService
from shared.metabomb_moralis_service import MetabombMoralisService

from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService

from datetime import datetime


class InventoryService:
    def __init__(
        self,
        mapper_service: MapperService,
        metabomb_api_service: MetabombApiService,
        metabomb_coingecko_service: MetabombCoingeckoService,
        metabomb_moralis_service=MetabombMoralisService,
    ):
        self.mapper_service = mapper_service
        self.metabomb_api_service = metabomb_api_service
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.metabomb_moralis_service = metabomb_moralis_service
        
    async def get_hero_documents(self, address, currency):
        documents = []

        hero_list = await self.metabomb_api_service.get_market_heroes()
        # print(f'hero list is: \n {hero_list}')
        mtb_rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        hero_map = self.mapper_service.get_hero_map(hero_list)
        # print(f'hero map is: \n {hero_map}')
        hero_price_map = self.mapper_service.get_hero_price_map(hero_list)
        # print(f'hero price map is: \n {hero_price_map}')
        hero_nfts = await self.metabomb_moralis_service.get_heroes_by_address(address)

        documents = []

        for hero_nft in hero_nfts:

            token_id = str(hero_nft["token_id"])

            stats = await self.metabomb_api_service.get_hero(token_id)
            # print(stats)

            if token_id not in hero_map:
                continue

            hero = hero_map[token_id]
            rarity = hero["rarity"]
            rarity_name = self.mapper_service.HERO_RARITY_TO_NAME[rarity]
            level = hero["level"]
            hero_class = hero["hero_class"]

            price = self.mapper_service.get_hero_price(
                rarity,
                level,
                hero_price_map
            )

            price_fiat = None

            if price:
                price_fiat = price * mtb_rate

            mtb_per_day = 0.145 * 0.5 * 1440 * stats['power']
            fiat_per_day = mtb_per_day * mtb_rate
            
            est_payback = None
            est_roi = None
            
            if price_fiat:
                est_payback = f"{int(price_fiat / fiat_per_day)} days"
                est_roi = int(fiat_per_day * 365 * 100 / price_fiat)
                
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
                "price_fiat": price_fiat,
                "hero_power": stats['power'],
                "hero_health": stats['health'],
                "hero_speed": stats['speed'],
                "hero_stamina": stats['stamina'],
                "hero_bomb_num": stats['bomb_num'],
                "hero_bomb_range": stats['bomb_range'],
                "mtb_per_day": mtb_per_day,
                "fiat_per_day": fiat_per_day,
                "est_payback": est_payback,
                "est_roi": est_roi
            }

            documents.append(document)

        # print(documents)

        return documents

    async def get_box_documents(self, address, currency):
        documents = []

        box_list = await self.metabomb_api_service.get_market_boxes()
        mtb_rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        box_price_map = self.mapper_service.get_box_price_map(box_list)

        box_nfts = await self.metabomb_moralis_service.get_boxes_by_address(address)

        documents = []

        for box_nft in box_nfts:

            token_id = str(box_nft["token_id"])

            contract_address = box_nft["token_address"]

            name = self.mapper_service.get_box_name_by_contract_address(
                contract_address
            )

            price = box_price_map.get(name, None)

            price_fiat = None

            if price:
                price_fiat = price * mtb_rate

            document = {
                "id": token_id,
                "updated": datetime.now().timestamp(),
                "name": name,
                "fiat_symbol": currency["symbol"],
                "price": price,
                "price_fiat": price_fiat
            }

            documents.append(document)

        return documents
