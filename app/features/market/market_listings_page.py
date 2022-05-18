from ekp_sdk.ui import (Badge, Button, Card, Col, Column, Container,
                            Datatable, Div, Form, Fragment, Hr, Icon, Image,
                            Paragraphs, Row, Select, Span, collection, commify,
                            documents, format_currency, format_template,
                            is_busy, switch_case)
from app.utils.game_constants import class_names, rarity_names
from app.utils.page_title import page_title


def listings_page(LISTINGS_COLLECTION_NAME):
    return Container(
        children=[
            Paragraphs(
                ["The Metabomb marketplace is launching soon!",
                 "We are ready to fill it with all the Play to Earn metrics you need. Watch this space 👀"],
            ),
            market_row(LISTINGS_COLLECTION_NAME),
        ]
    )


def market_row(LISTINGS_COLLECTION_NAME):
    return Datatable(
        data=documents(LISTINGS_COLLECTION_NAME),
        busy_when=is_busy(collection(LISTINGS_COLLECTION_NAME)),
        default_view="grid",
        default_sort_field_id="name",
        pagination_per_page=18,
        disable_list_view=True,
        grid_view={
            "tileWidth": [12, 6, 4, 3],
            "tile": grid_tile()
        },
        filters=[
            {"columnId": "rarity", "icon": "cil-spa"},
            {"columnId": "hero_class", "icon": "cil-shield-alt"},
            {"columnId": "level", "icon": "cil-chevron-double-up"},
        ],
        columns=[
            Column(
                id="name",
                sortable=True,
                searchable=True
            ),
            Column(
                id="hero_class",
                value=switch_case("$.hero_class", class_names()),
                title="Class"
            ),
            Column(
                id="rarity",
                value=switch_case("$.rarity", rarity_names()),
                omit=True
            ),
            Column(
                id="rarity_num",
                title="Rarity",
                format=switch_case("$.rarity", rarity_names()),
                sortable=True
            ),
            Column(
                id="level",
                sortable=True
            ),
        ]
    )


def grid_tile():
    return Card(
        class_name='m-0',
        children=[
            Row(
                class_name="mb-1 font-small-3",
                children=[
                    Col(
                        class_name='text-center col-12',
                        children=[
                            Image(
                                style={
                                    "height": "156px"
                                },
                                class_name="mt-4 mb-2",
                                src=format_template(
                                    "https://market.metabomb.io/gifs/char-gif/{{ image_id }}.gif",
                                    {
                                        "image_id": "$.display_id"
                                    }
                                )
                            ),
                        ]
                    ),
                    Col(
                        children=[
                            table(
                                [
                                    ["Name", "$.name"],
                                    ["Class", switch_case(
                                        "$.hero_class", class_names())],
                                    ["Rarity", switch_case(
                                        "$.rarity", rarity_names())],
                                    ["Level", "$.level"],
                                ],
                            )
                        ]
                    )

                ]
            )
        ]
    )


def table(rows):
    return Row(

        children=list(map(lambda row: table_row(row), rows))

    )


def table_row(row):
    return Fragment(
        children=[
            Col(
                class_name='col-12',
                children=[Hr()]
            ),
            Col(
                children=[
                    Span(
                        class_name="ml-1",
                        content=row[0]
                    )
                ]
            ),
            Col(
                children=[
                    Span(
                        class_name="float-right mr-1",
                        content=row[1]
                    )
                ]
            )
        ]
    )
