from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Book, User
from . import db

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', books=books, user=current_user)

@main.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        review = request.form['review']

        new_book = Book(title=title, author=author, review=review, user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()
        
        flash('Book Added!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_book.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.review = request.form['review']
        db.session.commit()
        flash('Book Updated!', 'success')
        return redirect(url_for('main.index'))
    return render_template('edit_book.html', book=book)

@main.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted', 'success')
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            flash('Username Already Exists')
            return redirect(url_for('main.register'))
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account Created! Please log in')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged In Successfully!')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid Username or Password')
            return redirect(url_for('main.login'))
    return render_template('login.html')   

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('main.login'))