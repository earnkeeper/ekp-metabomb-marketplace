from ekp_sdk.ui import Form, Row, Col, Select, Button, Chart, documents, commify, ekp_map, json_array, sort_by


def form_row(RARITIES_FORM_NAME):
    return Form(
        name=RARITIES_FORM_NAME,
        schema={
            "type": "object",
            "properties": {
                "rarity": "string"
            },
        },
        children=[
            Row([
                Col(
                    "col-auto my-auto",
                    [
                        Select(
                            label="Select rarity",
                            name="rarity",
                            options=["Common", "Epic", "Rare", "Legend"],
                            min_width="120px"
                        ),
                    ],

                ),
                Col(
                    "col-auto my-auto",
                    [
                        Button(label="Update", is_submit=True)
                    ]
                )
            ])

        ]
    )


def chart_row(CHART_COLLECTION_NAME):
    return Chart(
        title="",
        height=200,
        type="line",
        data=documents(CHART_COLLECTION_NAME),
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
                {
                    "labels": {
                        "show": False,
                        "formatter": commify("$")
                    },
                    "opposite": True,
                },
            ],
            "labels": ekp_map(
                sort_by(
                    json_array(
                        documents(CHART_COLLECTION_NAME)
                    ),
                    "$.timestamp_ms"
                ), "$.timestamp_ms"
            ),
            "stroke": {
                "width": [4, 4],
                "curve": 'smooth',
            }
        },
        series=[
            {
                "name": "Sales Count",
                "type": "column",
                "data": ekp_map(
                    sort_by(
                        json_array(documents(CHART_COLLECTION_NAME)),
                        "$.timestamp_ms"),
                    "$.number_of_sales"
                )
            },
            {
                "name": "Sales Value",
                "type": "line",
                "data": ekp_map(
                    sort_by(
                        json_array(documents(CHART_COLLECTION_NAME)),
                        "$.timestamp_ms"
                    ),
                    "$.price_fiat_avg"
                ),
            },
        ],

    )
