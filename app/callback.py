from app import db, app
from dash import dcc, html, Input, Output, State, callback, ALL, MATCH, ctx, no_update
from app.model import Article, Recipe
from app.controller import add_article, get_recipes, get_articles_list
import pandas as pd

CURRENT_LIST = pd.read_csv('groceries-list.csv', sep=';')['recipe_id'].tolist()

GROCERIES_ORDER = [
    'Entretien maison',
    'Beauté',
    'Surgelés',
    'Produit du monde',
    'Epicerie sucrée',
    'Epicerie salée',
    'Epices',
    'Produit frais',
    'Viande',
    'Poisson',
    'Stand Charcuterie',
    'Cremerie lait oeuf',
    'Fruit et Légume',
    ]


def get_recipes_layout():
    # 
    # Get the recipes to suggest 
    # 
    recipes_dict = {}
    recipes_groceries_list = pd.read_csv('groceries-list.csv', sep=';')['recipe_id'].tolist()
    with app.app_context():
       recipes_dict = get_recipes(recipes_to_remove=recipes_groceries_list)
    
    recipes_layout = []
    
    for recipe in recipes_dict:
        components_list = [html.Label([recipe['name']], className='h4 mr-3')]
        ingredient_list = []
        for article in recipe['ingredients']:
            ingredient_list.append(article['name']+', ')
        components_list.append(html.Div(ingredient_list))
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
    Output('groceries-list-container', 'children'),
    Input('app-url', 'href'),
    prevent_initial_call=True
)
def get_html_groceries_list(url):
    recipes_groceries_list = pd.read_csv('groceries-list.csv', sep=';')['recipe_id'].tolist()
    if len(recipes_groceries_list) == 0:
        recipes_groceries_list = [-1]
    df = get_articles_list(recipes_groceries_list)
    html_layout = []
    for aisle in GROCERIES_ORDER:
        df_articles_per_aisle = df.loc[df['aisle'] == aisle]
        if df_articles_per_aisle.empty is False:
            articles_per_aisle = []
            for index, row in df_articles_per_aisle.iterrows():
                quantity_str = str(row['quantity'])
                if row['quantity_unit'] != 'unit':
                    quantity_str +=''+row['quantity_unit']
                articles_per_aisle.append(quantity_str+' '+row['article'])
            checklist_component = dcc.Checklist(options=articles_per_aisle)
            html_content_aisle = html.Div([
                html.Div([aisle], className='h5'), 
                checklist_component
            ])
            html_layout.append(html_content_aisle)
    return html_layout

@callback(
    Output('selected-recipe-container', 'children'),
    Input('app-url', 'href'),
    # prevent_initial_call=True
)
def get_html_selected_recipes(_):
    html_content = get_html_selected_recipes()

    return html_content

def get_html_selected_recipes():
    recipes_groceries_list = pd.read_csv('groceries-list.csv', sep=';')['recipe_id'].tolist()
    if len(recipes_groceries_list) == 0:
        recipes_groceries_list = [-1]
    selected_recipes = get_recipes(recipes_groceries_list)
    
    html_content = []
    for recipe in selected_recipes:
        html_content.append(
            html.Div([
                html.Label([recipe['name']], className='me-2 small'),
                html.Button('X', id={'type': 'btn-remove-recipe', 'index': recipe['id']}, className='btn btn-danger small', n_clicks=0)
            ], className='p-3 mx-2 bg-info-subtle')
        )
    return html_content


@callback(
    Output('selected-recipe-container', 'children', allow_duplicate=True),
    Output('groceries-list-container', 'children', allow_duplicate=True),
    Input({"type": "btn-add-recipe", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def add_recipe_ingredients_to_the_list(n_clicks):
    recipe_id = ctx.triggered_id['index']
    groceries_list = pd.read_csv('groceries-list.csv', sep=';')
    groceries_list = pd.concat([groceries_list, pd.DataFrame({'recipe_id': [recipe_id]})])
    groceries_list.to_csv('groceries-list.csv', sep=';', index=False)

    # evoluate make it take the current list and avoid read_csv again
    html_content = get_html_selected_recipes()
    recipes_groceries_list = groceries_list['recipe_id'].tolist()
    df = get_articles_list(recipes_groceries_list)
    html_layout = []
    for aisle in GROCERIES_ORDER:
        df_articles_per_aisle = df.loc[df['aisle'] == aisle]
        if df_articles_per_aisle.empty is False:
            articles_per_aisle = []
            for index, row in df_articles_per_aisle.iterrows():
                quantity_str = str(row['quantity'])
                if row['quantity_unit'] != 'unit':
                    quantity_str +=''+row['quantity_unit']
                articles_per_aisle.append(quantity_str+' '+row['article'])
            checklist_component = dcc.Checklist(options=articles_per_aisle)
            html_content_aisle = html.Div([
                html.Div([aisle], className='h5'), 
                checklist_component
            ])
            html_layout.append(html_content_aisle)
    return html_content, html_layout

@callback(
    Output("trash-output", "children"),
    Input({"type": "btn-remove-recipe", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def remove_recipe_ingredients_from_the_list(n_clicks):
    # print('n_clicks')
    # print(n_clicks)
    if n_clicks:
        print('test return no update')
        return no_update
    recipe_id_to_remove = ctx.triggered_id['index']
    df_recipes_groceries_list = pd.read_csv('groceries-list.csv', sep=';')
    df_recipes_groceries_list = df_recipes_groceries_list.loc[df_recipes_groceries_list['recipe_id'] != recipe_id_to_remove]
    # print('id to remove')
    # print(recipe_id_to_remove)
    # print('df')
    # print(df_recipes_groceries_list)
    # print('')
    df_recipes_groceries_list.to_csv('groceries-list.csv', sep=';', index=False)
    return None