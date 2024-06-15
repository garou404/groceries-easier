import dash
from dash import dcc, html, Input, Output, State, callback
from app import db, app
from app.model import Article, Recipe
from app.controller import add_article

dash_app = dash.Dash(__name__, server=app)

dash_app.layout = html.Div([
    'Hello application'
])


if __name__ == '__main__':
    dash_app.run(debug=True)