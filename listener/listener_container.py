
from decouple import AutoConfig
from ekp_sdk import BaseContainer
from shared.metabomb_api_service import MetabombApiService

from listener.listener_service import ListenerService
from listener.notification_service import NotificationService


class ListenerContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        DISCORD_BASE_URL = config("DISCORD_BASE_URL")
        DISCORD_CHANNEL_ID = config("DISCORD_CHANNEL_ID")

        self.notification_service = NotificationService(
            rest_client=self.rest_client,
            discord_base_url=DISCORD_BASE_URL,
            discord_channel_id=DISCORD_CHANNEL_ID,
        )
        self.metabomb_api_service = MetabombApiService(
            coingecko_service=self.coingecko_service
        )
        self.listener_service = ListenerService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            metabomb_api_service=self.metabomb_api_service,
            notification_service=self.notification_service,
            web3_service=self.web3_service,
        )