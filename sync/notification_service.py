from db.market_listings_repo import MarketListingsRepo
from db.state_repo import StateRepo
from ekp_sdk.services import RestClient


class NotificationService:
    __STATE_ID = "notifications"

    def __init__(
        self,
        market_listings_repo: MarketListingsRepo,
        state_repo: StateRepo,
        rest_client: RestClient,
        discord_base_url,
        discord_channel_id
    ):
        self.market_listings_repo = market_listings_repo
        self.rest_client = rest_client
        self.state_repo = state_repo
        self.discord_base_url = discord_base_url
        self.discord_channel_id = discord_channel_id

    async def process_notifications(self):
        state = self.state_repo.find("notifications")

        if state is None:
            latest_block = self.market_listings_repo.find_latest_block_number()
            state = {
                "id": self.__STATE_ID,
                "market_listings_latest_block": latest_block
            }
            self.state_repo.save([state])
            print("✅ Finished notification check")            
            return

        latest_block = state["market_listings_latest_block"]

        listings = self.market_listings_repo.find_since_block_number(
            latest_block + 1,
            1000
        )

        if not len(listings):
            return

        for listing in listings:
            block_number = listing["blockNumber"]
            latest_block = block_number

            await self.send_notification(listing)

        new_state = {
            "id": self.__STATE_ID,
            "market_listings_latest_block": latest_block
        }
        
        self.state_repo.save([new_state])
        
        print("✅ Finished notification check")

    async def send_notification(self, listing):
        seller = listing["seller"]
        name = listing["nftName"]
        imageUrl = self.__HERO_BOX_NAME_IMAGE[name]
        embed = {
            "type": "rich",
            "title": "New Hero Box Listed!",
            "description": "A new Hero Box has been added to the Metabomb Marketplace\n\n👀",
            "url": "https://app.metabomb.io/trade/boxes",
            "color": 16215296,
            "image": {"url": imageUrl},
            "fields": [
                {
                    "name": "Name",
                    "value": name,
                    "inline": True
                },
                {
                    "name": "Token Id",
                    "value": str(listing["tokenId"]),
                    "inline": True
                },
                {
                    "name": "Seller",
                    "value": f'{seller[0:5]}...{seller[-3:]}',
                    "inline": True
                },

                {
                    "name": "MTB",
                    "value": format(int(listing["price"]), ",d"),
                    "inline": True
                },
                {
                    "name": "USD",
                    "value": f'$ {format(round(listing["priceUsd"],2))}',
                    "inline": True
                },
            ]
        }
        
        await self.rest_client.post(
            f"{self.discord_base_url}/message/{self.discord_channel_id}",
            {"embeds": [embed]}
        )

    __HERO_BOX_NAME_IMAGE = {
        "Common Box": "https://app.metabomb.io/gifs/herobox-gif/normal-box.gif",
        "Premium Box": "https://app.metabomb.io/gifs/herobox-gif/premium-box.gif",
        "Ultra Box": "https://app.metabomb.io/gifs/herobox-gif/ultra-box.gif"
    }
