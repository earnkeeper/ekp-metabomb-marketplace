from ekp_sdk.ui import (Card, Col, Container, Div, Image, Row, Span, Tab, Tabs,
                        format_currency, format_template, switch_case)
from app.features.heroes_market.history.heroes_history_tab import history_tab
from app.utils.page_title import page_title

def heroes_page(HISTORY_COLLECTION_NAME):
    return Container(
        children=[
            page_title('shopping-cart', 'Boxes Market'),
            # summary_row(SUMMARY_COLLECTION_NAME),
            Tabs(
                [
                    Tab(
                        label="History",
                        children=[history_tab(HISTORY_COLLECTION_NAME)]
                    ),
                ]
            ),
        ]
    )
