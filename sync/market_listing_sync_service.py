import json
import time

from ekp_sdk.services import CacheService
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


class MarketListingSyncService():
    def __init__(
        self,
        cache_service: CacheService
    ):
        self.cache_service = cache_service

    async def sync_market_listings(self):

        url = "https://api.metabomb.io/graphql/"

        print(f"🐛 {url}")

        start = time.perf_counter()

        transport = AIOHTTPTransport(url=url)

        async with Client(transport=transport) as client:
            result = await client.execute(
                self.query(),
                variable_values=self.params(1, 5000)
            )

            listings = result["hero_market"]["heroes"]

            print(f"⏱  [{url}] {time.perf_counter() - start:0.3f}s")

            await self.cache_service.set("market_listings", listings)

    def query(self):
        return gql(
            """
            query hero_market($input: HeroMarketInput!) {
                hero_market(input: $input) {
                    error
                    count
                    heroes {
                    id
                    name
                    display_id
                    rarity
                    level
                    hero_class
                    for_sale
                    price
                    __typename
                    }
                    __typename
                }
            }
            """
        )

    def params(self, page, count):
        return {
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
