from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.image_cell import image_cell
from ekp_sdk.ui import (Card, Chart, Column, Container, Datatable, Span,
                        collection, commify, documents, format_currency,
                        format_template, is_busy, switch_case)


def box_tab(BOXES_COLLECTION_NAME):
    return Container(
        children=[
            Datatable(
                data=documents(BOXES_COLLECTION_NAME),
                busy_when=is_busy(collection(BOXES_COLLECTION_NAME)),
                filters=[
                    {"columnId": "name", "icon": "cil-spa"},
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
                        id="priceFiat",
                        title="Fiat Value",
                        format=format_currency(
                            "$.price_fiat", "$.fiat_symbol"),
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                ]
            )
        ]
    )


__name_cell = image_cell(
    switch_case(
        "$.name",
        HERO_BOX_NAME_IMAGE
    ),
    "$.name"
)