from ekp_sdk.services import RestClient


class NotificationService:
    __STATE_ID = "notifications"

    def __init__(
        self,
        rest_client: RestClient,
        discord_base_url,
        discord_channel_id
    ):
        self.rest_client = rest_client
        self.discord_base_url = discord_base_url
        self.discord_channel_id = discord_channel_id

    async def send_notification(self, listing, floor_listing):
        seller = listing["seller"]
        masked_seller = f"{seller[0:5]}...{seller[-3:]}"
        name = listing["nftName"]
        imageUrl = self.__HERO_BOX_NAME_IMAGE[name]
        embed = {
            "type": "rich",
            "title": "Metabomb Floor Alert!",
            "description": f'**{masked_seller}** has listed a **{name}** at lower than floor price!\n\n👀\n\n',
            "url": "https://app.metabomb.io/trade/boxes",
            "color": 16215296,
            "image": {"url": imageUrl},
            "fields": [
                {
                    "name": "Token Id",
                    "value": str(listing["tokenId"]),
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
                {
                    "name": "Floor USD",
                    "value": f'$ {format(round(floor_listing["price_usdc"],2))}',
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
