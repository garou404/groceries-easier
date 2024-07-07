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

    list_of_atricle_strings = [
    'Banane', 'Fruit et Légume',
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
            'Pâte brisée', '1', 
            'Crème semi liquide', '25cl', 
            'Oeuf', '2'
        ],
        'raclette': 
        [
            'Raclette', '200g', 
            'Patate', '500g'
        ],
        'quiche saumon épinard': 
        [
            'Saumon surgelé', '1', 
            'Epinard surgelé', '1', 
            'Pâte brisée', '1', 
            'Crème semi liquide', '25cl',
            'Oeuf', '1'
        ],
        'galette de brocoli': 
        [
            
        ],
        'poulet tenders': 
        [
            'Poulet', '150g',
            'Farine', '1',
            'Oeuf', '2',
            'Huile d\'olive', '1', 
            'Paprika', '1',
            'Corn flakes', '1'
        ],
        'chili con carne': 
        [
            'Viande Hachée 5%', '75g',
            'Haricots rouges', '70g',
            'Concassé de tomate', '100g',
            'Oignon rouge', '1',
            'Cumin', '1',
            'Riz', '100g'
        ],
        'bolognaise': 
        [
            'Viande Hachée 15%', '100g',
            'Spaguettis', '140g',
            'Couli de tomate', '1',
            'Oignon', '1'
        ],
        'carbonara': 
        [
            'Penne', '100g', 
            'Pancetta', '50g',
            'Parmesan', '40g',
            'Oeuf', '2'
        ],
        'nouilles poulet curry': 
        [
            'Nouilles', '100g',
            'Poulet', '100g',
            'Lait de coco', '1', 
            'Carotte',  '300g',
            'Curry',  '1',
            'Paprika', '1'
            ],
        'riz thon': 
        [
            'Riz', '130g',
            'Thon', '110g'
        ],
        'tacos mexicain': 
        [
            'Crèpes Old El Paso', '1', 
            'Viande Hachée 15%', '100g',
            'Poivron rouge', '1',
            'Poivron vert', '1',
            'Poivron jaune', '1',
            'Tomate', '1',
            'Oignon rouge', '1'
        ],
        'tartare de saumon': 
        [
            'Saumon fumé', '1',
            'Pavé de saumon', '1',
            'Echalotte', '3',
            'Citron liquide', '1',
            'Huile d\'olive', '1'
        ],
        'frite de patates douces bavette': 
        [
            'Patate douce', '400g',
            'Bavette', '1'
        ],
        'gnocci mozza burrata': 
        [
            'Gnoccis', '1',
            'Mozzarella Burrata', '1',
            'Ricotta', '1',
            'Oignon rouge', '1',
            'Concentré de tomate', '1'
        ],
        'guacamole maison': 
        [
            'Avocat', '2',
            'Citron liquide', '1',
            'Oignon rouge', '1',
            'Tomate', '1'
        ],
        'riz brocolis + poisson': 
        [
            'Riz', '90',
            'Brocolis surgelé', '1', 
            'Poisson panure', '1'
        ],
        'ricotta miel noix': 
        [
            'Ricotta', '1'
        ],
        'croque-monsieur': 
        [
            'Pain de mie', '1',
            'Jambon', '4',
            'Toastinette', '1',
            'Beurre', '1',
            'Fromage rapé', '1'
        ]
    }


    list_of_recipes = []
    for recipe in list_of_recipe_strings:
        # print(recipe.capitalize())
        recipe_to_add = Recipe(name=recipe.capitalize())
        # Add recipe here
        db.session.add(recipe_to_add)
        # list_of_recipes.append(recipe_to_add)
        o = 0
        while o != len(list_of_recipe_strings[recipe]):
            article_name = list_of_recipe_strings[recipe][o]
            article_quantity = list_of_recipe_strings[recipe][o+1]
            article_to_add = Article.query.filter_by(name=article_name).first()
            if not article_to_add:
                print(article_to_add)
                print(f'{article_name} is none')
            recipe_to_add.article.append(article_to_add)
            o += 2
        # for ingredient in list_of_recipe_strings[recipe]:
        #     print('     '+ingredient)
        #     article_to_add = Article.query.filter_by(name=ingredient).first()
        #     if not article_to_add:
        #         print(article_to_add)
        #         print(f'{ingredient} is none')
        #     recipe_to_add.article.append(article_to_add)

    db.session.commit()

    for recipe in list_of_recipe_strings:
        print(recipe.capitalize())
        recipe_id = Recipe.query.filter_by(name=recipe.capitalize()).first().id
        print(str(recipe_id))
        # Add recipe here
        # list_of_recipes.append(recipe_to_add)
        o = 0
        print(list_of_recipe_strings[recipe])
        while o != len(list_of_recipe_strings[recipe]):
            article_name = list_of_recipe_strings[recipe][o]
            article_quantity = list_of_recipe_strings[recipe][o+1]
            print('     '+article_name+'  '+article_quantity)
            article_id = Article.query.filter_by(name=article_name).first().id
            print('     '+str(article_id))
            print()
            print(f'recipe_id {recipe_id} article_id {article_id}')
            r_a = recipe_article.update().where(
                (recipe_article.c.recipe_id == recipe_id) & 
                (recipe_article.c.article_id == article_id)
                ).values(quantity=article_quantity)
            db.session.execute(r_a)
            db.session.commit()
            o += 2