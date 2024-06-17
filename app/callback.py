from app import db, app
from dash import dcc, html, Input, Output, State, callback
from app.model import Article, Recipe
from app.controller import add_article, get_recipes



@callback(
    Output('recipes-container', 'children'), 
    Input('app-url', 'href')
)
def get_recipes_layout(app_url):
    recipes_dict = get_recipes()
    
    recipes_layout = []
    
    for recipe_name in recipes_dict:
        components_list = [html.Label([recipe_name], className='h4 mr-3')]
        ingredient_list = []
        for article in recipes_dict[recipe_name]:
            ingredient_list.append(article+', ')
        components_list.append(html.Div(ingredient_list))
        recipe_layout = html.Div(components_list, className='mb-4 bg-info-subtle mx-4 p-2')
        recipes_layout.append(recipe_layout)

    return recipes_layout    