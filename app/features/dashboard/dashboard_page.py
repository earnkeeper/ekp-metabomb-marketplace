from app.utils.page_title import page_title
from ekp_sdk.ui import (Card, Col, Container, Chart, Image, Row, Span, Tab, Tabs,
                        format_currency, format_template, switch_case, documents)


def page(OPENS_COLLECTION_NAME):
    return Container(
        children=[
            page_title('box', 'Dashboard'),
            opens_chart_row(OPENS_COLLECTION_NAME)
        ]
    )


def opens_chart_row(OPENS_COLLECTION_NAME):
    return Chart(
        data=f"$.{OPENS_COLLECTION_NAME}[0]",
        type="sankey",
        title="Common Box Heroes",
    )
