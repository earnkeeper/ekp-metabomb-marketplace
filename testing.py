from ast import literal_eval
from pprint import pprint

from bson import SON
from pymongo import MongoClient

con_link = 'mongodb://localhost:27017/'
cluster = MongoClient(con_link)
db = cluster['metabomb']
collection_1 = db['market_sales']

# res = list(collection_1.find({"hash": "0xc0000fadb147fe589523d7d3648620fb171185a08689794c5acab5389103ebf3"}))[0]

# print(list(collection_1.find({"hero": SON([("hero", SON([("rarity_name", "Common")]))])})))

# pprint(list(collection_1.find({"hero.hero.rarity_name": "Common"})))

# result = list(
#     collection_1.aggregate(
#         [
#             {"$match":
#                 {
#                     "hero.hero.rarity_name": "Common"
#                 }
#             },
#             {
#                 "$group":
#                     {
#                         "_id": {
#                             "$dateToString": {
#                                 "format": "%Y-%m-%d",
#                                 "date": {
#                                     "$toDate": {
#                                         "multiply": [1000, "$timestamp"]
#                                     }
#                                 }
#                             }
#                         },
#                         "count": {"$sum": 1}
#                         # "total": {"$sum": f"$timestamp"}
#                     }
#             }
#         ])
# )

from dateutil import parser
import pytz
from datetime import datetime, date, time


def get_midnight_utc(dt=None):
    if dt is None:
        dt = datetime.now()

    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    dt = pytz.utc.localize(dt)

    return dt


results = list(
    collection_1.aggregate(
        [
            {"$match":
                {
                    "hero.hero.rarity_name": "Epic"
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
                        "price_avg": {"$avg": "$priceUsd"}
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
    new_result_list.append(new_result_dict)

pprint(new_result_list)
# print(res['input'])
# print(res['input'][10:74])
# print(literal_eval(res['input'][10:75]))
# print(literal_eval('8e9dff9d58e6da4ab5017566b73749bf98ce53c741d1b9e7732f2e63c9f993da'))
# print(int('000000000000000000000000000000000000000000000000000000000000000a', 16))
