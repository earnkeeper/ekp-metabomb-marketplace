from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.image_cell import image_cell
from ekp_sdk.ui import (Card, Chart, Column, Container, Datatable, Span,
                        collection, commify, documents, format_currency,
                        format_template, is_busy)


def hero_tab(HEROES_COLLECTION_NAME):
    return Container(
        children=[
            Datatable(
                data=documents(HEROES_COLLECTION_NAME),
                busy_when=is_busy(collection(HEROES_COLLECTION_NAME)),
                filters=[
                    {"columnId": "rarity_name", "icon": "cil-spa"},
                    {"columnId": "level", "icon": "cil-shield-alt"},
                ],
                columns=[
                    Column(
                        id="id",
                        title="Token Id",
                        width="100px"
                    ),
                    Column(
                        id="name",
                        cell=__name_cell,
                        width='200px'
                    ),
                    Column(
                        id="hero_power",
                        title="Power",
                        width="100px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_health",
                        title="Health",
                        width="100px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_speed",
                        title="Speed",
                        width="100px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_stamina",
                        title="Stamina",
                        width="100px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_bomb_num",
                        title="Bomb num",
                        width="100px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_bomb_range",
                        title="Bomb range",
                        width="100px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="price",
                        title="MTB Value",
                        format=commify("$.price"),
                        width="100px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="price_fiat",
                        title="Fiat Value",
                        format=format_currency("$.price_fiat", "$.fiat_symbol"),
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="rarity_name",
                        omit=True,
                        title="Rarity"
                    ),
                    Column(
                        id="level",
                        omit=True
                    ),

                ]
            )
        ]
    )


__name_cell = image_cell(
    format_template("https://app.metabomb.io/gifs/char-gif/{{ display_id }}.gif", {
        "display_id": '$.display_id'
    }),
    "$.name"
)
