from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bijxwcyjcoptsd:61eaff35b019360884a9617ad04dd41a47918e02804ec6c8762c97134747761d@ec2-54-163-234-88.compute-1.amazonaws.com:5432/d9obuqceoutoms'

heroku = Heroku(app)
db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(120))
    author = db.Column(db.String(80))

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return '<Title %r>' % self.title

@app.route('/')
def home():
    return "<h1>Hi from Flask</h1>"

@app.route('/books/input', methods=['POST'])
def books_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        title = post_data.get('title')
        author = post_data.get('author')
        reg = Books(title, author)
        db.session.add(reg)
        db.session.commit()
        return jsonify("Data Posted")
    return jsonify('Something went wrong')

@app.route('/books', methods=['GET'])
def return_books():
    all_books = db.session.query(Books.id, Books.title, Books.author).all()
    return jsonify(all_books)

if __name__ == '__main__':
    app.debug = True
    app.run()