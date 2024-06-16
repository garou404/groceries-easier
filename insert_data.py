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
    db.Column('kg', db.Integer),
    db.Column('quantity', db.Integer)
)

with app.app_context():
    db.create_all()

    list_of_atricle_strings = ['Banane', 'Fruit et Légume',
    'Oeuf', 'Cremerie lait oeuf',
    'Pomme', 'Fruit et Légume',
    'Scamorza', 'Cremerie lait oeuf',
    'Parmesan', 'Cremerie lait oeuf',
    'Pancetta', 'Stand Charcuterie',
    'Poisson panure', 'Poisson',
    'Brocolis surgelé', 'Surgelés',
    'Mouchoir', 'Entretien maison',
    'Sopallin', 'Entretien maison',
    'Sac poubelle', 'Entretien maison',
    'Shampoing', 'Beauté',
    'Gel douche', 'Beauté',
    'Raclette', 'Cremerie lait oeuf',
    'Patate', 'Fruit et Légume',
    'Crème semi liquide', 'Cremerie lait oeuf',
    'Pâte feuilletée', 'Produit frais',
    'Pâte brisée', 'Produit frais',
    'Epinard surgelé', 'Surgelés',
    'Saumon surgelé', 'Surgelés',
    'Poulet', 'Viande',
    'Farine', 'Epicerie sucrée',
    'Corn flakes', 'Epicerie sucrée',
    'Haricots rouges', 'Epicerie salée',
    'Cumin', 'Epices',
    'Viande Hachée 5%', 'Viande',
    'Viande Hachée 15%', 'Viande',
    'Oignon rouge', 'Fruit et Légume',
    'Riz', 'Epicerie salée',
    'Concassé de tomate', 'Epicerie salée',
    'Spaguettis', 'Epicerie salée',
    'Couli de tomate', 'Epicerie salée',
    'Oignon', 'Fruit et Légume',
    'Penne', 'Epicerie salée',
    'Nouilles', 'Produit du monde',
    'Lait de coco', 'Produit du monde',
    'Carotte', 'Fruit et Légume',
    'Thon', 'Epicerie salée',
    'Mozzarella', 'Cremerie lait oeuf',
    'Crèpes Old El Paso', 'Produit du monde',
    'Avocat', 'Fruit et Légume',
    'Poivron rouge', 'Fruit et Légume',
    'Poivron vert', 'Fruit et Légume',
    'Poivron jaune', 'Fruit et Légume',
    'Tomate', 'Fruit et Légume',
    'Saumon fumé', 'Poisson',
    'Echalotte', 'Fruit et Légume',
    'Citron liquide', 'Epicerie salée',
    "Huile d'olive", 'Epicerie salée',
    'Patate douce', 'Fruit et Légume',
    'Bavette', 'Viande',
    'Pain de mie', 'Epicerie salée',
    'Toastinette', 'Cremerie lait oeuf',
    'Lait', 'Cremerie lait oeuf',
    'Fromage rapé', 'Cremerie lait oeuf',
    'Jambon', 'Produit frais',
    'Beurre', 'Cremerie lait oeuf',
    'Gnoccis', 'Produit frais',
    'Mozzarella Burrata', 'Cremerie lait oeuf',
    'Concentré de tomate', 'Epicerie salée',
    'Ricotta', 'Cremerie lait oeuf',
    'Pavé de saumon', 'Poisson',
    'Paprika', 'Epices',
    'Curry', 'Epices']

    list_of_article = []
    i = 0
    while i != len(list_of_atricle_strings):
        list_of_article.append(Article(name=list_of_atricle_strings[i], aisle=list_of_atricle_strings[i+1]))
        i += 2

    db.session.add_all(list_of_article)

    print(Article.query.filter_by(name='Pâte brisée').first())
    list_of_recipe_strings =  {
        'quiche': 
        [
            'Pâte brisée', 'Crème semi liquide', 'Oeuf'
        ],
        'raclette': 
        [
            'Raclette', 'Patate'
        ],
        'quiche saumon épinard': 
        [
            'Saumon surgelé', 'Epinard surgelé', 'Pâte brisée', 'Crème semi liquide', 'Oeuf'
        ],
        'galette de brocoli': 
        [
            
        ],
        'poulet tenders': 
        [
            'Poulet', 'Farine', 'Oeuf', 'Huile d\'olive', 'Paprika', 'Corn flakes'
        ],
        'chili con carne': 
        [
            'Viande Hachée 5%', 'Haricots rouges', 'Concassé de tomate', 'Oignon', 'Cumin', 'Riz'
        ],
        'bolognaise': 
        [
            'Viande Hachée 15%', 'Spaguettis', 'Couli de tomate', 'Oignon'
        ],
        'carbonara': 
        [
            'Penne', 'Pancetta', 'Parmesan', 'Oeuf'
        ],
        'nouilles poulet curry': 
        [
            'Nouilles', 'Poulet', 'Lait de coco', 'Carotte', 'Curry', 'Paprika'
            ],
        'riz thon': 
        [
            'Riz', 'Thon'
        ],
        'tacos mexicain': 
        [
            'Crèpes Old El Paso', 'Viande Hachée 15%', 'Poivron rouge', 'Poivron vert', 'Poivron jaune', 'Tomate', 'Oignon rouge'
        ],
        'tartare de saumon': 
        [
            'Saumon fumé', 'Pavé de saumon', 'Echalotte', 'Citron liquide', 'Huile d\'olive'
        ],
        'frite de patates douces bavette': 
        [
            'Patate douce', 'Bavette'
        ],
        'gnocci mozza burrata': 
        [
            'Gnoccis', 'Mozzarella Burrata', 'Ricotta', 'Oignon rouge', 'Concentré de tomate'
            ],
        'guacamole maison': 
        [
            'Avocat', 'Citron liquide', 'Oignon rouge', 'Tomate'],
        'riz brocolis + poisson': 
        [
            'Riz', 'Brocolis surgelé', 'Poisson panure'],
        'ricotta miel noix': 
        [
            'Ricotta'
        ],
        'croque-monsieur': 
        [
            'Pain de mie', 'Jambon', 'Toastinette', 'Beurre', 'Fromage rapé'
        ]
    }
    list_of_recipes = []
    for recipe in list_of_recipe_strings:
        print(recipe.capitalize())
        recipe_to_add = Recipe(name=recipe.capitalize())
        # Add recipe here
        db.session.add(recipe_to_add)
        # list_of_recipes.append(recipe_to_add)
        for ingredient in list_of_recipe_strings[recipe]:
            print('     '+ingredient)
            article_to_add = Article.query.filter_by(name=ingredient).first()
            if not article_to_add:
                print(article_to_add)
                print(f'{ingredient} is none')
            recipe_to_add.article.append(article_to_add)

    db.session.commit()