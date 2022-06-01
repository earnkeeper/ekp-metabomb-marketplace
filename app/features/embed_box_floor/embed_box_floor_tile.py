from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span, Div, Chart, commify, ekp_map, sort_by, json_array


def tile():
    return Container(
        children=[
            Span("Metabomb"),
            Span("Box Floor Prices"),
        ]
    )
