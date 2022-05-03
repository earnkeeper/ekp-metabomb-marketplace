from sdk import cache
import json

def documents():
    json_str = cache.get("metabomb_market_listings")

    if (json_str == None):
        return []
    docs = json.loads(cache.get("metabomb_market_listings"))
    return list(map(lambda doc: format_document(doc), docs))

def format_document(doc):
    return {
        "id": doc["id"],
        "name": f'Hero #{doc["id"]}',
        "display_id": doc["display_id"],
        "rarity": doc["rarity"],
        "level": doc["level"],
        "hero_class": doc["hero_class"],
        "for_sale": doc["for_sale"],
        "price": doc["price"],
    }