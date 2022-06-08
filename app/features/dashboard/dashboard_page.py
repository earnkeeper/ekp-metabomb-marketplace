from app.features.dashboard.dashboard_hero_profit_page import hero_dashboard_profit_calc_page
from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span, Div, Chart, commify, ekp_map, sort_by, json_array, \
    Hr, Alert
from app.features.dashboard.dashboard_fusion_page import fusion_table

def page(OPENS_COLLECTION_NAME, FUSION_COLLECTION_NAME, HERO_DASH_PROFIT_COLLECTION_NAME):
    return Container(
        children=[
            Div([], "mb-4"),
            page_title('activity', 'Dashboard'),
            Div(class_name="my-4"),
            hero_dashboard_profit_calc_page(HERO_DASH_PROFIT_COLLECTION_NAME),
            Div(class_name="my-4"),
            fusion_table(FUSION_COLLECTION_NAME),
            Div(class_name="my-4"),
            hero_drop_rates(OPENS_COLLECTION_NAME),
        ]
    )

def hero_drop_rates(OPENS_COLLECTION_NAME):
    return Div([
        Span('Actual Hero Drop Rates', 'font-medium-4 font-weight-bold'),
        Hr("mb-2"),        
        Span('We scan the binance smart chain in real time, to give you the real hero drop rates as boxes are opened.', "d-block mb-2 mt-1"),
        Row([
            Col("col-12 col-md-6", [
                opens_chart_row(
                    OPENS_COLLECTION_NAME,
                    0,
                    "Common Box"
                ),
            ]),
            Col("col-12 col-md-6", [
                opens_chart_row(
                    OPENS_COLLECTION_NAME,
                    1,
                    "Premium Box"
                ),
            ]),
            Col("col-12 col-md-6", [
                opens_chart_row(
                    OPENS_COLLECTION_NAME,
                    2,
                    "Ultra Box"
                ),
            ])
        ])
    ])


def opens_chart_row(OPENS_COLLECTION_NAME, doc_index, box_type):
    return Card(
        [
            Row(
                class_name="mx-1 my-2",
                children=[
                    Col(
                        "col-auto my-auto pr-0", [
                            Image(
                                src=HERO_BOX_NAME_IMAGE[box_type],
                                style={"height": "32px"}
                            )
                        ]
                    ),
                    Col(
                        "col-auto my-auto", [
                            Span(box_type, "font-medium-3 font-weight-bold")
                        ]
                    ),

                ]
            ),
            Chart(
                data=f"$.{OPENS_COLLECTION_NAME}[{doc_index}]",
                type="sankey",
                card=False,
                class_name="mx-2 my-0",
                height=300
            )

        ]
    )
