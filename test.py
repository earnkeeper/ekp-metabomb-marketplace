
from web3.auto import Web3, w3
from decouple import config


provider_url = config("WEB3_PROVIDER_URL")

w3 = Web3(Web3.HTTPProvider(provider_url))


print(w3.eth.get_block(17937338))