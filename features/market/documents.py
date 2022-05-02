from sdk import cache
import json

def documents():
    docs = json.loads(cache.get("metabomb_market_listings"))
    return list(map(lambda doc: format_document(doc), docs))

def format_document(doc):
    return {
        "id": doc["id"],
        "rarity": doc["rarity"],
        "level": doc["level"],
        "hero_class": doc["hero_class"],
        "for_sale": doc["for_sale"],
        "price": doc["price"],
    }