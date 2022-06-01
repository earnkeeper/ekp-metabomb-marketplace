import time
from datetime import datetime

from ekp_sdk.services import CoingeckoService
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


class BoxesListingsService:
    def __init__(
        self,
        coingecko_service: CoingeckoService
    ):
        self.coingecko_service = coingecko_service

    async def get_documents(self, currency, history_documents):
        url = "https://api.metabomb.io/graphql/"

        print(f"🐛 {url}")

        start = time.perf_counter()

        transport = AIOHTTPTransport(url=url)

        now = datetime.now().timestamp()

        name_totals = self.get_name_totals(history_documents, now)

        async with Client(transport=transport) as client:
            gql_result = await client.execute(
                self.__QUERY,
                variable_values=self.params(1, 5000)
            )

            print(f"⏱  [{url}] {time.perf_counter() - start:0.3f}s")

            listings = gql_result["box_market"]["boxes"]

            documents = []

            rate = await self.coingecko_service.get_latest_price("metabomb", currency["id"])

            for listing in listings:
                document = self.map_document(
                    listing, 
                    currency, 
                    rate, 
                    now, 
                    name_totals
                )
                
                if document:
                    documents.append(document)

            return documents

    def map_document(self, listing, currency, rate, now, name_totals):
        price = listing["price"]
        
        box_type = listing["box_type"]
        
        if box_type not in self.__BOX_TYPES:
            return None
        
        name = self.__BOX_TYPES[box_type]

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
            "pcAboveAvg": pc_above_avg_price,
            "pcAboveAvgFiat": pc_above_avg_price_fiat,
            "deal": deal,
            "price": price,
            "priceFiat": price * rate,
            "seller": listing["user"]["wallet_address"],
            "tokenId": int(listing["token_id"]),
            "type": listing["__typename"],
            "updated": now,
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

    __QUERY = gql("""
    query box_market($input: BoxMarketInput!) {
    box_market(input: $input) {
        error
        count
        boxes {
        id
        token_id
        user {
            wallet_address
            __typename
        }
        box_type
        price
        for_sale
        chain_process
        __typename
        }
        __typename
    }
    }
    """)

    def params(self, page, count):
        return {
            "input": {
                "f5": 0,
                "token_id": -1,
                "page": page,
                "count": count,
                "sort": 0,
                "sort_type": 3,
                "box_type": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5
                ],
                "forSale": 2

            }
        }
