from sdk.components import (Badge, Button, Col, Column, Container, Datatable,
                            Div, Form, Icon, Row, Select, Span, collection,
                            commify, documents, format_currency,
                            format_template, is_busy, switch_case)


def page():
    return Container(
        children=[
            title_row(),
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

