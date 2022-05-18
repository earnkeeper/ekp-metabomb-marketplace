from app.utils.game_constants import HERO_BOX_NAME_CONTRACT
from ekp_sdk.ui import (Col, Column, Container, Datatable, Image, Link, Row,
                        Span, collection, commify, documents, format_age,
                        format_currency, format_mask_address, format_template,
                        is_busy, switch_case)


def history_page(HISTORY_COLLECTION_NAME):
    return Container([
        table_row(HISTORY_COLLECTION_NAME)
    ])


def table_row(HISTORY_COLLECTION_NAME):
    return Datatable(
        data=documents(HISTORY_COLLECTION_NAME),
        busy_when=is_busy(collection(HISTORY_COLLECTION_NAME)),
        default_sort_field_id="timestamp",
        default_sort_asc=False,
        filters=[
            {"columnId": "name", "icon": "cil-spa"},
            {"columnId": "type", "icon": "cil-3d"},
        ],
        columns=[
            Column(
                id="timestamp",
                sortable=True,
                cell=timestamp_cell(),
                width="120px"
            ),
            Column(
                id="name",
                title="Item",
                sortable=True,
                searchable=True,
                cell=name_cell(),
            ),
            Column(
                id="price",
                sortable=True,
                right=True,
                cell=price_cell()
            ),
            Column(
                id="type",
                omit=True,
                format=format_currency("$.priceFiat", "$.fiatSymbol")
            ),
        ]
    )


def timestamp_cell():
    return Row([
        Col(
            class_name="col-12",
            children=[
                Span(format_age("$.timestamp"))
            ]
        ),
        Col(
            class_name="col-12",
            children=[
                Link(
                    class_name="font-small-1",
                    href=format_template(
                        "https://bscscan.com/tx/{{ hash }}", {"hash": "$.hash"}),
                    external=True,
                    content=format_mask_address("$.hash")
                )
            ]
        )
    ])


def name_cell():
    return Row(
        children=[
            Col(
                class_name="my-auto col-auto pr-0",
                children=[
                    Image(
                        src="https://app.metabomb.io/gifs/herobox-gif/normal-box.gif",
                        style={"height": "38px"}
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
                                    Span("$.name")
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
                                                "contractAddress": switch_case("$.name", HERO_BOX_NAME_CONTRACT),
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


def price_cell():
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(format_currency("$.priceFiat", "$.fiatSymbol"))
            ]
        ),
        Col(
            class_name="col-12 text-right font-small-1",
            children=[
                Row([
                    Col([]),
                    Col(
                        class_name="col-auto p-0 my-auto",
                        children=[
                            Image(
                                src="https://app.metabomb.io/icons/mtb-token.png",
                                style={"height": "10px",
                                       "marginRight": "3px", "marginTop": "-2px"}
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
