from app import db, app
from dash import dcc, html, Input, Output, State, callback, ALL, MATCH, ctx
from app.model import Article, Recipe
from app.controller import add_article, get_recipes, get_list_articles
import pandas as pd


# @callback(
#     Output('recipes-container', 'children'), 
#     Input('app-url', 'href')
# )
# def get_recipes_layout(app_url):
#     recipes_dict = get_recipes()
    
#     recipes_layout = []
    
#     for recipe_name in recipes_dict:
#         components_list = [html.Label([recipe_name], className='h4 mr-3')]
#         ingredient_list = []
#         for article in recipes_dict[recipe_name]:
#             ingredient_list.append(article+', ')
#         components_list.append(html.Div(ingredient_list))
#         recipe_layout = html.Div(components_list, className='mb-4 bg-info-subtle mx-4 p-2')
#         recipes_layout.append(recipe_layout)

def get_recipes_layout():
    recipes_dict = {}
    with app.app_context():
       recipes_dict = get_recipes()
    
    recipes_layout = []
    
    for recipe in recipes_dict:
        components_list = [html.Label([recipe['name']], className='h4 mr-3')]
        ingredient_list = []
        for article in recipe['ingredients']:
            ingredient_list.append(article+', ')
        components_list.append(html.Div(ingredient_list))
        # print(components_list)
        recipe_layout = html.Div([
            html.Div(
                children=components_list
            ),
            html.Div([
                html.Button('Add', id={'type': 'btn-add-recipe', 'index': str(recipe['id'])}, n_clicks=0, className='btn')
            ])
        ], className='m-4 p-2 rounded shadow-sm bg-light-subtle d-flex align-items-center justify-content-between')
        recipes_layout.append(recipe_layout)
    return recipes_layout    



@callback(
    Output("trash-output", "children"),
    Input({"type": "btn-add-recipe", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
    # State({"type": "btn-add-recipe", "index": ALL}, "id")
)
def display_output(n_clicks):
    recipe_id = ctx.triggered_id['index']
    groceries_list = pd.read_csv('groceries-list.csv', sep=';')
    print(groceries_list)
    groceries_list = pd.concat([groceries_list, pd.DataFrame({'recipe_id': [recipe_id]})])
    print(groceries_list)
    groceries_list.to_csv('groceries-list.csv', sep=';', index=False)
    return str(recipe_id)+' added'

@callback(
    Output('groceries-list-container', 'children'),
    Input('app-url', 'href')
)
def get_list_recipes(url):
    groceries_list = pd.read_csv('groceries-list.csv', sep=';')['recipe_id'].tolist()
    print(groceries_list)
    get_list_articles(groceries_list)
    # list_layout = []
    # for id in groceries_list['recipe_id']:
    #     list_layout.append(html.Div([id]))
    # print(list_layout)
    # return list_layout
    return 'coucou'