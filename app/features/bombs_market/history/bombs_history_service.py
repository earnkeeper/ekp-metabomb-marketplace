from db.bombs_sales_repo import BombsSalesRepo

from shared.mapper_service import MapperService
from shared.metabomb_coingecko_service import MetabombCoingeckoService


class BombsHistoryService:
    def __init__(
        self,
        bombs_sales_repo: BombsSalesRepo,
        metabomb_coingecko_service: MetabombCoingeckoService,
        mapper_service: MapperService
    ):
        self.bombs_sales_repo = bombs_sales_repo
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.mapper_service = mapper_service

    async def get_documents(self, currency):
        rate = await self.metabomb_coingecko_service.get_usd_price(currency["id"])

        models = self.bombs_sales_repo.find_all('bomb', 1000)

        documents = []

        for model in models:
            document = self.map_document(model, currency, rate)
            documents.append(document)

        return documents

    def map_document(self, model, currency, rate):
        bomb = model['bomb']['bomb']
        rarity_name = bomb['rarity_name']
        element_name = bomb['element_name'].lower()
        name = f"{rarity_name} Bomb"

        
        return {
            "bnbCost": model["bnbCost"],
            "bnbCostFiat": model["bnbCostUsd"] * rate,
            "buyer": model["buyer"],
            "display_id": bomb['display_id'],
            "fiatSymbol": currency["symbol"],
            "hash": model["hash"],
            "name": name,
            "rarity": rarity_name,
            "element_name": element_name,
            "skill_1": bomb['skill_1'],
            "skill_2": bomb['skill_2'],
            "skill_3": bomb['skill_3'],
            "skill_4": bomb['skill_4'],
            "skill_5": bomb['skill_5'],
            "skill_6": bomb['skill_6'],
            "type": model["nftType"],
            "price": model["price"],
            "priceFiat": model["priceUsd"] * rate,
            "seller": model["seller"],
            "updated": model["timestamp"],
            "timestamp": model["timestamp"],
            "tokenId": model["tokenId"],
        }
