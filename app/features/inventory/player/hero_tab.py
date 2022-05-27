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
                        cell=__name_cell
                    ),
                    Column(
                        id="price",
                        title="MTB Value",
                        format=commify("$.price"),
                        width="120px",
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
