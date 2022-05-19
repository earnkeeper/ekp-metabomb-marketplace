from ekp_sdk.db import MgClient
from pymongo import DESCENDING, UpdateOne
import time

class MarketListingsRepo:
    def __init__(
        self,
        mg_client: MgClient
    ):
        self.mg_client = mg_client

        self.collection = self.mg_client.db['market_listings']
        self.collection.create_index("hash", unique=True)
        self.collection.create_index("blockNumber")
        self.collection.create_index("nftName")
        self.collection.create_index("nftType")
        self.collection.create_index("seller")
        self.collection.create_index("timestamp")
        self.collection.create_index("tokenId")

    def find_latest_block_number(self):
        results = list(
            self.collection
            .find()
            .sort("blockNumber", -1)
            .limit(1)
        )
        
        if not len(results):
            return 0
        
        return results[0]["blockNumber"]
    
    def find_since_block_number(self, block_number, limit):
        start = time.perf_counter()
        
        results = list(
            self.collection
            .find({"blockNumber": {"$gte": block_number}})
            .sort("blockNumber")
            .limit(limit)
        )
        
        print(f"⏱  [MarketListingsRepo.find_since_block_number({len(results)})] {time.perf_counter() - start:0.3f}s")        
        
        return results

    def save(self, models):
        
        start = time.perf_counter()
                
        self.collection.bulk_write(
            list(map(lambda model: UpdateOne(
                {"hash": model["hash"]}, {"$set": model}, True), models))
        )
        
        print(f"⏱  [MarketListingsRepo.save({len(models)})] {time.perf_counter() - start:0.3f}s")

