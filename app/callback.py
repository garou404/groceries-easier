from app import db, app
from dash import dcc, html, Input, Output, State, callback, ALL, MATCH, ctx
from app.model import Article, Recipe
from app.controller import add_article, get_recipes, get_articles_list
import pandas as pd


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
    recipes_dict = {}
    with app.app_context():
       recipes_dict = get_recipes()
    
    recipes_layout = []
    
    for recipe in recipes_dict:
        components_list = [html.Label([recipe['name']], className='h4 mr-3')]
        ingredient_list = []
        for article in recipe['ingredients']:
            ingredient_list.append(article['name']+', ')
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
    Input('app-url', 'href'),
    prevent_initial_call=True
)
def get_list_recipes(url):
    groceries_list = pd.read_csv('groceries-list.csv', sep=';')['recipe_id'].tolist()
    df = get_articles_list(groceries_list)
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