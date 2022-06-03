from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span, Div, Chart, commify, ekp_map, sort_by, json_array, \
    Hr
from app.features.dashboard.dashboard_fusion_page import fusion_table

def page(OPENS_COLLECTION_NAME, ACTIVITY_COLLECTION_NAME, FUSION_COLLECTION_NAME):
    return Container(
        children=[
            page_title('activity', 'Dashboard'),
            hero_drop_rates(OPENS_COLLECTION_NAME),
            Hr(),
            fusion_table(FUSION_COLLECTION_NAME),
            Hr(),
            new_user_activity(ACTIVITY_COLLECTION_NAME),
        ]
    )


def new_user_activity(ACTIVITY_COLLECTION_NAME):
    return Div([
        Span('New Users', 'font-medium-4 font-weight-bold'),
        Span('A great way to judge the health of a game economy is checking how many new users are entering the game every day.', "d-block mb-2 mt-1"),
        Span('Our chart below shows you the number of new unique wallet addresses interacting with Metabomb each day.', "d-block mb-2 mt-1"),
        Span('🤔 NOTE, Metabomb gameplay is not live yet, so new user counts are expected to be low',
             "d-block mb-2 mt-1"),
        new_user_chart(ACTIVITY_COLLECTION_NAME)
    ])


def new_user_chart(ACTIVITY_COLLECTION_NAME):
    return Card([
        Chart(
            card=False,
            height=250,
            type="line",
            data=f"$.{ACTIVITY_COLLECTION_NAME}.*",
            options={
                "chart": {
                    "zoom": {
                        "enabled": False,
                    },
                    "toolbar": {
                        "show": False,
                    },
                    "stacked": False,
                    "type": "line"
                },
                "xaxis": {
                    "type": "datetime",
                },
                "yaxis": [
                    {
                        "labels": {
                            "show": False,
                            "formatter": commify("$")
                        },
                    },
                ],
                "labels": ekp_map(
                    sort_by(
                        json_array(
                            f"$.{ACTIVITY_COLLECTION_NAME}.*"
                        ),
                        "$.timestamp_ms"
                    ), "$.timestamp_ms"
                ),
                "stroke": {
                    "width": 4,
                    "curve": 'smooth',
                }
            },
            series=[
                {
                    "name": "new users",
                    "type": "line",
                    "data": ekp_map(
                        sort_by(
                            json_array(f"$.{ACTIVITY_COLLECTION_NAME}.*"),
                            "$.timestamp_ms"),
                        "$.new_users"
                    )
                },
            ],

        )
    ])


def hero_drop_rates(OPENS_COLLECTION_NAME):
    return Div([
        Span('Actual Hero Drop Rates', 'font-medium-4 font-weight-bold'),
        Span('We are scanning the binance chain in REAL TIME, so that you know the ACTUAL hero drop rates. Check them out below 👀', "d-block mb-2 mt-1"),
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
