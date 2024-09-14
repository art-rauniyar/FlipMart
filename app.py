from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
import csv

popular_df = pickle.load(open('a.pkl','rb'))

bh=pickle.load(open('browser.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/index')
def index():
    # Past Purchase  History
    ratings = pd.read_csv('similar users.csv')
    ratings = ratings.dropna()

    popular_products = pd.DataFrame(ratings.groupby('ITEM',as_index=False)['Rating'].count())
    most_popular = popular_products.sort_values('Rating', ascending=False).reset_index()

    recommendation = []
    for i in range(6):
        item = []
        with open('Unique Items with ProductId.csv', 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                if row[0] == most_popular['ITEM'][i]:
                    price = row[2]
                    imgLink = row[4]
                    size = row[5]
                    id = row[1]
                    break

        item.extend([most_popular['ITEM'][i]])
        item.extend([price])
        item.extend([imgLink])
        item.extend([size])
        recommendation.append(item)
    print(recommendation)
    return render_template('index.html',
                           PRODUCT_NAME= list(bh['PRODUCT-NAME'].values),
                           PRICE=list(bh['PRICE'].values),
                           WEIGHT=list(bh['WEIGHT(kg)'].values),
                           image1=list(bh['IMAGE-LINK'].values),
                           
                           book_name = list(popular_df['ITEM'].values),
                           Categories=list(popular_df['Categories'].values),
                           votes=list(popular_df['Price'].values),
                           image=list(popular_df['Image Link'].values),
                           rating=list(popular_df['Size'].values),
                           data=recommendation
                            )

# Add the /recipe route
@app.route('/recipe')
def recipe_page():
    return render_template('recipe.html')

@app.route('/recipeinfo')
def recipe_info():
    return render_template('recipeinfo.html')

@app.route('/addcart')
def addcart():
    return render_template('addcart.html')

if __name__ == '__main__':
    app.run(debug=True)