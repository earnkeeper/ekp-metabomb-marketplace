from db.market_listings_repo import MarketListingsRepo
from db.state_repo import StateRepo



class NotificationService:
    __STATE_ID = "notifications"

    def __init__(
        self,
        market_listings_repo: MarketListingsRepo,
        state_repo: StateRepo,
    ):
        self.market_listings_repo = market_listings_repo
        self.state_repo = state_repo

    async def process_notifications(self):
        state = self.state_repo.find("notifications")

        if state is None:
            latest_block = self.market_listings_repo.find_latest_block_number()
            state = {
                "id": self.__STATE_ID,
                "market_listings_latest_block": latest_block
            }
            self.state_repo.save([state])
            return

        latest_block = state["market_listings_latest_block"]

        listings = self.market_listings_repo.find_since_block_number(
            latest_block,
            1000
        )

        if not len(listings):
            return

        for listing in listings:
            block_number = listing["blockNumber"]
            latest_block = block_number

            self.send_notification(listing)

    def send_notification(self, listing):
        print("📣  SEND NOTIFICATION")
