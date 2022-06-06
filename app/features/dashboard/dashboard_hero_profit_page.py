from ekp_sdk.ui import Div, Span, Row, Col, Datatable, Card, Column, format_currency, format_template, Icon, \
    Container, Paragraphs, switch_case, Link, Hr


def hero_dashboard_profit_calc_page(HERO_DASH_PROFIT_COLLECTION_NAME):
    return Container(
        children=[
            title_row(),
            Paragraphs(
                [
                    "Use the table below as reference for how long a hero will take to pay back its initial purchase cost",
                    "These figures are based on 24hr play in the Chest Farm mode"
                ],
            ),
            Row([
                Col("col-12 col-md-6", [
                    table_row(
                        HERO_DASH_PROFIT_COLLECTION_NAME,
                        0,
                        "Common"
                    ),
                ]),
                Col("col-12 col-md-6", [
                    table_row(
                        HERO_DASH_PROFIT_COLLECTION_NAME,
                        1,
                        "Rare"
                    ),
                ]),
                Col("col-12 col-md-6", [
                    table_row(
                        HERO_DASH_PROFIT_COLLECTION_NAME,
                        2,
                        "Epic"
                    ),
                ]),
                Col("col-12 col-md-6", [
                    table_row(
                        HERO_DASH_PROFIT_COLLECTION_NAME,
                        3,
                        "Legend"
                    ),
                ]),
            ]),
            Paragraphs(
                [
                    "⚠️Est MTB earning calculations are based on the current state of testnet and subject to change.",
                ],
            ),
            Row(

                children=[
                    Col(
                        class_name="col-auto",
                        children=[Icon(name="cib-discord")],
                    ),
                    Col(
                        class_name="col-auto px-0",
                        children=[
                            Link(
                                content="Join us on discord.",
                                external=True,
                                href="https://discord.com/invite/RHnnWBAkes"
                            )],
                    ),
                    Col(
                        class_name="col-auto",
                        children=[Span(
                            "We research earning potential for games daily"
                        )],
                    ),

                ]
            ),
            Hr()
        ]
    )


def title_row():
    return Row(
        children=[
            Col(
                children=[Icon("box")],
                class_name='col-auto pr-0'
            ),
            Col(
                children=[
                    Span("Hero Profit Calculator", "font-medium-3")
                ]
            )
        ],
        class_name="mb-2"
    )


def table_row(HERO_DASH_PROFIT_COLLECTION_NAME, doc_index, hero_type):
    return Div(
        [
            Row(
                class_name="mx-1 my-2",
                children=[

                    Col(
                        class_name="col-auto px-0",
                        children=[
                            Div(
                                [],
                                style={
                                    "backgroundColor": switch_case(hero_type, {
                                        'Common': "#D1CCCC",
                                        'Rare': '#65F44E',
                                        'Epic': '#C13EFA',
                                        'Legend': '#EB9A29',
                                    }),
                                    "width": 6,
                                    "height": '100%',
                                    "marginRight": '0.6rem',
                                }
                            ),
                        ],
                    ),
                    Col(
                        "col-auto my-auto", [
                            Span(format_template("{{ hero_type }} Hero",
                                                 {"hero_type": hero_type}), "font-medium-3 font-weight-bold")
                        ]
                    ),

                ]
            ),
            Datatable(
                class_name="mt-1",
                data=f"$.{HERO_DASH_PROFIT_COLLECTION_NAME}[{doc_index}].*",
                # busy_when=is_busy(collection(FUSION_COLLECTION_NAME)),
                show_export=False,
                columns=[
                    Column(
                        id="power",
                        value="$.power",
                        width="100px",
                    ),
                    Column(
                        id="market_value",
                        value=format_currency("$.market_value", "$.fiat_symbol"),
                        min_width="120px"
                    ),
                    Column(
                        id="mtb_per_day",
                        value="$.mtb_per_day",
                        min_width="120px"
                    ),
                    Column(
                        id="roi",
                        value=format_template(
                            "{{ roi }} days",
                            {"roi": "$.roi"}
                        ),
                        min_width="120px"
                    ),
                    Column(
                        id="spacer",
                        title="",
                        width="10px"
                    )
                ]
            )

        ]
    )
