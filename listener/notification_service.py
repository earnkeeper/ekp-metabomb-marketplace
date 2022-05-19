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
