from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span


def page(OPENS_COLLECTION_NAME):
    return Container(
        children=[
            page_title('box', 'Dashboard'),
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
        ]
    )


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
