from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Col, Column, Container, Datatable, Div,
                        Form, Image, Input, Row, Span, Tab, Tabs, collection,
                        documents, format_currency, format_template, is_busy,
                        navigate, remove_form_record, commify)


def players_page(PLAYERS_COLLECTION_NAME, PLAYERS_FORM_NAME):
    return Container(
        children=[
            page_title('users', 'Inventory'),
            Span(
                "Track Boxes, Heroes, Market Value and ROI for any player. Once you add an address, click on it in the list for full details",
                "my-1 d-block font-small-4"
            ),
            form_row(PLAYERS_FORM_NAME),
            table_row(PLAYERS_COLLECTION_NAME, PLAYERS_FORM_NAME)
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
                sortable=True
            ),
            Column(
                id="boxes",
                right=True,
                width="100px",
                sortable=True
            ),
            Column(
                id="heroes",
                right=True,
                width="100px",
                sortable=True
            ),
            Column(
                id="market_value_fiat",
                title="Value",
                right=True,
                width="100px",
                format=format_currency("$.market_value_fiat", "$.fiat_symbol"),
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