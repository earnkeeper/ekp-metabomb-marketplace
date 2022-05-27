
from shared.metabomb_coingecko_service import MetabombCoingeckoService
from shared.metabomb_moralis_service import MetabombMoralisService

from datetime import datetime

from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService


class InventoryPlayersService:
    def __init__(
        self,
        mapper_service: MapperService,
        metabomb_api_service: MetabombApiService,
        metabomb_coingecko_service: MetabombCoingeckoService,
        metabomb_moralis_service: MetabombMoralisService,
    ):
        self.mapper_service = mapper_service
        self.metabomb_api_service = metabomb_api_service
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.metabomb_moralis_service = metabomb_moralis_service

    async def get_documents(self, currency, form_values):
        documents = []

        hero_list = await self.metabomb_api_service.get_market_heroes()
        box_list = await self.metabomb_api_service.get_market_boxes()
        mtb_rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        hero_map = self.mapper_service.get_hero_map(hero_list)
        hero_price_map = self.mapper_service.get_hero_price_map(hero_list)

        box_price_map = self.mapper_service.get_box_price_map(box_list)

        for form_value in form_values:
            address = form_value["address"]

            document = await self.__get_document(
                address,
                currency,
                hero_map,
                hero_price_map,
                box_price_map,
                mtb_rate
            )

            documents.append(document)

        return documents

    async def __get_document(
        self,
        address,
        currency,
        hero_map,
        hero_price_map,
        box_price_map,
        mtb_rate
    ):

        box_nfts = await self.metabomb_moralis_service.get_boxes_by_address(address)
        hero_nfts = await self.metabomb_moralis_service.get_heroes_by_address(address)

        total_price = 0

        for hero_nft in hero_nfts:
            token_id = hero_nft["token_id"]

            if token_id not in hero_map:
                continue

            hero = hero_map[token_id]

            rarity = str(hero["rarity"])

            level = str(hero["level"])

            price = self.mapper_service.get_hero_price(
                rarity,
                level,
                hero_price_map
            )

            if price:
                total_price += price

        for box_nft in box_nfts:
            contract_address = box_nft["token_address"]

            box_name = self.mapper_service.get_box_name_by_contract_address(
                contract_address
            )

            price = box_price_map.get(box_name, None)

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
