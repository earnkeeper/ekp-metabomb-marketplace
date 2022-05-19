import time

from ekp_sdk.services import CacheService, CoingeckoService
from gql.transport.aiohttp import AIOHTTPTransport
from gql import Client, gql
from datetime import datetime

class MarketListingsService:
    def __init__(
        self,
        cache_service: CacheService,
        coingecko_service: CoingeckoService
    ):
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service

    async def get_documents(self, currency):
        url = "https://api.metabomb.io/graphql/"

        print(f"🐛 {url}")

        start = time.perf_counter()

        transport = AIOHTTPTransport(url=url)

        async with Client(transport=transport) as client:
            result = await client.execute(
                self.__QUERY,
                variable_values=self.params(1, 5000)
            )

            print(f"⏱  [{url}] {time.perf_counter() - start:0.3f}s")

            listings = result["box_market"]["boxes"]

            documents = []
            
            now = datetime.now().timestamp()

            rate = await self.coingecko_service.get_latest_price("metabomb", currency["id"])

            for listing in listings:
                document = self.map_document(listing, currency, rate, now)

    async def map_document(self, listing, currency, rate, now):
        price = listing["price"] / 1000000
        
        return {
            "fiatSymbol": currency["symbol"],
            "id": listing["id"],
            "name": self.__BOX_TYPES[listing["box_type"]],
            "price": price,
            "priceFiat": price * rate,
            "seller": listing["user"]["wallet_address"],
            "tokenId": listing["token_id"],
            "type": listing["__typename"],
            "updated": now,
        }

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

    def params()
