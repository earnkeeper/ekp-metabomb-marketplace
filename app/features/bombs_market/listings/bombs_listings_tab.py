from ekp_sdk.ui import (Col, Column, Container, Datatable, Div, Image, Link,
                        Paragraphs, Row, Span, commify,
                        format_currency, format_mask_address, format_percent,
                        format_template, is_busy, switch_case, format_age)
from ekp_sdk.util import documents, collection
from ekp_sdk.util.clean_null_terms import clean_null_terms

from app.utils.game_constants import MTB_ICON, METABOMB_IMAGE_URL
from app.utils.image_cell import image_cell
from shared.constants import BOMB_CONTRACT_ADDRESS


def bombs_listings_tab(LISTINGS_COLLECTION_NAME):
    return Container(
        children=[
            Paragraphs(
                [
                    "Browse the live Metabomb Marketplace for the best deals.",
                    # "The bombs with the best Return on Investment are shown at the top. (Based on Testnet gameplay mechanics) ",
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
        # default_sort_field_id="est_roi",
        default_sort_asc=False,
        pagination_per_page=18,
        disable_list_view=True,
        search_hint="Search by token id or token name...",
        # filters=[
        #     {"columnId": "rarity_name", "icon": "cil-spa"},
        #     {"columnId": "level", "icon": "cil-shield-alt"},
        # ],
        columns=[
            Column(
                id="last_listing_timestamp",
                title="Listed",
                sortable=True,
                cell=timestamp_cell(),
                width="120px"
            ),
            Column(
                id="item",
                value="$.name",
                title="Item",
                sortable=True,
                searchable=True,
                cell=name_cell(),
                min_width="200px"
            ),
            Column(
                id="skills",
                title="Skills",
                cell=skills_cell(),
                min_width="200px"
            ),
            Column(
                id="priceFiat",
                title="Cost",
                sortable=True,
                searchable=True,
                cell=cost_cell(),
                min_width="100px"
            ),
            Column(
                id="avgPriceFiat",
                title="Vs 24h Avg",
                width="120px",
                sortable=True,
                cell=__avg_price_cell
            ),
            Column(
                id="rarity_name",
                omit=True,
                title="Rarity"
            ),

            Column(
                id="spacer",
                title="",
                width="2px"
            )
        ]
    )

def skills_cell():
    return Row(
        children=[
            skill_col(s_id) for s_id in range(1, 7)
            # skill_col("1"),
            # skill_col("2"),
            # skill_col("3"),
            # skill_col("4"),
            # skill_col("5"),
            # skill_col("6"),
        ]
    )
# onerror="this.style.display='none'"
def skill_col(skill_id):
    return Col(
        class_name="my-auto col-auto pr-0",
        children=[
            Image(
                src=format_template(METABOMB_IMAGE_URL + "/icons/skill-icon/skill-{{ skill_id }}.png", {
                    "skill_id": f"$.skill_{skill_id}"
                }),
                style={"height": "20px", "border-radius": "50%"},
                when=f"$.skill_{skill_id}"
            )
        ]
    )

def earn_cell():
    return Row(
        children=[
            Col(
                class_name="col-12",
                children=[
                    Span(
                        format_template(
                            "{{ est_payback }} days", {
                                "est_payback": "$.est_payback"
                            }
                        ),
                    )
                ]
            ),
            Col(
                class_name="col-12",
                children=[
                    Row([
                        Col(
                            "col-auto pr-0",
                            [
                                Image(
                                    src=MTB_ICON,
                                    style={
                                        "height": "10px",
                                        "marginRight": "3px",
                                        "marginTop": "-2px"
                                    }
                                )
                            ]
                        ),
                        Col(
                            "col-auto pl-0",
                            [
                                Span(
                                    format_template(
                                        "{{ mtb_per_day }} /day",
                                        {
                                            "mtb_per_day": commify("$.mtb_per_day")
                                        }
                                    ),
                                    "font-small-1 text-success"
                                )
                            ]
                        )
                    ])
                ]
            ),
        ]
    )


def cost_cell():
    return Row([
        Col(
            class_name="col-12",
            children=[
                Span(
                    format_currency("$.priceFiat", "$.fiatSymbol"),
                ),
            ]
        ),
        Col(
            class_name="col-12 font-small-1",
            children=[
                Row([
                    Col(
                        class_name="col-auto pr-0 my-auto",
                        children=[
                            Image(
                                src=MTB_ICON,
                                style={
                                    "height": "10px",
                                    "marginRight": "3px",
                                    "marginTop": "-2px"
                                }
                            )
                        ]
                    ),
                    Col(
                        class_name="col-auto pl-0 my-auto text-success",
                        children=[
                            Span(commify("$.price"))
                        ]
                    )
                ])

            ]
        ),
    ])


def name_cell():
    return Row(
        children=[
            Col(
                class_name="my-auto col-auto pr-0",
                children=[
                    Image(
                        src=format_template(METABOMB_IMAGE_URL + "/gifs/bomb-gif/{{ display_id }}.gif", {
                            "display_id": '$.display_id'
                        }),
                        style={"height": "50px"}
                    )
                ]
            ),
            Col(
                children=[
                    Row(
                        children=[
                            Col(
                                class_name="col-12 font-small-4",
                                children=[
                                    Row(
                                        children=[
                                            Col(
                                                class_name="col-auto my-auto pr-0",
                                                children=[
                                                    Span("$.name")
                                                ]
                                            ),
                                            Col(
                                                class_name="col-auto my-auto",
                                                children=[
                                                    Image(
                                                        src=format_template(
                                                            METABOMB_IMAGE_URL + "/icons/element-icon/{{ element }}.png",
                                                            {
                                                                "element": '$.element'
                                                            }),
                                                        style={"height": "14px"}
                                                    )
                                                ]
                                            )

                                        ]
                                    )
                                ]
                            ),
                            Col(
                                class_name="col-12",
                                children=[
                                    Link(
                                        class_name="font-small-1",
                                        href=format_template(
                                            "https://bscscan.com/token/{{ contractAddress }}?a={{ tokenId }}",
                                            {
                                                "contractAddress": BOMB_CONTRACT_ADDRESS,
                                                "tokenId": "$.tokenId"
                                            }
                                        ),
                                        external=True,
                                        content=format_template(
                                            "Token Id: {{ tokenId }}",
                                            {
                                                "tokenId": "$.tokenId"
                                            }
                                        ),
                                    )
                                ]
                            )
                        ]
                    )

                ]
            )

        ]
    )


__avg_price_cell = Span(
    format_percent("$.pcAboveAvgFiat"),
    switch_case("$.deal", {"no": "text-success", "yes": "text-danger"})
),


def set_image(icon_name, attr_name):
    return image_cell(
        f"{METABOMB_IMAGE_URL}/icons/stats-icon/{icon_name}.svg",
        f"$.{attr_name}",
        image_size="16px"
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

    format_template(METABOMB_IMAGE_URL + "/gifs/char-gif/{{ display_id }}.gif", {
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
