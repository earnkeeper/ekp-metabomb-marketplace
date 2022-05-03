from sdk.components import (Badge, Button, Card, Col, Column, Container, Datatable,
                            Div, Form, Fragment, Hr, Icon, Image, Row, Select, Span, collection,
                            commify, documents, format_currency,
                            format_template, is_busy, switch_case)


def page(listings_collection_name):
    return Container(
        children=[
            title_row(),
            market_row(listings_collection_name),
        ]
    )


def title_row():
    return Row(
        children=[
            Col(
                children=[Icon("shopping-cart")],
                class_name='col-auto pr-0'
            ),
            Col(
                children=[
                    Span("Marketplace", "font-medium-3")
                ]
            )
        ],
        class_name="mb-2"
    )


def market_row(listings_collection_name):
    return Datatable(
        class_name="mt-2",
        data=documents(listings_collection_name),
        busy_when=is_busy(collection(listings_collection_name)),
        show_export=False,
        default_view="grid",
        pagination_per_page=18,
        disable_list_view=True,
        grid_view={
            "tile": grid_tile()
        },
        columns=[
            Column(
                id="id",
            ),
        ]
    )


def grid_tile():
    return Card(
        children=[
            Row(
                class_name="mb-1",
                children=[
                    Col(
                        class_name='text-center col-12',
                        children=[
                            Image(
                                style={
                                    "height": "156px"
                                },
                                class_name="mt-3 mb-2",
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
                                    ["Rarity", "$.rarity"],
                                    ["Level", "$.level"],
                                    ["Class", "$.hero_class"],
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
