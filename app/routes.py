from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post, Category

routes = Blueprint('routes', __name__)

@routes.route("/")
def home():
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template('home.html', posts=posts, categories=categories)

@routes.route("/new_post_home", methods=['POST'])
@login_required
def new_post_home():
    title = request.form.get('title')
    content = request.form.get('content')
    category_id = request.form.get('category')
    post = Post(title=title, content=content, author=current_user, category_id=int(category_id))
    db.session.add(post)
    db.session.commit()
    flash('Gönderiniz oluşturuldu!', 'success')
    return redirect(url_for('routes.home'))

@routes.route("/category/<int:category_id>")
def category_posts(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category.id).all()
    return render_template('category_posts.html', category=category, posts=posts)

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

@routes.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        current_user.username = username
        current_user.email = email
        db.session.commit()
        flash('Hesabınız güncellendi!', 'success')
        return redirect(url_for('routes.account'))

    return render_template('account.html')

@routes.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@routes.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category')
        post = Post(title=title, content=content, author=current_user, category_id=int(category_id))
        db.session.add(post)
        db.session.commit()
        flash('Gönderiniz oluşturuldu!', 'success')
        return redirect(url_for('routes.home'))

    return render_template('create_post.html', title='Yeni Gönderi Oluştur', categories=categories)

@routes.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@routes.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('Bu gönderiyi düzenleme yetkiniz yok.', 'danger')
        return redirect(url_for('routes.home'))

    categories = Category.query.all()
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.category_id = request.form.get('category')
        db.session.commit()
        flash('Gönderiniz güncellendi!', 'success')
        return redirect(url_for('routes.post', post_id=post.id))

    return render_template('create_post.html', title='Gönderiyi Güncelle', post=post, categories=categories)

@routes.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('Bu gönderiyi silme yetkiniz yok.', 'danger')
        return redirect(url_for('routes.home'))

    db.session.delete(post)
    db.session.commit()
    flash('Gönderiniz silindi!', 'success')
    return redirect(url_for('routes.home'))