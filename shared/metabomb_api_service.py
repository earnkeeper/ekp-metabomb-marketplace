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

    async def get_current_listings(self) -> List[MarketListingDto]:
        url = "https://api.metabomb.io/graphql/"

        print(f"🐛 {url}")

        start = time.perf_counter()

        transport = AIOHTTPTransport(url=url)

        now = datetime.now().timestamp()

        mtb_rate = await self.coingecko_service.get_latest_price("metabomb", "usd")

        async with Client(transport=transport) as client:
            gql_result = await client.execute(
                self.__QUERY,
                variable_values=self.__params(1, 5000)
            )

            print(f"⏱  [{url}] {time.perf_counter() - start:0.3f}s")

            listings = gql_result["box_market"]["boxes"]

            dtos = []

            for listing in listings:

                dto = self.__map_dto(listing, mtb_rate, now)

                dtos.append(dto)

            return dtos

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

    __BOX_TYPES = {
        0: "Common Box",
        1: "Premium Box",
        2: "Ultra Box"
    }
    
    def __params(self, page, count):
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
