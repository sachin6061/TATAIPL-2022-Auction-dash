import dash_bootstrap_components as dbc
from dash import html


card =dbc.Card(
    [
        # dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            [
                html.H4("Card title", className="card-header"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
            ],
        ),
    ],
    style={"width": "18rem"},className='card text-white bg-success mb-3 m-1 p-1 w-100')