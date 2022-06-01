from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService

class HeroFloorPriceService:
    def __init__(
        self,
        metabomb_api_service: MetabombApiService,
        mapper_service: MapperService
    ):
        self.metabomb_api_service = metabomb_api_service
        self.mapper_service = mapper_service
        
    async def get_floor_prices(self):
        listings = await self.metabomb_api_service.get_market_heroes()
        
        floor_prices = {
            "Common": None,
            "Rare": None,
            "Epic": None,
            "Legend": None,
            "Mythic": None,
            "Meta": None,
        }
        
        for listing in listings:
            price = listing["price"]
            rarity_name = self.mapper_service.HERO_RARITY_TO_NAME[listing['rarity']]
            
            if (not floor_prices[rarity_name]) or (price < floor_prices[rarity_name]):
                floor_prices[rarity_name] = price

        return floor_prices