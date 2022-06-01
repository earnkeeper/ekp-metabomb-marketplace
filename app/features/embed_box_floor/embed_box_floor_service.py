from datetime import datetime


class EmbedBoxesService:
    def get_documents(self, listing_documents, history_documents, currency):
        # pprint(listing_documents)
        floor_prices = {
            "Common Box": None,
            "Premium Box": None,
            "Ultra Box": None,
        }

        avg_prices = {
            "Common Box": None,
            "Premium Box": None,
            "Ultra Box": None,
        }

        count_boxes = {
            "Common Box": 0,
            "Premium Box": 0,
            "Ultra Box": 0,
        }
        perc_difference = {
            "Common Box": None,
            "Premium Box": None,
            "Ultra Box": None,
        }

        for listing in listing_documents:
            price_fiat = listing["priceFiat"]
            avg_price_fiat = listing["avgPriceFiat"]
            name = listing['name']
            count_boxes[name] += 1
            if (not floor_prices[name]) or (price_fiat < floor_prices[name]):
                floor_prices[name] = price_fiat
            if (not avg_prices[name]) and avg_price_fiat:
                avg_prices[name] = avg_price_fiat
            perc_difference[name] = None
            if floor_prices[name] and avg_prices[name]:
                perc_difference[name] = (floor_prices[name] - avg_prices[name]) / avg_prices[name] * 100

        return [
            {
                "id": "0",
                "updated": datetime.now().timestamp(),
                "common": {
                    "name": "Common Box",
                    "countBoxes": count_boxes["Common Box"],
                    "percDiff": perc_difference["Common Box"],
                    "floorPrice": floor_prices["Common Box"],
                    "avgPrice": avg_prices["Common Box"],
                    "fiatSymbol": currency["symbol"],
                    "color": "danger" if perc_difference["Common Box"] and perc_difference[
                        "Common Box"] < 0 else "success"
                },
                "premium": {
                    "name": "Premium Box",
                    "countBoxes": count_boxes["Premium Box"],
                    "percDiff": perc_difference["Premium Box"],
                    "floorPrice": floor_prices["Premium Box"],
                    "avgPrice": avg_prices["Premium Box"],
                    "fiatSymbol": currency["symbol"],
                    "color": "danger" if perc_difference["Premium Box"] and perc_difference[
                        "Premium Box"] < 0 else "success"
                },
                "ultra": {
                    "name": "Ultra Box",
                    "countBoxes": count_boxes["Ultra Box"],
                    "percDiff": perc_difference["Ultra Box"],
                    "floorPrice": floor_prices["Ultra Box"],
                    "avgPrice": avg_prices["Ultra Box"],
                    "fiatSymbol": currency["symbol"],
                    "color": "danger" if perc_difference["Ultra Box"] and perc_difference[
                        "Ultra Box"] < 0 else "success"
                },
            }
        ]
