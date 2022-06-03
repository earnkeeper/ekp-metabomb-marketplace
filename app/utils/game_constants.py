from shared.constants import COMMON_BOX_CONTRACT_ADDRESS, PREMIUM_BOX_CONTRACT_ADDRESS, ULTRA_BOX_CONTRACT_ADDRESS, \
    BOMB_BOX_CONTRACT_ADDRESS


def rarity_names():
    return {
        0: "Common",
        1: "Rare",
        2: "Epic",
        3: "Legend",
        4: "Mythic",
        5: "Meta",
    }


def class_names():
    return {
        0: "Warrior",
        1: "Assassin",
        2: "Mage",
        3: "Support",
        4: "Ranger",
    }


HERO_BOX_NAME_CONTRACT = {
    "Common Box": COMMON_BOX_CONTRACT_ADDRESS,
    "Premium Box": PREMIUM_BOX_CONTRACT_ADDRESS,
    "Ultra Box": ULTRA_BOX_CONTRACT_ADDRESS,
    "Bomb Box": BOMB_BOX_CONTRACT_ADDRESS
}

HERO_BOX_NAME_IMAGE = {
    "Common Box": "https://app.metabomb.io/gifs/herobox-gif/normal-box.gif",
    "Premium Box": "https://app.metabomb.io/gifs/herobox-gif/premium-box.gif",
    "Ultra Box": "https://app.metabomb.io/gifs/herobox-gif/ultra-box.gif",
    "Bomb Box": "https://app.metabomb.io/gifs/herobox-gif/bomb-box.gif"
}

MTB_ICON = "https://app.metabomb.io/icons/mtb-token.png"
