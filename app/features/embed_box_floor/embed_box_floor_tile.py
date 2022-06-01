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
                    Col("col-auto", [
                        Image(
                            src=switch_case("$.data[0]['common'].name", HERO_BOX_NAME_IMAGE),
                            style={"height": "20px"}
                        )
                    ]),
                    Col(
                        children=[
                            Span(class_name='d-block', content="$.data[0]['common'].name"),
                            Span(class_name='d-block', content=format_template(
                                "{{ boxes_num }} sales",
                                {
                                    "boxes_num": "$.data[0]['common'].countBoxes"
                                }
                            )),
                        ]
                    ),
                    Col(
                        class_name="col-auto pr-4",
                        children=[
                            Span(class_name='d-block', content=format_currency("$.data[0]['common'].floorPrice",
                                                                               "$.data[0]['common'].fiatSymbol")),
                            Span(class_name='d-block $.data[0]["common"].color', content=format_currency("$.data[0]['common'].percDiff",
                                                                               "%")),
                        ]
                    )
                ]
            ),
            Div(style={"marginBottom": "2px"}),
            Row(
                children=[
                    Col("col-auto", [
                        Image(
                            src=switch_case("$.data[0]['premium'].name", HERO_BOX_NAME_IMAGE),
                            style={"height": "20px"}
                        )
                    ]),
                    Col(
                        children=[
                            Span(class_name='d-block', content="$.data[0]['premium'].name"),
                            Span(class_name='d-block', content=format_template(
                                "{{ boxes_num }} sales",
                                {
                                    "boxes_num": "$.data[0]['premium'].countBoxes"
                                }
                            )),
                        ]
                    ),
                    Col(
                        class_name="col-auto pr-4",
                        children=[
                            Span(class_name='d-block', content=format_currency("$.data[0]['premium'].floorPrice",
                                                                               "$.data[0]['premium'].fiatSymbol")),
                            Span(class_name='d-block', content="$.data[0]['premium'].percDiff"),
                        ]
                    )
                ]
            ),
            Div(style={"marginBottom": "2px"}),
            Row(
                children=[
                    Col("col-auto", [
                        Image(
                            src=switch_case("$.data[0]['ultra'].name", HERO_BOX_NAME_IMAGE),
                            style={"height": "20px"}
                        )
                    ]),
                    Col(
                        children=[
                            Span(class_name='d-block', content="$.data[0]['ultra'].name"),
                            Span(class_name='d-block', content=format_template(
                                "{{ boxes_num }} sales",
                                {
                                    "boxes_num": "$.data[0]['ultra'].countBoxes"
                                }
                            )),
                        ]
                    ),
                    Col(
                        class_name="col-auto pr-4",
                        children=[
                            Span(class_name='d-block', content=format_currency("$.data[0]['ultra'].floorPrice",
                                                                               "$.data[0]['ultra'].fiatSymbol")),
                            Span(class_name='d-block', content="$.data[0]['ultra'].percDiff"),
                        ]
                    )
                ]
            )
        ]
    )
