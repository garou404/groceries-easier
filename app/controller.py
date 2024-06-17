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
    
    for recipe in recipes:
        if not recipe.Recipe.name in recipes_dict:
            recipes_dict[recipe.Recipe.name] = {}
        recipes_dict[recipe.Recipe.name].update({recipe.Article.name: recipe.quantity})
    return recipes_dict

if __name__ == '__main__':
    app.run(debug=True)