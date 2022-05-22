from db.box_ import MarketTransactionsRepo
from ekp_sdk.services import CoingeckoService


class BoxesHistoryService:
    def __init__(
        self,
        market_transactions_repo: MarketTransactionsRepo,
        coingecko_service: CoingeckoService
    ):
        self.market_transactions_repo = market_transactions_repo
        self.coingecko_service = coingecko_service

    async def get_documents(self, currency):
        rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])

        models = self.market_transactions_repo.find_all(1000)

        documents = []

        for model in models:
            document = self.map_document(model, currency, rate)
            documents.append(document)

        return documents

    def map_document(self, model, currency, rate):

        return {
            "bnbCost": model["bnbCost"],
            "bnbCostFiat": model["bnbCostUsd"] * rate,
            "buyer": model["buyer"],
            "fiatSymbol": currency["symbol"],
            "hash": model["hash"],
            "name": model["nftName"],
            "type": model["nftType"],
            "price": model["price"],
            "priceFiat": model["priceUsd"] * rate,
            "seller": model["seller"],
            "updated": model["timestamp"],
            "timestamp": model["timestamp"],
            "tokenId": model["tokenId"],
        }
