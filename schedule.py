import json

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from sdk import cache


def query():
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


def params(page, count):
    return {
        "input": {
            "f5": 0,
            "rarity": [
                0,
                1,
                2,
                3,
                4,
                5
            ],
            "class_hero": [
                0,
                1,
                2,
                3,
                4
            ],
            "power": [
                1,
                18
            ],
            "speed": [
                1,
                18
            ],
            "health": [
                1,
                18
            ],
            "stamina": [
                1,
                18
            ],
            "bomb_num": [
                1,
                4
            ],
            "bomb_range": [
                1,
                4
            ],
            "level": [
                0,
                6
            ],
            "page": page,
            "count": count,
            "sort": 0,
            "sort_type": 1,
            "forSale": 2
        }
    }


if __name__ == '__main__':
    transport = RequestsHTTPTransport(url="https://api.metabomb.io/graphql/")

    client = Client(transport=transport)

    result = client.execute(query(), variable_values=params(1, 5000))

    listings = result["hero_market"]["heroes"]

    print(f"Fetched {len(listings)} market listings")

    cache.set("metabomb_market_listings", json.dumps(listings))
