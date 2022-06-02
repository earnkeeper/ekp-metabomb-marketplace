from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.image_cell import image_cell
from ekp_sdk.ui import (Card, Chart, Column, Container, Datatable, Span,
                        collection, commify, documents, format_currency,
                        format_template, is_busy)


def hero_tab(HEROES_COLLECTION_NAME):
    return Container(
        children=[
            Datatable(
                data=documents(HEROES_COLLECTION_NAME),
                busy_when=is_busy(collection(HEROES_COLLECTION_NAME)),
                filters=[
                    {"columnId": "rarity_name", "icon": "cil-spa"},
                    {"columnId": "level", "icon": "cil-shield-alt"},
                ],
                columns=[
                    Column(
                        id="id",
                        title="Token Id",
                        width="100px"
                    ),
                    Column(
                        id="name",
                        cell=__name_cell,
                        min_width='200px'
                    ),
                    Column(
                        id="price",
                        title="MTB Value",
                        format=commify("$.price"),
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="price_fiat",
                        title="Fiat Value",
                        format=format_currency(
                            "$.price_fiat", "$.fiat_symbol"),
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="mtb_per_day",
                        title="Est mtb per day",
                        format=commify("$.mtb_per_day"),
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="est_payback",
                        title="Est payback",
                        format=format_template("{{ est_payback }} days", {"est_payback": "$.est_payback"}),
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="est_roi",
                        title="Est ROI",
                        format=format_template("{{ est_roi }} %", {"est_roi": "$.est_roi"}),
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_power",
                        title="Power",
                        cell=set_image(icon_name='stats-power',
                                       attr_name='hero_power'),
                        width="80px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_health",
                        title="Health",
                        cell=set_image(icon_name='stats-health',
                                       attr_name='hero_health'),
                        width="80px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_speed",
                        title="Speed",
                        cell=set_image(icon_name='stats-speed',
                                       attr_name='hero_speed'),
                        width="80px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_stamina",
                        title="Stamina",
                        cell=set_image(icon_name='stats-stamina',
                                       attr_name='hero_stamina'),
                        width="90px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_bomb_num",
                        title="Bomb num",
                        cell=set_image(icon_name='stats-bombnum',
                                       attr_name='hero_bomb_num'),
                        width="80px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_bomb_range",
                        title="Bomb range",
                        cell=set_image(icon_name='stats-bombrange',
                                       attr_name='hero_bomb_range'),
                        width="80px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="spacer",
                        title="",
                        width="2px"
                    ),
                    Column(
                        id="rarity_name",
                        omit=True,
                        title="Rarity"
                    ),
                    Column(
                        id="level",
                        omit=True
                    ),

                ]
            )
        ]
    )


__name_cell = image_cell(
    format_template("https://app.metabomb.io/gifs/char-gif/{{ display_id }}.gif", {
        "display_id": '$.display_id'
    }),
    "$.name"
)


def set_image(icon_name, attr_name):
    return image_cell(
        f"https://app.metabomb.io/icons/stats-icon/{icon_name}.svg",
        f"$.{attr_name}",
        image_size="16px"
    )
