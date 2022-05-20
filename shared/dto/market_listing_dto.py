from typing import TypedDict


class MarketListingDto(TypedDict):
    box_type: str
    chain_process: int
    for_sale: bool
    id: int
    price_mtb: int
    price_usdc: float
    token_id: str
    type: str
    updated: int
    wallet_address: str
