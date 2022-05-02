import requests


def latest_price(tokenId, fiatId):
    if (tokenId == "usd-coin" and fiatId == "usd"):
        return 1

    response = requests.get(
        f'https://api.coingecko.com/api/v3/simple/price?ids={tokenId}&vs_currencies={fiatId}')

    return response.json()[tokenId][fiatId]
