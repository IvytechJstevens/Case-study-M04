from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)  # Enable CORS support

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255), nullable=False)

# Use a context manager to create the database tables
with app.app_context():
    db.create_all()

# CRUD operations
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    if not all(key in data for key in ('book_name', 'author', 'publisher')):
        return jsonify({'error': 'Incomplete data. Please provide book_name, author, and publisher.'}), 400

    new_book = Book(book_name=data['book_name'], author=data['author'], publisher=data['publisher'])
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book created successfully'}), 201

@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_list.append({'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher})
    return jsonify({'books': book_list})

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher})

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    if 'book_name' in data:
        book.book_name = data['book_name']
    if 'author' in data:
        book.author = data['author']
    if 'publisher' in data:
        book.publisher = data['publisher']

    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
