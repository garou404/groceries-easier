from app import db, app
from app.model import Article, Recipe, recipe_article

def add_article(name, aisle, calorie=None, kg_for_calorie=None, price=None):
    new_article = Article(name=name, aisle=aisle, calorie=calorie, kg_for_calorie=kg_for_calorie, price=price)
    db.session.add(new_article)
    db.session.commit()

def get_recipes():
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
            recipe_dict = {'name' : recipe.Recipe.name, 'id': recipe.Recipe.id, 'ingredients': {}}
        recipe_dict['ingredients'].update({recipe.Article.name: recipe.quantity})
        if not recipe.Recipe.name in recipes_dict:
            recipes_dict[recipe.Recipe.name] = {}
        recipes_dict[recipe.Recipe.name].update({recipe.Article.name: recipe.quantity})
    return new_list_test

if __name__ == '__main__':
    app.run(debug=True)