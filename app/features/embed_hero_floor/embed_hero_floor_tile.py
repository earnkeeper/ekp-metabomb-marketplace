from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span, Div, Chart, commify, ekp_map, sort_by, json_array, \
    switch_case, format_template, format_currency


def tile():
    return Container(
        children=[
            Span("Hero Floor Prices", "font-medium-2"),
            Div(class_name="mb-1"),
            Row(
                children=[
                    image_cell('common'),
                    heroes_name_count('common'),
                    heroes_price_stats('common')
                ]
            ),
            Div(class_name="mb-1"),
            Row(
                children=[
                    image_cell('rare'),
                    heroes_name_count('rare'),
                    heroes_price_stats('rare')
                ]
            ),
            Div(class_name="mb-1"),
            Row(
                children=[
                    image_cell('epic'),
                    heroes_name_count('epic'),
                    heroes_price_stats('epic')
                ]
            ),
        ]
    )


def image_cell(hero_type):
    return Col("col-auto pr-0 my-auto", [
        Image(
            src=format_template("https://app.metabomb.io/gifs/char-gif/{{ display_id }}.gif", {
                "display_id": f"$.data[0]['{hero_type}'].display_id"
            }),
            style={"height": "32px"}
        )
    ])


def heroes_name_count(hero_type):
    return Col(
        children=[
            Span(
                class_name='d-block font-small-3',
                content=f"$.data[0]['{hero_type}'].name"
            ),
            Span(
                class_name='d-block font-small-1',
                content=format_template(
                    "{{ heroes_num }} sales",
                    {
                        "heroes_num": f"$.data[0]['{hero_type}'].countBoxes"
                    }
                )
            ),
        ]
    )


def heroes_price_stats(hero_type):
    return Col(
        class_name="col-auto",
        children=[
            Span(
                class_name=format_template(
                    'd-block text-right font-small-3 text-{{ color }}',
                    {
                        "color": f'$.data[0]["{hero_type}"].color'
                    }
                ),
                content=format_currency(
                    f"$.data[0]['{hero_type}'].floorPrice",
                    f"$.data[0]['{hero_type}'].fiatSymbol"
                )
            ),
            Span(
                class_name=format_template(
                    'd-block text-right font-small-1 text-{{ color }}',
                    {
                        "color": f'$.data[0]["{hero_type}"].color'
                    }
                ),
                content=format_currency(
                    f"$.data[0]['{hero_type}'].percDiff",
                    "%"
                )
            ),
        ]
    )
