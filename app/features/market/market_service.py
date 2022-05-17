import time

from ekp_sdk.services import CacheService


class MarketService:
    def __init__(
        self,
        cache_service: CacheService
    ):
        self.cache_service = cache_service

    async def get_documents(self):
        docs = await self.cache_service.get("market_listings")

        if (docs == None):
            return []

        now = time.time()

        return list(map(lambda doc: self.format_document(doc, now), docs))

    def format_document(self, doc, now):
        return {
            "id": doc["id"],
            "updated": now,
            "name": f'Hero #{doc["id"]}',
            "display_id": doc["display_id"],
            "rarity": doc["rarity"],
            "level": doc["level"],
            "hero_class": doc["hero_class"],
            "hero_class_name": self.map_hero_class_name(doc["hero_class"]),
            "for_sale": doc["for_sale"],
            "price": doc["price"],
        }

    def map_hero_class_name(self, class_id):
        if (class_id == 0):
            return "Warrior"
        if (class_id == 1):
            return "Assassin"
        if (class_id == 2):
            return "Mage"
        if (class_id == 3):
            return "Support"
        if (class_id == 4):
            return "Ranger"
        return "?"
