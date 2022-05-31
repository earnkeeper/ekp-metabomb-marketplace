from datetime import datetime

from ekp_sdk.services import CoingeckoService
from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService
from db.hero_listing_timestamp_repo import HeroListingTimestampRepo


class HeroListingsService:
    def __init__(
            self,
            coingecko_service: CoingeckoService,
            metabomb_api_service: MetabombApiService,
            mapper_service: MapperService,
            hero_listing_timestamp_repo: HeroListingTimestampRepo
    ):
        self.coingecko_service = coingecko_service
        self.metabomb_api_service = metabomb_api_service
        self.mapper_service = mapper_service
        self.hero_listing_timestamp_repo = hero_listing_timestamp_repo

    async def get_documents(self, currency, history_documents):
        url = "https://api.metabomb.io/graphql/"

        print(f"🐛 {url}")

        now = datetime.now().timestamp()

        name_totals = self.get_name_totals(history_documents, now)

        listings = await self.metabomb_api_service.get_market_heroes()

        hero_listing_timestamps = list(self.hero_listing_timestamp_repo.collection.find())
        # print(hero_listing_timestamps)

        documents = []

        rate = await self.coingecko_service.get_latest_price("metabomb", currency["id"])

        for listing in listings:
            if not listing['for_sale']:
                continue

            document = self.map_document(
                listing, hero_listing_timestamps,
                currency, rate, now, name_totals)
            documents.append(document)

        return documents

    def map_document(self, listing, hero_listing_timestamps, currency, rate, now, name_totals):
        price = listing["price"]

        rarity_name = self.mapper_service.HERO_RARITY_TO_NAME[listing["rarity"]]
        token_id = int(listing["id"])
        timestamp = [hero_listing_timestamp['tokenId'] for hero_listing_timestamp in hero_listing_timestamps if
                     hero_listing_timestamp['tokenId'] == token_id]

        # find the hero listing timestamp using the hero token id listing["id"]
        # print(timestamp)
        name = self.mapper_service.map_hero_name(rarity_name, listing["level"])

        name_total = None
        if name in name_totals:
            name_total = name_totals[name]

        avg_price_24h = None
        avg_price_fiat_24h = None
        pc_above_avg_price = None
        pc_above_avg_price_fiat = None

        deal = "?"

        if name_total is not None:
            avg_price_24h = name_total["price_total"] / name_total["count"]
            avg_price_fiat_24h = name_total["price_fiat_total"] / \
                                 name_total["count"]
            pc_above_avg_price = (price - avg_price_24h) * 100 / avg_price_24h
            pc_above_avg_price_fiat = (
                                              price * rate - avg_price_fiat_24h) * 100 / avg_price_fiat_24h
            if pc_above_avg_price_fiat < 0:
                deal = "yes"
            if pc_above_avg_price_fiat > 1:
                deal = "no"

        return {
            "fiatSymbol": currency["symbol"],
            "id": int(listing["id"]),
            "name": name,
            "avgPrice": avg_price_24h,
            "avgPriceFiat": avg_price_fiat_24h,
            "display_id": listing['display_id'],
            "pcAboveAvg": pc_above_avg_price,
            "pcAboveAvgFiat": pc_above_avg_price_fiat,
            "deal": deal,
            "price": price,
            "priceFiat": price * rate,
            "tokenId": int(listing["id"]),
            "type": listing["__typename"],
            "updated": now,
            "rarity_name": rarity_name,
            "level": listing["level"] + 1,
            "last_listing_timestamp": timestamp[0] if timestamp else None
        }

    def get_name_totals(self, history_documents, now):
        name_totals = {}

        for document in history_documents:
            timestamp = document["timestamp"]

            if (now - timestamp) > 86400:
                continue

            name = document["name"]

            if name not in name_totals:
                name_totals[name] = {
                    "price_total": 0,
                    "price_fiat_total": 0,
                    "count": 0
                }

            name_totals[name]["price_total"] += document["price"]
            name_totals[name]["price_fiat_total"] += document["priceFiat"]
            name_totals[name]["count"] += 1

        return name_totals

    __BOX_TYPES = {
        0: "Common Box",
        1: "Premium Box",
        2: "Ultra Box"
    }
