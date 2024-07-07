import dash
from dash import dcc, html, Input, Output, State, callback
from app import db, app
from app.model import Article, Recipe
from app.controller import add_article
from app.callback import *

dash_app = dash.Dash(__name__, server=app)

dash_app.layout = html.Div([
    # dcc.Link(id='app-url', href='home'),
    # 'Hello application',
    html.Div([
        html.Div([], id='trash-output'),
        html.Div(children=get_list_recipes(), id='groceries-list-container')
    ], className='col-md-6'),
    html.Div(
        [
            html.Div(
                children=get_recipes_layout(), 
                className='bg-warning-subtle p-4 m-4 overflow-y-scroll',
                style={'height': '600px'}
                )
        ],
        id='recipes-container',
        className='col-md-6 h-100'
        )
], className='fluid-container row h-100')

if __name__ == '__main__':
    dash_app.run(debug=True)