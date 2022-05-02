
from features.market.controller import MarketController
from sdk.client_service import ClientService
from sdk.gateway_service import GatewayService

gateway_service = GatewayService()
client_service = ClientService(gateway_service.sio)

gateway_service.add_controller(MarketController(client_service))

if __name__ == '__main__':
    gateway_service.listen()
