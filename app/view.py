import dash
from dash import dcc, html, Input, Output, State, callback
from app import db, app
from app.model import Article, Recipe
from app.controller import add_article
from app.callback import *

dash_app = dash.Dash(__name__, server=app)


dash_app.layout = html.Div([
    dcc.Location(id='app-url'),
    # 'Hello application',
    html.Div([
        html.Div([], id='trash-output'),
        html.Div([
            html.Div(id='groceries-list-container', className='bg-success-subtle p-2')
        ], className='p-5 '),
        html.Div(className='row',
                 children=[
                    html.Div(className='d-flex align-content-start flex-wrap', id='selected-recipe-container', children=[

                    ])
                 ])
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
], className='fluid-container d-flex h-100')

if __name__ == '__main__':
    dash_app.run(debug=True)