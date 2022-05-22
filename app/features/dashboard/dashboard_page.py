from app.utils.page_title import page_title
from ekp_sdk.ui import Chart, Col, Container, Row


def page(OPENS_COLLECTION_NAME):
    return Container(
        children=[
            page_title('box', 'Dashboard'),
            Row([
                Col("col-xs-12 col-md-6", [
                    opens_chart_row(
                        OPENS_COLLECTION_NAME,
                        0,
                        "Common Box Drop Percents"
                    ),
                ]),
                Col("col-xs-12 col-md-6", [
                    opens_chart_row(
                        OPENS_COLLECTION_NAME,
                        1,
                        "Premium Box Drop Percents"
                    ),
                ]),
                Col("col-xs-12 col-md-6", [
                    opens_chart_row(
                        OPENS_COLLECTION_NAME,
                        2,
                        "Ultra Box Drop Percents"
                    ),
                ])
            ])
        ]
    )


def opens_chart_row(OPENS_COLLECTION_NAME, doc_index, title):
    return Chart(
        data=f"$.{OPENS_COLLECTION_NAME}[{doc_index}]",
        type="sankey",
        title=title,
        class_name="mx-2 my-0",
        height=300
    )
