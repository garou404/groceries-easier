from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' # utilisation de SQLite en local

# pour postgreSQL, définir l'URI appropriée ici
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    healthymeter = db.Column(db.Integer)
    how_many_person = db.Column(db.Integer)
    photo_path = db.Column(db.String(100))

    article = db.relationship('Article', secondary='recipe_article', back_populates='recipe')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40) , nullable=False)
    aisle = db.Column(db.String(40), nullable=False)
    calorie = db.Column(db.Integer)
    kg_for_calorie = db.Column(db.Integer)
    price = db.Column(db.Integer)

    recipe = db.relationship('Recipe', secondary='recipe_article' ,back_populates='article')


recipe_article = db.Table(
    'recipe_article',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
    db.Column('quantity', db.String)
)

with app.app_context():
    db.create_all()

    recipes = db.session.query(Recipe, recipe_article, Article).filter(
        Recipe.id == recipe_article.c.recipe_id
        ).filter(
            recipe_article.c.article_id == Article.id            
            ).all()
    
    dict_recipes = {}
    
    for recipe in recipes:
        if not recipe.Recipe.name in dict_recipes:
            dict_recipes[recipe.Recipe.name] = []
        dict_recipes[recipe.Recipe.name].append({recipe.Article.name: recipe.quantity})

print(dict_recipes)