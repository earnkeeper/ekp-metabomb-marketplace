from app.features.market.market_history_page import history_page
from app.features.market.market_listings_page import listings_page
from app.utils.page_title import page_title
from ekp_sdk.ui import Container, Tab, Tabs


def page(LISTINGS_COLLECTION_NAME, HISTORY_COLLECTION_NAME):
    return Container(
        children=[
            page_title('shopping-cart', 'Marketplace'),
            tabs_row(LISTINGS_COLLECTION_NAME, HISTORY_COLLECTION_NAME),
        ]
    )


def tabs_row(LISTINGS_COLLECTION_NAME, HISTORY_COLLECTION_NAME):
    return Tabs(
        [
            Tab(
                label="History",
                children=[history_page(HISTORY_COLLECTION_NAME)]
            ),
            Tab(
                label="Listings (TESTNET)",
                children=[listings_page(LISTINGS_COLLECTION_NAME)]
            )
        ]
    )
