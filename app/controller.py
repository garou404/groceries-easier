from app import db, app
from app.model import Article, Recipe, recipe_article
from sqlalchemy import select
import pandas as pd
import re

def add_article(name, aisle, calorie=None, kg_for_calorie=None, price=None):
    new_article = Article(name=name, aisle=aisle, calorie=calorie, kg_for_calorie=kg_for_calorie, price=price)
    db.session.add(new_article)
    db.session.commit()

def get_recipes(recipes_list=None):
    if recipes_list:
        # Query
        recipes = db.session.query(Recipe, recipe_article, Article).filter(
            Recipe.id == recipe_article.c.recipe_id
            ).filter(
                recipe_article.c.article_id == Article.id            
                ).filter(
                    Recipe.id.in_(recipes_list)
                ).all()
    else:
        # Query
        recipes = db.session.query(Recipe, recipe_article, Article).filter(
            Recipe.id == recipe_article.c.recipe_id
            ).filter(
                recipe_article.c.article_id == Article.id            
                ).all()
    
    recipes_dict = {}
    
    current_recipe = ''
    recipe_dict = {}
    new_list_test = []
    for recipe in recipes:
        if current_recipe != recipe.Recipe.name:
            if recipe_dict:
                new_list_test.append(recipe_dict)
            current_recipe = recipe.Recipe.name
            recipe_dict = {'name' : recipe.Recipe.name, 'id': recipe.Recipe.id, 'ingredients': []}
        recipe_dict['ingredients'].append({
            'name': recipe.Article.name, 
            'quantity': recipe.quantity, 
            'aisle': recipe.Article.aisle})
        if not recipe.Recipe.name in recipes_dict:
            recipes_dict[recipe.Recipe.name] = {}
        recipes_dict[recipe.Recipe.name].update({recipe.Article.name: recipe.quantity})
    return new_list_test

def decompose_string(input_string, num):
    # Define a regular expression pattern to match digits and letters
    pattern = r'(\d+)([A-Za-z]+)'
    
    # Use re.match to find the pattern in the input string
    match = re.match(pattern, input_string)
    
    if match:
        numeric_part = match.group(1)
        alphabetic_part = match.group(2)
        if num is True:
            return numeric_part
        else:
            return alphabetic_part
    else:
        if num is True:
            return input_string
        else:
            return 'unit'

def get_articles_list(recipe_ids):

    dict_recipes = get_recipes(recipe_ids)
    dict_articles = {
        'article': [],
        'quantity': [],
        'aisle': [],
    }
    for recipe in dict_recipes:
        for ingredient in recipe['ingredients']:
            dict_articles['article'].append(ingredient['name'])
            dict_articles['aisle'].append(ingredient['aisle'])
            dict_articles['quantity'].append(ingredient['quantity'])

    df = pd.DataFrame(dict_articles)
    df['quantity_unit'] = df['quantity'].apply(lambda x: decompose_string(x, False))
    df['quantity'] = df['quantity'].apply(lambda x: decompose_string(x, True))
    df['quantity'] = df['quantity'].astype(int)
    df = df.groupby(['article', 'aisle', 'quantity_unit'])['quantity'].sum().reset_index()
    df = df.sort_values(by=['aisle'])
    return df

    
if __name__ == '__main__':
    app.run(debug=True)