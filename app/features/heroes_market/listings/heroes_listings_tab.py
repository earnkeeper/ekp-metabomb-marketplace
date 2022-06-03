from ekp_sdk.ui import (Col, Column, Container, Datatable, Div, Image, Link,
                        Paragraphs, Row, Span, collection, commify, documents,
                        format_currency, format_mask_address, format_percent,
                        format_template, is_busy, switch_case, format_age)

from app.utils.image_cell import image_cell
from shared.constants import HERO_CONTRACT_ADDRESS


def heroes_listings_tab(LISTINGS_COLLECTION_NAME):
    return Container(
        children=[
            Paragraphs(
                [
                    "Browse the live Metabomb Marketplace for the best deals.",
                    "The heroes with the best Return on Investment are shown at the top. (Based on Testnet gameplay mechanics) ",
                ],
            ),
            Div([], "mb-3"),
            market_row(LISTINGS_COLLECTION_NAME),
        ]
    )


def market_row(LISTINGS_COLLECTION_NAME):
    return Datatable(
        data=documents(LISTINGS_COLLECTION_NAME),
        busy_when=is_busy(collection(LISTINGS_COLLECTION_NAME)),
        default_sort_field_id="est_roi",
        default_sort_asc=False,
        pagination_per_page=18,
        disable_list_view=True,
        search_hint="Search by token id or token name...",
        filters=[
            {"columnId": "rarity_name", "icon": "cil-spa"},
            {"columnId": "level", "icon": "cil-shield-alt"},
        ],
        columns=[
            Column(
                id="last_listing_timestamp",
                title="Listed",
                sortable=True,
                cell=timestamp_cell(),
                width="120px"
            ),
            Column(
                id="tokenId",
                title="Token",
                sortable=True,
                searchable=True,
                width="80px",
                cell=__id_cell,
            ),
            Column(
                id="name",
                sortable=True,
                searchable=True,
                min_width="220px",
                cell=__name_cell
            ),
            Column(
                id="est_payback",
                title="Payback Period",
                format=format_template(
                    "{{ est_payback }} days",
                    {
                        "est_payback": "$.est_payback"
                    }
                ),
                width="120px",
                sortable=True,
            ),
            Column(
                id="est_roi",
                title="ROI",
                format=format_percent("$.est_roi"),
                width="100px",
                sortable=True,
            ),
            Column(
                id="price",
                title="Cost MTB",
                format=commify("$.price"),
                width="110px",
                sortable=True,
            ),
            Column(
                id="priceFiat",
                title="Cost Fiat",
                format=format_currency("$.priceFiat", "$.fiatSymbol"),
                width="110px",
                sortable=True,
            ),
            Column(
                id="avgPriceFiat",
                title="Vs 24h Avg",
                width="90px",
                sortable=True,
                cell=__avg_price_cell
            ),
            # Column(
            #     id="power",
            #     title="Power",
            #     cell=set_image(icon_name='stats-power',
            #                    attr_name='power'),
            #     width="80px",
            #     sortable=True,
            # ),
            Column(
                id="rarity_name",
                omit=True,
                title="Rarity"
            ),
            Column(
                id="level",
                omit=True
            ),
            Column(
                id="spacer",
                title="",
                width="2px"
            )
        ]
    )


__avg_price_cell = Span(
    format_percent("$.pcAboveAvgFiat"),
    switch_case("$.deal", {"no": "text-success", "yes": "text-danger"})
),


def set_image(icon_name, attr_name):
    return image_cell(
        f"https://app.metabomb.io/icons/stats-icon/{icon_name}.svg",
        f"$.{attr_name}",
        image_size="16px"
    )


__id_cell = Link(
    href=format_template(
        "https://bscscan.com/token/{{ contractAddress }}?a={{ tokenId }}",
        {
            "contractAddress": HERO_CONTRACT_ADDRESS,
            "tokenId": "$.tokenId"
        }
    ),
    external=True,
    content="$.tokenId"
)

__seller_cell = Link(
    href=format_template(
        "https://bscscan.com/address/{{ seller }}",
        {
            "seller": "$.seller",
        }
    ),
    external=True,
    content=format_mask_address("$.seller")
)


def image_text_cell(src, text):
    return Row([
        Col("col-auto my-auto", [
            Image(
                src=src,
                style={"width": "24px"}
            )
        ]),
        Col("pl-0 my-auto", [Span(text)])
    ])


__name_cell = image_text_cell(

    format_template("https://app.metabomb.io/gifs/char-gif/{{ display_id }}.gif", {
        "display_id": '$.display_id'
    }),
    "$.name"
)


def timestamp_cell():
    return Row([
        Col(
            class_name="my-auto col-auto pr-0",
            children=[
                Span(format_age("$.last_listing_timestamp"))
            ]
        ),
        # Col(
        #     class_name="my-auto col-auto pr-0",
        #     children=[
        #         Span(format_datetime("$.last_listing_timestamp"))
        #     ]
        # ),
    ])
