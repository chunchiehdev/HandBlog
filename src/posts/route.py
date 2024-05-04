from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from .. import db
from ..models import Posts
from ..posts.form import PostForm, SearchForm

posts = Blueprint('posts', __name__)

# 點入每一個文章
@posts.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)    

# 編輯文章
@posts.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required 
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        #post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        
        # 更新資料庫
        db.session.add(post)
        db.session.commit()
        flash('Update Suceesfully！')
        return redirect(url_for('posts.post',id = post.id))

    if current_user.id == post.poster_id:
            
        form.title.data = post.title
        #form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else:
        flash('No Access')
        redirect(url_for('main.home'))

# 刪除文章
@posts.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id 
    if id == post_to_delete.poster.id or 1:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            flash("Delete Suceesfully！")
            return redirect(url_for('main.home'))

        except:
            flash("Delete Error！")
            return redirect(url_for('main.home'))
    else:
            flash("No Access")
            redirect(url_for('main.home'))

# 添加文章
@posts.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(
            title = form.title.data,
            content = form.content.data,
            poster_id = poster,
            slug = form.slug.data)

        # 清除表單
        form.title.data = ''
        form.content.data = ''
        #form.author.data = ''
        form.slug.data = ''

        # 添加資料到資料庫
        db.session.add(post)
        db.session.commit()
        flash('Add Suceesfully！')
        return redirect(url_for('main.home'))
        # 重新定向至網頁
    return render_template("add_post.html", form=form)

# 建立搜索方法
@posts.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # 取得搜索欄資料
        post.searched = form.searched.data
        # 找尋資料庫資料
        posts = posts.filter(Posts.title.like('%' + post.searched + '%')) | (Posts.content.like(f'%{post.searched}%'))
        posts = posts.order_by(Posts.title).all()
        
        return render_template("search.html", form=form, searched = post.searched, posts=posts)

@posts.context_processor
def base():
    form = SearchForm()
    return dict(form=form)
