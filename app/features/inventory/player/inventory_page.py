from app.features.inventory.player.box_tab import box_tab
from app.features.inventory.player.hero_tab import hero_tab
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span, Tabs, Tab, count, sum, format_currency

from app.utils.summary_card import summary_card


def page(HEROES_COLLECTION_NAME, BOXES_COLLECTION_NAME):
    return Container(
        children=[
            page_title('box', 'Inventory'),
            summary_row(HEROES_COLLECTION_NAME, BOXES_COLLECTION_NAME),
            Tabs(
                [
                    Tab(
                        label="Heroes",
                        children=[hero_tab(HEROES_COLLECTION_NAME)]
                    ),
                    Tab(
                        label="Boxes",
                        children=[box_tab(BOXES_COLLECTION_NAME)]
                    ),
                ]
            ),
        ],
    )


def summary_row(HEROES_COLLECTION_NAME, BOXES_COLLECTION_NAME):
    return Container(
        children=[
            Row([
                Col(
                    "col-auto",
                    [
                        summary_card(
                            "Total Heroes",
                            count(
                                f"$.{HEROES_COLLECTION_NAME}.*"
                            ),
                        ),
                    ]
                ),
                Col("col-auto", [
                    summary_card(
                        "Hero Market Value",
                        format_currency(
                            sum(
                                f"$.{HEROES_COLLECTION_NAME}..price_fiat"
                            ),
                            f"$.{HEROES_COLLECTION_NAME}[0].fiat_symbol"
                        ),
                    ),
                ]),
                Col(
                    "col-auto",
                    [
                        summary_card(
                            "Total Boxes",
                            sum(
                                f"$.{BOXES_COLLECTION_NAME}.*"
                            ),
                        ),
                    ]
                ),
                Col("col-auto", [
                    summary_card(
                        "Box Market Value",
                        format_currency(
                            sum(
                                f"$.{BOXES_COLLECTION_NAME}..price_fiat"
                            ),
                            f"$.{BOXES_COLLECTION_NAME}[0].fiat_symbol"
                        ),
                    ),
                ]),
            ])
        ]
    )
