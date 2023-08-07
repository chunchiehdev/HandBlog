from flask import current_app, render_template, session, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from handblog import db 
from handblog.models import Users, Posts
from handblog.users.form import LoginForm, UserForm, PasswordForm, ForgotPasswordFrom, SetForgotPasswordFrom
from werkzeug.security import generate_password_hash ,check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from handblog.mail.verify_token import generate_confirmation_token, confirm_token
from handblog.mail.emailBusiness import to_send_email
from handblog.posts.form import SearchForm
from flask import request, jsonify

users = Blueprint('users', __name__)


# 建立登入頁面
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(username = form.username.data).first()
            if user:
                # 檢查密碼
                if check_password_hash(user.password_hash, form.password.data):
                    login_user(user)
                    flash("Login Suceesfully")
                    return redirect(url_for('users.dashboard'))
                else:
                    flash("Password Error！")
            else:
                flash("User not exist")
        return render_template('login.html', form = form)

# 建立登出頁面
@users.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logout suceesfully！")
    return redirect(url_for('main.home'))

# 建立儀表板頁面
@users.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_song = request.form['favorite_song']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']

        # 檢查圖片檔案
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']

            # 建立圖檔名稱
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            # 設置 UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename

            # 儲存圖片
            saver = request.files['profile_pic']
            
            # 將圖片存將圖片存為字串存入資料庫
            name_to_update.profile_pic = pic_name

            try:
                db.session.commit()
                saver.save(os.path.join(current_app.root_path, 'static/image', pic_name))

                flash("Update Suceesfully！")
                return render_template("dashboard.html", 
                    form=form,
                    name_to_update = name_to_update)
            except:
                flash("Update Error！")
                return render_template("dashboard.html", 
                    form=form,
                    name_to_update = name_to_update)
        else:
                db.session.commit()
                flash("Update Suceesfully！")
                return render_template("dashboard.html", form=form, name_to_update = name_to_update)                         
    else:
        return render_template("dashboard.html", 
                form=form,
                name_to_update = name_to_update,
                id = id)

@users.route('/user/add', methods= ['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
        user = Users(username=form.username.data,name=form.name.data, email=form.email.data, favorite_song=form.favorite_song.data, password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('mail.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        to_send_email(user.email, subject, html)
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_song.data = ''
        form.password_hash.data = ''
        flash("Add Suceesfully！A confirmation email has been sent via email.")
        return redirect(url_for('users.login'))
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form = form, name=name, our_users=our_users)

@users.route('/confirmedthemail')
def send_to_confirmed_mail():
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    token = generate_confirmation_token(name_to_update.email)
    confirm_url = url_for('mail.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    to_send_email(name_to_update.email, subject, html)
    flash('A confirmation email has been sent via email.', 'success')
    return redirect(url_for('users.dashboard'))

@users.route('/delete/<int:id>')
@login_required
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    if id == current_user.id:
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('Delete Suceesfully！')
            our_users = Users.query.order_by(Users.date_added)
            return render_template('add_user.html', form = form, name=name, our_users=our_users)
        except:
            flash('Delete Error')
            return render_template('add_user.html', form = form, name=name, our_users=our_users)
    else:
        flash("No Access")
        return redirect(url_for('users.dashboard'))

@users.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_song =  request.form['favorite_song']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("Update Suceesfully！")
            return render_template("update.html", 
                form=form,
                name_to_update = name_to_update)
        except:
            flash("Update Error！")
            return render_template("update.html", 
                form=form,
                name_to_update = name_to_update)
    else:
        return render_template("update.html", 
                form=form,
                name_to_update = name_to_update,
                id = id)

@users.route('/password_reset', methods= ['GET', 'POST'])
def send_password_reset():
    form = ForgotPasswordFrom()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user:
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('users.password_reset', token=token, _external=True)
            html = render_template('send_password_mail.html', confirm_url=confirm_url)
            subject = "Please reset your password"
            to_send_email(user.email, subject, html)
            flash('Reset password has been sent via email.', 'success')
            return render_template('password_reset.html',form = form)
        else:
            form.email.data = ''
            flash('User is not exsit', 'danger')
            return render_template('password_reset.html',form = form)   
    return render_template('password_reset.html',form = form)

@users.route('/password_reset/<token>', methods= ['GET', 'POST'])
def password_reset(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    form = SetForgotPasswordFrom()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
        user = Users.query.filter_by(email=email).first_or_404()
        user.password_hash = hashed_pw
        try:
            db.session.add(user)
            db.session.commit()
            flash('You have reset your passwords. Thanks!', 'success')
            return redirect(url_for('users.login'))
        except:
            flash("Reset password error, try again", "danger")
            return render_template('set_password_reset.html',form = form)
    return render_template('set_password_reset.html',form = form)

@users.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        users = Users.query.order_by(Users.date_added)

        return render_template('admin.html', users=users)
    else:
        flash("No Access！")
        return redirect(url_for('users.dashboard'))

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Users.query.filter_by(username=username).first_or_404()
    posts = Posts.query.filter_by(poster=user).order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@users.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@users.route('/api/', methods=['GET'])
def api():
	info = dict()
	info['message'] = 'This is the API to consume blog posts'
	info['services'] = []
	info['services'].append({'url': '/api/posts', 'method': 'GET', 'description': 'Gets a list of posts'})
	return jsonify(info)

@users.route('/api/posts', methods=['GET'])
def api_get_posts():
	posts = Posts.query.all()
	return jsonify(posts)
