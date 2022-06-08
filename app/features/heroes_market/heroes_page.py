from ekp_sdk.ui import (Card, Col, Container, Div, Image, Row, Span, Tab, Tabs,
                        format_currency, format_template, switch_case, Alert)
from app.features.heroes_market.history.heroes_history_tab import history_tab
from app.features.heroes_market.listings.heroes_listings_tab import heroes_listings_tab
from app.utils.page_title import page_title

def heroes_page(HISTORY_COLLECTION_NAME, HERO_LISTINGS_COLLECTION_NAME, HERO_SUMMARY_COLLECTION_NAME):
    return Container(
        children=[
            Alert(
                "Metabomb is currently under maintenance, preparing for their official launch today. This page may encounter errors.",
                header="Attention",
                icon_name="bell"
            ),
            Div([], "mb-4"),
            page_title('shopping-bag', 'Hero Market'),
            summary_row(HERO_SUMMARY_COLLECTION_NAME),
            Tabs(
                [
                    Tab(
                        label="Listings",
                        children=[heroes_listings_tab(HERO_LISTINGS_COLLECTION_NAME)]
                    ),
                    Tab(
                        label="History",
                        children=[history_tab(HISTORY_COLLECTION_NAME)]
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


def summary_card(boxId):
    return Container(
        context=f"$.{boxId}",
        children=[
            Card(
                class_name="p-1",
                children=[
                    Row([
                        Col("col-auto my-auto", [
                            Image(
                                src=format_template("https://app.metabomb.io/gifs/char-gif/{{ display_id }}.gif", {
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
        ]
    )
