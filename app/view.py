import dash
from dash import dcc, html, Input, Output, State, callback
from app import db, app
from app.model import Article, Recipe
from app.controller import add_article
from app.callback import *

dash_app = dash.Dash(__name__, server=app)

dash_app.layout = html.Div([
    dcc.Link(id='app-url', href='home'),
    'Hello application',
    html.Div([

    ], id='recipes-container', )
], className='')


if __name__ == '__main__':
    dash_app.run(debug=True)