from app import db, app
from app.model import Article, Recipe

def add_article(name, aisle, calorie=None, kg_for_calorie=None, price=None):
    new_article = Article(name=name, aisle=aisle, calorie=calorie, kg_for_calorie=kg_for_calorie, price=price)
    db.session.add(new_article)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)