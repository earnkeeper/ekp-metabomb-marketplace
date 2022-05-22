import time
from datetime import datetime
from typing import List

from ekp_sdk.services import CacheService, CoingeckoService
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from shared.dto.market_listing_dto import MarketListingDto


class MetabombApiService:
    def __init__(
        self,
        coingecko_service: CoingeckoService
    ):
        self.coingecko_service = coingecko_service
        self.base_url = "https://api.metabomb.io/graphql/"

    async def get_market_boxes(self) -> List[MarketListingDto]:
        url = self.base_url

        print(f"🐛 {url}")

        start = time.perf_counter()

        transport = AIOHTTPTransport(url=url)

        now = datetime.now().timestamp()

        mtb_rate = await self.coingecko_service.get_latest_price("metabomb", "usd")

        async with Client(transport=transport) as client:
            gql_result = await client.execute(
                self.__MARKET_BOX_QUERY,
                variable_values=self.__market_box_params(1, 5000)
            )

            print(f"⏱  [{url}] {time.perf_counter() - start:0.3f}s")

            listings = gql_result["box_market"]["boxes"]

            dtos = []

            for listing in listings:

                dto = self.__map_dto(listing, mtb_rate, now)

                dtos.append(dto)

            return dtos

    async def get_hero(self, token_id):
        url = self.base_url

        print(f"🐛 {url}")

        start = time.perf_counter()

        transport = AIOHTTPTransport(url=url)

        async with Client(transport=transport) as client:
            gql_result = await client.execute(
                self.__HERO_QUERY,
                variable_values={"id": str(token_id)}
            )

            print(f"⏱  [{url}] {time.perf_counter() - start:0.3f}s")

            hero = gql_result["hero"]

            return hero

    async def get_market_heroes(self):
        url = self.base_url

        print(f"🐛 {url}")

        start = time.perf_counter()

        transport = AIOHTTPTransport(url=url)

        async with Client(transport=transport) as client:
            gql_result = await client.execute(
                self.__MARKET_HERO_QUERY,
                variable_values=self.__market_hero_params(1, 5000)
            )

            print(f"⏱  [{url}] {time.perf_counter() - start:0.3f}s")

            listings = gql_result["hero_market"]["heroes"]

            return listings

    def __map_dto(self, listing, mtb_rate, now):

        price_mtb = listing["price"]
        price_usdc = price_mtb * mtb_rate

        dto = MarketListingDto(
            box_type=self.__BOX_TYPES[listing["box_type"]],
            chain_process=listing["chain_process"],
            for_sale=listing["for_sale"] == 1,
            id=listing["id"],
            price_mtb=price_mtb,
            price_usdc=price_usdc,
            token_id=listing["token_id"],
            type=listing["__typename"],
            updated=now,
            wallet_address=listing["user"]["wallet_address"],
        )

        return dto

    __MARKET_BOX_QUERY = gql("""
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

    __MARKET_HERO_QUERY = gql("""
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
        """)

    __HERO_QUERY = gql("""
        query hero($id: ID!) {
            hero(id: $id) {
                id
                user_id
                name
                display_id
                rarity
                level
                hero_class
                for_sale
                price
                power
                health
                speed
                stamina
                bomb_num
                bomb_range
                user {
                id
                name
                user_name
                __typename
                }
                __typename
            }
        }
        """)
    __BOX_TYPES = {
        0: "Common Box",
        1: "Premium Box",
        2: "Ultra Box"
    }

    def __market_box_params(self, page, count):
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

    def __market_hero_params(self, page, count):
        return {
            "input": {
                "f5": 0,
                "rarity": [0, 1, 2, 3, 4, 5],
                "class_hero": [0, 1, 2, 3, 4],
                "power": [1, 18],
                "speed": [1, 18],
                "health": [1, 18],
                "stamina": [1, 18],
                "bomb_num": [1, 4],
                "bomb_range": [1, 4],
                "level": [0, 6],
                "page": page,
                "count": count,
                "sort": 0,
                "sort_type": 1,
                "forSale": 2
            }

        }
