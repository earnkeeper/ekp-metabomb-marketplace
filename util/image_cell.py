from sdk.components import Col, Image, Row, Span


def image_cell(image, content, class_name=None):
    return Row(
        children=[
            Col(
                children=[
                    Image(
                        src=image
                    )
                ]
            ),
            Col(
                children=[
                    Span(
                        content=content
                    )
                ]
            )
        ]
    )
