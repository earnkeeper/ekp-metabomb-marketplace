from shared.metabomb_coingecko_service import MetabombCoingeckoService


class DashboardHeroProfitService:
    def __init__(
            self,
            metabomb_coingecko_service: MetabombCoingeckoService,
    ):
        self.metabomb_coingecko_service = metabomb_coingecko_service

    async def get_documents(self, listing_documents, currency):

        mtb_rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        all_documents = []

        for rarity, powers in self.POWERS_OF_RARITIES.items():
            documents = []
            for power in powers:
                document = {}
                document['power'] = power
                spec_listings = list(
                    filter(lambda x: x['power'] == power and x['rarity_name'] == rarity, listing_documents))
                mtb_per_day = 0.145 * 0.5 * 1440 * power
                fiat_per_day = mtb_per_day * mtb_rate
                floor_price = None
                roi = None
                if spec_listings:
                    floor_price = min(spec_listing["priceFiat"] for spec_listing in spec_listings)
                    roi = int(fiat_per_day * 365 * 100 / floor_price)
                document['market_value'] = floor_price
                document['mtb_per_day'] = int(mtb_per_day)
                document['roi'] = roi
                document["fiat_symbol"] = currency["symbol"],
                documents.append(document)

            all_documents.append(documents)

        return all_documents

    POWERS_OF_RARITIES = {
        "Common": [1, 2, 3, 4],
        "Rare": [4, 5, 6, 7],
        "Epic": [7, 8, 9, 10],
        "Legend": [10, 11, 12, 13]
    }