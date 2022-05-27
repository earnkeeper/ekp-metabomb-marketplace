from app.features.inventory.player.box_tab import box_tab
from app.features.inventory.player.hero_tab import hero_tab
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span, Tabs, Tab, count, sum, format_currency, Icon, Link, format_template, Div

from app.utils.summary_card import summary_card


def page(HEROES_COLLECTION_NAME, BOXES_COLLECTION_NAME):
    return Container(
        children=[
            Row(
                children=[
                    Col(
                        class_name='col-auto pr-0 my-auto',
                        children=[
                            Icon(
                                size="lg",
                                name="user"
                            )
                        ],
                    ),
                    Col(
                        class_name="my-auto",
                        children=[
                            Span("Inventory", "font-large-1")
                        ]
                    ),
                ],
            ),
            Div([], "mt-1"),            
            Link(
                content={
                    "method": "replace",
                    "params": ["$.shared.client.path", "inventory/", ""]
                },
                class_name="d-block font-small-2",
                external_icon=True,
                external=True,
                href=format_template(
                    "https://bscscan.com/address/{{ address }}",
                    {
                        "address": {
                            "method": "replace",
                            "params": ["$.shared.client.path", "inventory/", ""]
                        }
                    }
                )
            ),
            Div([], "mt-1"),
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
                            count(
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
