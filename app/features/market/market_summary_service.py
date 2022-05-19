from datetime import datetime


class MarketSummaryService:
    def get_documents(self, listing_documents, history_documents, currency):

        return [
            {
                "id": "0",
                "updated": datetime.now().timestamp(),
                "common": {
                    "name": "Common Box",
                    "floorPrice": 38.5,
                    "avgPrice": 41.2,
                    "fiatSymbol": currency["symbol"]
                },
                "premium": {
                    "name": "Premium Box",
                    "floorPrice": 170,
                    "avgPrice": 191,
                    "fiatSymbol": currency["symbol"]
                },
                "ultra": {
                    "name": "Ultra Box",
                    "floorPrice": 700,
                    "avgPrice": None,
                    "fiatSymbol": currency["symbol"]
                },
            }
        ]
