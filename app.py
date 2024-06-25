from flask import Flask, render_template, request, send_file
import os
from main import scrape_reviews_to_csv

app = Flask(__name__)
reviews = []
output_file = 'reviews.csv'

def remove_file(filename):
    if os.path.exists(filename):  
        os.remove(filename)
        
def check(file):
     if os.path.exists(file): 
         return 1
     else:
         return 0 
remove_file('reviews.csv')

check = remove_file('reviews.csv')

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/submit', methods=['POST'])
def submit():
    url = request.form.get('name')
    scrape_reviews_to_csv(url, output_file,reviews)
    check = remove_file('reviews.csv')
    return render_template('index.html',file=check)

@app.route('/download_reviews')
def download_reviews():
    reviews_file = 'reviews.csv'
    if os.path.isfile(reviews_file):
        return send_file(reviews_file, as_attachment=True)
    else:
        return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=False)
