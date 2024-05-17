from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post

routes = Blueprint('routes', __name__)

@routes.route("/")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@routes.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('routes.home'))
        else:
            flash('Giriş başarısız. Lütfen e-posta ve şifrenizi kontrol edin.', 'danger')
    
    return render_template('login.html')

@routes.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Hesabınız oluşturuldu! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('routes.login'))
    
    return render_template('register.html')

@routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@routes.route("/account")
@login_required
def account():
    return render_template('account.html')