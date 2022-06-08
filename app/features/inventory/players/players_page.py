from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Col, Column, Container, Datatable, Div,
                        Form, Image, Input, Row, Span, collection, documents,
                        format_currency, format_template, is_busy, Link,
                        navigate, remove_form_record, commify, sum, format_mask_address, Icon, Alert)

from app.utils.summary_card import summary_card


def players_page(PLAYERS_COLLECTION_NAME, PLAYERS_FORM_NAME):
    return Container(
        children=[
            Alert(
                "Metabomb is currently under maintenance, preparing for their official launch today. This page may encounter errors.",
                header="Attention",
                icon_name="bell"
            ),
            Div([], "mb-4"),
            page_title('users', 'Inventory'),
            Span(
                "Track Boxes, Heroes, Market Value and ROI for any player. Once you add an address, click on it in the list for full details",
                "my-1 d-block font-small-4"
            ),
            summary_row(PLAYERS_COLLECTION_NAME),
            form_row(PLAYERS_FORM_NAME),
            table_row(PLAYERS_COLLECTION_NAME, PLAYERS_FORM_NAME),
            Row(
                children=[
                    Col(
                        class_name="col-auto",
                        children=[
                            Span("⚠️")
                        ]
                    ),
                    Col(
                        class_name="col-auto px-0",
                        children=[
                            Span(
                                "Est MTB earning calculations are based on the current state of testnet and subject to change."
                            ), ]
                    )
                ]
            ),
            Div([], "mt-1"),
            Row(

                children=[
                    Col(
                        class_name="col-auto",
                        children=[Icon(name="cib-discord")],
                    ),
                    Col(
                        class_name="col-auto px-0",
                        children=[
                            Link(
                                content="Join us on discord.",
                                external=True,
                                href="https://discord.com/invite/RHnnWBAkes"
                            )],
                    ),
                    Col(
                        class_name="col-auto",
                        children=[Span(
                            "We research earning potential for games daily"
                        )],
                    ),

                ]
            ),
            Div([], "mt-2"),
        ]
    )


def summary_row(PLAYERS_COLLECTION_NAME):
    return Div(
        when=f"$.{PLAYERS_COLLECTION_NAME}[0].id",
        children=[
            Row([
                Col(
                    "col-auto",
                    [
                        summary_card(
                            "Total Heroes",
                            sum(
                                f"$.{PLAYERS_COLLECTION_NAME}..heroes"
                            ),
                        ),
                    ]
                ),
                Col(
                    "col-auto",
                    [
                        summary_card(
                            "Total Boxes",
                            sum(
                                f"$.{PLAYERS_COLLECTION_NAME}..boxes"
                            ),
                        ),
                    ]
                ),
                Col("col-auto", [
                    summary_card(
                        "Market Value",
                        format_currency(
                            sum(
                                f"$.{PLAYERS_COLLECTION_NAME}..market_value_fiat"
                            ),
                            f"$.{PLAYERS_COLLECTION_NAME}[0].fiat_symbol"
                        ),
                    ),
                ]),

            ])
        ]
    )


def form_row(PLAYERS_FORM_NAME):
    return Form(
        name=PLAYERS_FORM_NAME,
        schema={
            "type": "object",
            "properties": {
                "address": "string"
            },
        },
        multi_record={
            "idField": "address"
        },
        children=[
            Row([
                Col(
                    "col-auto my-auto",
                    [
                        Input(
                            label="👇 Enter a BSC address to track",
                            name="address",
                            style={"minWidth": "300px"}
                        ),
                    ]
                ),
                Col(
                    "col-auto my-auto",
                    [
                        Button(label="Add", is_submit=True)
                    ]
                )
            ])

        ]
    )


def table_row(PLAYERS_COLLECTION_NAME, PLAYERS_FORM_NAME):
    return Datatable(
        default_sort_field_id="id",
        data=documents(PLAYERS_COLLECTION_NAME),
        busy_when=is_busy(collection(PLAYERS_COLLECTION_NAME)),
        on_row_clicked=navigate(
            format_template(
                "inventory/{{ address }}",
                {
                    "address": "$.id"
                }
            )
        ),
        columns=[
            Column(
                id="id",
                title="Address",
                searchable=True,
                sortable=True,
                format=format_mask_address("$.id")
            ),
            Column(
                id="boxes",
                right=True,
                width="120px",
                sortable=True
            ),
            Column(
                id="heroes",
                right=True,
                width="120px",
                sortable=True
            ),
            Column(
                id="market_value_fiat",
                title="Value",
                right=True,
                width="120px",
                format=format_currency("$.market_value_fiat", "$.fiat_symbol"),
                sortable=True
            ),
            Column(
                id="est_mtb_per_day",
                title="MTB / day",
                value=commify("$.est_mtb_per_day"),
                right=True,
                width="120px",
                # format="$.est_mtb_per_day",
                sortable=True
            ),
            Column(
                id="actions",
                width="60px",
                title="",
                cell=Button(
                    icon="cil-delete",
                    size='sm',
                    color='flat-primary',
                    on_click=remove_form_record(
                        PLAYERS_FORM_NAME, "address", "$.id"),
                    tooltip="Remove player"
                )
            )
        ]
    )
