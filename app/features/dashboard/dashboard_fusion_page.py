from ekp_sdk.ui import (Badge, Button, Col, Column, Container, Datatable, Div, Form,
                        Icon, Row, Select, Span, collection, commify, documents,
                        format_currency, format_template, is_busy, switch_case)


def fusion_table(FUSION_COLLECTION_NAME):
    return Container(
        children=[
            title_row(),
            table_row(FUSION_COLLECTION_NAME)
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
                    Span("Fusion Cost Calculator", "font-medium-3")
                ]
            )
        ],
        class_name="mb-2"
    )


def table_row(FUSION_COLLECTION_NAME):
    return Datatable(
        class_name="mt-1",
        data=documents(FUSION_COLLECTION_NAME),
        busy_when=is_busy(collection(FUSION_COLLECTION_NAME)),
        show_export=False,
        columns=[
            Column(
                id="target_name",
                width="130px",
                cell=target_cell(),
            ),
            Column(
                id="inputs",
                cell=materials_cell(),
                min_width="160px"
            ),
            Column(
                id="input_costs",
                title="Input costs",
                cell=input_costs(),
                right=True,
                width="160px"
            ),
            Column(
                id="fusion_fees",
                title="Fusion Fees",
                cell=fusion_fees(),
                right=True,
                width="160px"
            ),
            Column(
                id="total_costs",
                title="Total cost",
                cell=total_costs(),
                right=True,
                width="160px"
            ),
            Column(
                id="market_value",
                title="Market Value",
                cell=market_value(),
                right=True,
                width="160px"
            ),
            # Column(
            #     id="premium",
            #     value='$.calcs.premium.total_cost',
            #     title="Premium Box",
            #     cell=cost_cell("premium"),
            #     right=True,
            #     width="160px"
            # ),
            # Column(
            #     id="ultra",
            #     value='$.calcs.ultra.total_cost',
            #     title="Ultra Box",
            #     cell=cost_cell("ultra"),
            #     right=True,
            #     width="160px"
            # ),
            Column(
                id="spacer",
                title="",
                width="10px"
            )
        ]
    )


def target_cell():
    return Row(
        children=[
            Col(
                class_name="col-auto px-0",
                children=[
                    Div(
                        [],
                        style={
                            "backgroundColor": switch_case('$.target_name', {
                                'Rare': '#D1CCCC',
                                'Epic': '#65F44E',
                                'Legend': '#C13EFA',
                                'Mythic': '#EB9A29',
                                'Meta': '#E8483A',
                            }),
                            "width": 6,
                            "height": '100%',
                            "marginRight": '0.6rem',
                        }
                    )
                ],
            ),
            Col(
                class_name="col-auto px-0",
                children=[
                    Span("$.target_name", "font-small-5 font-weight-bold")
                ],
            ),
        ],
        class_name="mx-0")


def materials_cell():
    return Row(
        children=[
            Col(
                class_name="col-12 font-small-5 font-weight-bold",
                children=[
                    Span(
                        format_template(
                            "2 x {{ input_hero_rarity }} @ Lv {{ inputs_required_level }}",
                            {
                                "input_hero_rarity": "$.input_hero_rarity",
                                "inputs_required_level": "$.inputs_required_level"
                            }
                        ))],
            ),
            Col(
                class_name="col-12 font-small-1",
                children=[
                    Span(
                        format_template(
                            "{{ inputs_count }} x {{ input_hero_rarity }} @ Lv 1",
                            {
                                "input_hero_rarity": "$.input_hero_rarity",
                                "inputs_count": "$.inputs_count"
                            }
                        )
                    )
                ],

            ),
        ])


# format_currency("$.total_price", "$.fiatSymbol")
def input_costs():
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(format_currency("$.inputs_cost_fiat", "$.fiat_symbol"))
            ],
        ),
        Col(
            class_name="col-12 text-right",
            children=[
                Span(
                    format_template(
                        "{{ inputs_count }} x {{ input_floor_price_fiat }}",
                        {
                            "inputs_count": "$.inputs_count",
                            "input_floor_price_fiat": format_currency(f"$.input_floor_price_fiat", "$.fiat_symbol")
                        }
                    ),
                    "float-right font-small-2"
                )
            ],
        )
    ])


def fusion_fees():
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(format_currency("$.fusion_fees_fiat", "$.fiat_symbol"))
            ],
        ),
        Col(
            class_name="col-12 text-right",
            children=[
                Span(
                    format_template(
                        "{{ fusion_fees_mtb }} MTB",
                        {
                            "fusion_fees_mtb": "$.fusion_fees_mtb",
                        }
                    ),
                    "float-right font-small-2"
                )
            ],
        )
    ])


def total_costs():
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(format_currency("$.total_cost_fiat", "$.fiat_symbol"))
            ],
        ),
        Col(
            class_name="col-12 text-right",
            children=[
                Span(
                    format_template(
                        "{{ total_cost_mtb }} MTB",
                        {
                            "total_cost_mtb": "$.total_cost_mtb",
                        }
                    ),
                    "float-right font-small-2"
                )
            ],
        )
    ])


def market_value():
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(format_currency("$.market_value_fiat", "$.fiat_symbol"))
            ],
        ),
        # Col(
        #     class_name="col-12 text-right",
        #     children=[
        #         Span(
        #             format_template(
        #                 "{{ market_value_mtb }} MTB",
        #                 {
        #                     "market_value_mtb": "$.market_value_mtb",
        #                 }
        #             ),
        #             "float-right font-small-2"
        #         )
        #     ],
        # )
    ])
