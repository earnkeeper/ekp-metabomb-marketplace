import asyncio
import json
import logging
from ast import literal_eval

from ekp_sdk.services import CacheService, CoingeckoService, Web3Service
from shared.metabomb_api_service import MetabombApiService
from web3 import Web3

from listener.notification_service import NotificationService

COMMON_BOX_CONTRACT_ADDRESS = "0x1f36bef063ee6fcefeca070159d51a3b36bc68d6"
PREMIUM_BOX_CONTRACT_ADDRESS = "0x2076626437c3bb9273998a5e4f96438abe467f1c"
ULTRA_BOX_CONTRACT_ADDRESS = "0x9341faed0b86208c64ae6f9d62031b1f8a203240"


class ListenerService:
    def __init__(
        self,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        notification_service: NotificationService,
        metabomb_api_service: MetabombApiService,
        web3_service: Web3Service,
    ):
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.metabomb_api_service = metabomb_api_service
        self.notification_service = notification_service
        self.web3_service = web3_service

    def listen(self):
        common_filter = self.web3_service.get_filter({
            "address": Web3.toChecksumAddress(COMMON_BOX_CONTRACT_ADDRESS),
            "topics": ["0xe04eefd2590e9186abb360fc0848592add67dcef57f68a4110a6922c4793f7e0"]
        })

        premium_filter = self.web3_service.get_filter({
            "address": Web3.toChecksumAddress(PREMIUM_BOX_CONTRACT_ADDRESS),
            "topics": ["0xe04eefd2590e9186abb360fc0848592add67dcef57f68a4110a6922c4793f7e0"]
        })

        ultra_filter = self.web3_service.get_filter({
            "address": Web3.toChecksumAddress(ULTRA_BOX_CONTRACT_ADDRESS),
            "topics": ["0xe04eefd2590e9186abb360fc0848592add67dcef57f68a4110a6922c4793f7e0"]
        })

        loop = asyncio.get_event_loop()

        loop.run_until_complete(
            asyncio.gather(
                self.filter_loop(common_filter, 2),
                self.filter_loop(premium_filter, 2),
                self.filter_loop(ultra_filter, 2),
            )
        )

    async def filter_loop(self, filter, poll_interval):
        while True:
            try:
                for new_event in filter.get_new_entries():
                    listing = await self.decode_market_listing(json.loads(Web3.toJSON(new_event)))
                    await self.process_market_listing(listing)

                await asyncio.sleep(poll_interval)
            except Exception as e:
                logging.error("🚨 error while listening for events", e)

    async def decode_market_listing(self, log):
        hash = log["transactionHash"]

        logging.info(f"🐛 Decoding log: {hash}")

        address = log["address"].lower()

        data = log["data"]

        if len(data) < 66:
            return

        block_number = log["blockNumber"]
        tran = await self.web3_service.get_transaction(hash)
        block = await self.web3_service.get_block(block_number)

        timestamp = block["timestamp"]
        topics = log["topics"]

        mtb_cache_key = f"mtb_price_events"
        mtb_usd_price = await self.cache_service.wrap(mtb_cache_key, lambda: self.coingecko_service.get_latest_price("metabomb", "usd"), ex=60)

        price = Web3.fromWei(literal_eval(data[0:66]), 'ether')
        token_id = literal_eval(topics[1])

        name = None
        if address == COMMON_BOX_CONTRACT_ADDRESS:
            name = "Common Box"
        if address == PREMIUM_BOX_CONTRACT_ADDRESS:
            name = "Premium Box"
        if address == ULTRA_BOX_CONTRACT_ADDRESS:
            name = "Ultra Box"

        listing = {
            "blockNumber": block_number,
            "seller": tran["from"],
            "hash": hash,
            "nftName": name,
            "nftType": "Hero Box",
            "price": float(price),
            "priceUsd": float(price) * mtb_usd_price,
            "timestamp": timestamp,
            "tokenId": token_id,
        }

        return listing

    async def process_market_listing(self, listing):
        logging.info(f"🐛 Processing listing: {listing['hash']}")

        current_listings = await self.cache_service.wrap("listener_market_listings", lambda: self.metabomb_api_service.get_market_boxes(), ex=60)

        box_type_listings = filter(
            lambda x: x["box_type"] == listing["nftName"], current_listings)

        box_type_listings_sorted = sorted(
            box_type_listings, key=lambda x: x["price_mtb"])

        floor_listing = box_type_listings_sorted[0]

        if (listing["price"] < floor_listing["price_mtb"]):
            await self.notification_service.send_notification(listing, floor_listing)
            logging.info(f"📣 Listing sent to discord: {listing['hash']}")            
        else:
            logging.warn(
                f'⚠️ not notifying listing, price ({int(listing["price"])}) is not lower than floor price ({floor_listing["price_mtb"]})'
            )
