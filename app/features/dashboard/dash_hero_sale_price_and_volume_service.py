from pprint import pprint

from db.market_sales_repo import MarketSalesRepo
from shared.mapper_service import MapperService
from shared.metabomb_coingecko_service import MetabombCoingeckoService
from dateutil import parser
import pytz
from datetime import datetime, date, time


def get_midnight_utc(dt=None):
    if dt is None:
        dt = datetime.now()

    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    dt = pytz.utc.localize(dt)

    return dt


class HeroSalePriceAndVolumeService:
    def __init__(
            self,
            market_sales_repo: MarketSalesRepo,
            metabomb_coingecko_service: MetabombCoingeckoService,
            mapper_service: MapperService
    ):
        self.market_sales_repo = market_sales_repo
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.mapper_service = mapper_service

    async def get_documents(self, currency, form_value):

        rate = await self.metabomb_coingecko_service.get_usd_price(currency["id"])

        results = list(
            self.market_sales_repo.collection.aggregate(
                [
                    {"$match":
                        {
                            "hero.hero.rarity_name": form_value
                        }
                    },
                    {
                        "$group":
                            {
                                "_id": {
                                    "$dateToString": {
                                        "format": "%Y-%m-%d",
                                        "date": {
                                            "$convert": {
                                                "input": {
                                                    "$multiply": [1000, "$timestamp"]
                                                },
                                                "to": "date"
                                            }
                                        }
                                    }
                                },
                                "number_of_sales": {"$sum": 1},
                                "price_avg": {"$avg": "$price"},
                                "price_avg_usd": {"$avg": "$priceUsd"}
                            }
                    }
                ])
        )

        # pprint(results)
        new_result_list = []
        for result in results:
            new_result_dict = {}
            dt = parser.parse(result['_id'])
            dtm = get_midnight_utc(dt)
            new_result_dict["timestamp_ms"] = int(dtm.timestamp()) * 1000
            new_result_dict["number_of_sales"] = result["number_of_sales"]
            new_result_dict["price_avg"] = result["price_avg"]
            new_result_dict["price_fiat_avg"] = result["price_avg_usd"] * rate
            new_result_list.append(new_result_dict)

        # pprint(new_result_list)

        # documents = list(grouped_by_date_str.values())

        return new_result_list
        # hero_list = await self.metabomb_api_service.get_market_heroes()
