from app.features.inventory.player.box_tab import box_tab
from app.features.inventory.player.hero_tab import hero_tab
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span, Tabs, Tab


def page(HEROES_COLLECTION_NAME, BOXES_COLLECTION_NAME):
    return Container(
        children=[
            page_title('box', 'Inventory'),
             Tabs(
                [
                    Tab(
                        label="Heroes",
                        children=[hero_tab(HEROES_COLLECTION_NAME)]
                    ),
                    Tab(
                        label="Boxes",
                        children=[box_tab(BOXES_COLLECTION_NAME)]
                    ),
                ]
            ),           
        ]
    )

