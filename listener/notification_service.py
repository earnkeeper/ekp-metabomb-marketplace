from ekp_sdk.services import RestClient


class NotificationService:
    def __init__(
        self,
        rest_client: RestClient,
        discord_base_url,
        discord_channel_id
    ):
        self.rest_client = rest_client
        self.discord_base_url = discord_base_url
        self.discord_channel_id = discord_channel_id

    async def send_notification(self, listing, floor_listing=None):
        seller = listing["seller"]
        masked_seller = f"{seller[0:5]}...{seller[-3:]}"
        name = listing["nftName"]
        fields = [
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
        ]

        if "hero" in listing:
            hero = listing["hero"]

            fields.append({
                "name": "Power",
                "value": str(hero["power"]),
                "inline": True
            })
            fields.append({
                "name": "Health",
                "value": str(hero["health"]),
                "inline": True
            })
            fields.append({
                "name": "Speed",
                "value": str(hero["speed"]),
                "inline": True
            })
            fields.append({
                "name": "Stamina",
                "value": str(hero["stamina"]),
                "inline": True
            })
            fields.append({
                "name": "Bomb num",
                "value": str(hero["bomb_num"]),
                "inline": True
            })
            fields.append({
                "name": "Bomb range",
                "value": str(hero["bomb_range"]),
                "inline": True
            })

            fields.append({
                "name": "Class",
                "value": hero["class"],
                "inline": True
            })

        if floor_listing is not None:
            fields.append({
                "name": "Floor USD",
                "value": f'$ {format(round(floor_listing["price_usdc"],2))}',
                "inline": True
            })


        embed = {
            "type": "rich",
            "title": "Metabomb Floor Alert!",
            "description": f'**{masked_seller}** has listed a **{name}** at lower than floor price!\n\n👀\n\n',
            "url": "https://app.metabomb.io",
            "color": 16215296,
            "image": {"url": listing["imageSrc"]},
            "fields": fields
        }

        await self.rest_client.post(
            f"{self.discord_base_url}/message/{self.discord_channel_id}",
            {"embeds": [embed]}
        )
