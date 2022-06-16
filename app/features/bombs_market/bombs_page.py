from ekp_sdk.ui import (Card, Col, Container, Div, Image, Row, Span, Tab, Tabs,
                        format_currency, format_template, switch_case, Paragraphs)
from app.features.bombs_market.history.bombs_history_tab import history_tab
from app.features.bombs_market.listings.bomb_listings_tab import bomb_listings_tab
from app.utils.game_constants import METABOMB_IMAGE_URL

from app.utils.page_title import page_title

def bombs_page(
        BOMBS_HISTORY_COLLECTION_NAME,
        BOMBS_LISTINGS_COLLECTION_NAME,
        BOMBS_SUMMARY_COLLECTION_NAME
):
    return Container(
        children=[
            page_title('shopping-bag', 'Bomb Market'),
            Paragraphs(
                [
                    "Browse the live Metabomb Bomb Market for the best deals on bombs. 🤔 Bombs with skill 5 increase earning by 100%, look out for deals on these ones.",
                    "Click the History tab to browse the last 1000 sales from the bomb Marketplace. Check out our discord for real time notifications of new listings.",
                ],
            ),
            summary_row(BOMBS_SUMMARY_COLLECTION_NAME),
            Tabs(
                [
                    Tab(
                        label="Listings",
                        children=[bomb_listings_tab(BOMBS_LISTINGS_COLLECTION_NAME)]
                    ),
                    Tab(
                        label="History",
                        children=[history_tab(BOMBS_HISTORY_COLLECTION_NAME)]
                    ),
                ]
            ),
        ]
    )


def summary_row(SUMMARY_COLLECTION_NAME):
    return Container(
        context=f"$.{SUMMARY_COLLECTION_NAME}[0]",
        children=[
            Row([
                Col("col-auto", [
                    summary_card("common"),
                ]),
                Col("col-auto", [
                    summary_card("rare"),
                ]),
                Col("col-auto", [
                    summary_card("epic"),
                ]),
                Col("col-auto", [
                    summary_card("legend"),
                ]),
            ])
        ]
    )


def summary_card(bombId):
    return Container(
        context=f"$.{bombId}",
        children=[
            Div(
                children=[
                    Card(
                        class_name="p-1",
                        children=[
                            Row([
                                Col("col-auto my-auto pr-0", [
                                    Image(
                                        src=format_template(METABOMB_IMAGE_URL + "/gifs/bomb-gif/{{ display_id }}.gif",
                                                            {
                                                                "display_id": '$.display_id'
                                                            }),
                                        style={"height": "64px"}
                                    )
                                ]),
                                Col("col-auto pr-4", [
                                    Span("$.name", "font-medium-3 font-weight-bold d-block"),
                                    Span(
                                        content=format_template(
                                            "Floor Price: {{ price }}",
                                            {
                                                "price": format_currency("$.floorPrice", "$.fiatSymbol")
                                            }
                                        ),
                                        class_name="font-small-2 d-block"
                                    ),
                                    Div(style={"marginBottom": "2px"}),
                                    Span(
                                        content=format_template(
                                            "24h Avg Price: {{ price }}",
                                            {
                                                "price": format_currency("$.avgPrice", "$.fiatSymbol")
                                            }
                                        ),
                                        class_name="font-small-2 d-block"
                                    )
                                ]),

                            ])
                        ])
                ],
                when="$.display_id"
            )
        ]
    )
