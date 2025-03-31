import os

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    cover_url = db.Column(db.String(255))  # Add to Book class


@app.route('/')
def index():
    query = request.args.get('q')
    if query:
        books = Book.query.filter(
        Book.title.ilike(f'%{query}%') |
        Book.author.ilike(f'%{query}%')
        ).all()
    else:
        books = Book.query.all()
    return render_template('index.html', books=books, query=query)


@app.route('/add', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        status = request.form['status']
        cover_url = request.form['cover_url']
        new_book = Book(title=title, author=author, status=status, cover_url=cover_url)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.status = request.form['status']
        book.cover_url = request.form['cover_url']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book)


@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
