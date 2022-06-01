from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span, Div, Chart, commify, ekp_map, sort_by, json_array, \
    switch_case, format_template, format_currency


def tile():
    return Container(
        children=[
            Span("Metabomb"),
            Div([]),
            Span("Hero Box Floor Prices"),
            Div(style={"marginBottom": "10px"}),
            Row(
                children=[
                    image_cell('common'),
                    boxes_name_count('common'),
                    boxes_price_stats('common')
                ]
            ),
            Div(style={"marginBottom": "2px"}),
            Row(
                children=[
                    image_cell('premium'),
                    boxes_name_count('premium'),
                    boxes_price_stats('premium')
                ]
            ),
            Div(style={"marginBottom": "2px"}),
            Row(
                children=[
                    image_cell('ultra'),
                    boxes_name_count('ultra'),
                    boxes_price_stats('ultra')
                ]
            )
        ]
    )


def image_cell(box_type):
    return Col("col-auto", [
        Image(
            src=switch_case(f"$.data[0]['{box_type}'].name", HERO_BOX_NAME_IMAGE),
            style={"height": "20px"}
        )
    ])


def boxes_name_count(box_type):
    return Col(
        children=[
            Span(class_name='d-block', content=f"$.data[0]['{box_type}'].name"),
            Span(class_name='d-block', content=format_template(
                "{{ boxes_num }} sales",
                {
                    "boxes_num": f"$.data[0]['{box_type}'].countBoxes"
                }
            )),
        ]
    )


def boxes_price_stats(box_type):
    return Col(
        class_name="col-auto pr-4",
        children=[
            Span(class_name='d-block', content=format_currency(f"$.data[0]['{box_type}'].floorPrice",
                                                               f"$.data[0]['{box_type}'].fiatSymbol")),
            Span(class_name=f'd-block $.data[0]["{box_type}"].color',
                 content=format_currency(f"$.data[0]['{box_type}'].percDiff",
                                         "%")),
        ]
    )
