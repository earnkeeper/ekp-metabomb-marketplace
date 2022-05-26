from db.market_sales_repo import MarketSalesRepo
from ekp_sdk.services import CoingeckoService

from shared.mapper_service import MapperService


class HeroesHistoryService:
    def __init__(
        self,
        market_sales_repo: MarketSalesRepo,
        coingecko_service: CoingeckoService,
        mapper_service: MapperService
    ):
        self.market_sales_repo = market_sales_repo
        self.coingecko_service = coingecko_service
        self.mapper_service = mapper_service

    async def get_documents(self, currency):
        rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])

        models = self.market_sales_repo.find_all('hero', 1000)

        documents = []

        for model in models:
            document = self.map_document(model, currency, rate)
            documents.append(document)

        return documents

    def map_document(self, model, currency, rate):
        hero = model['hero']['hero']
        rarity = hero['rarity_name']
        level = hero['level']
        name = self.mapper_service.map_hero_name(rarity, level)
        
        return {
            "bnbCost": model["bnbCost"],
            "bnbCostFiat": model["bnbCostUsd"] * rate,
            "buyer": model["buyer"],
            "display_id": hero['display_id'],
            "fiatSymbol": currency["symbol"],
            "hash": model["hash"],
            "name": name,
            "rarity": hero["rarity_name"],
            "level": hero["level"] + 1,
            "type": model["nftType"],
            "price": model["price"],
            "priceFiat": model["priceUsd"] * rate,
            "seller": model["seller"],
            "updated": model["timestamp"],
            "timestamp": model["timestamp"],
            "tokenId": model["tokenId"],
        }
