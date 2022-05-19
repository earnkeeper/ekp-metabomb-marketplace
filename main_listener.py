
from decouple import AutoConfig
from ekp_sdk import BaseContainer

from listener.listener_service import ListenerService
from sync.notification_service import NotificationService


class AppContainer(BaseContainer):
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
        
        self.listener_service = ListenerService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            web3_service=self.web3_service,
            notification_service=self.notification_service,
        )


if __name__ == '__main__':
    container = AppContainer()

    print("🚀 Application Start")

    container.listener_service.listen()
