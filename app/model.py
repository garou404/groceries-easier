from app import db, app


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    healthymeter = db.Column(db.Integer)
    how_many_person = db.Column(db.Integer)
    photo_path = db.Column(db.String(100))

    article = db.relationship('Article', secondary='recipe_article', back_populates='recipe')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    aisle = db.Column(db.String(40))
    calorie = db.Column(db.Integer)
    kg_for_calorie = db.Column(db.Integer)
    price = db.Column(db.Integer)

    recipe = db.relationship('Recipe', secondary='recipe_article' ,back_populates='article')


recipe_article = db.Table(
    'recipe_article',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
    db.Column('kg', db.Integer),
    db.Column('quantity', db.Integer)
)

with app.app_context():
    db.create_all()