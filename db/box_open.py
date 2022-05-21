from typing import TypedDict


class BoxOpen(TypedDict):
    address: str
    block_number: int
    box_token_id: int
    box_type: str
    hash: str
    hero_rarity: int
    hero_token_id: int
    timestamp: int