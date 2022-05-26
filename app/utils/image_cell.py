from ekp_sdk.ui import Col, Image, Row, Span


def image_cell(image, content, class_name=None):
    return Row(
        children=[
            Col(
                class_name="col-auto pr-0",
                children=[
                    Image(
                        src=image,
                        style={"height": "24px"}
                    )
                ]
            ),
            Col(
                class_name="col-auto",
                children=[
                    Span(
                        content=content
                    )
                ]
            )
        ]
    )
