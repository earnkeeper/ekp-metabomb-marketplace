from typing import TypedDict

from shared.domain.hero import Hero
from shared.domain.hero_box import HeroBox
from typing_extensions import NotRequired


class MarketListing(TypedDict):
    hash: NotRequired[str]
    box: NotRequired[HeroBox]
    for_sale: bool
    hero: NotRequired[Hero]
    id: int
    listed: NotRequired[int]
    price_mtb: int
    price_usdc: float
    seller: NotRequired[str]
    token_id: str
    updated: int
