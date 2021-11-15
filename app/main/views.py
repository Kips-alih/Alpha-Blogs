from flask import render_template,request,redirect,url_for,abort,flash

from app.main.forms import UpdateProfile,BlogForm,CommentForm
from . import main
from ..models import  User,Blog,Comment
from flask_login import login_required,current_user
from .. import db,photos
from ..request import get_quotes


#views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data.
    '''

    title = 'Home - Welcome to Alpha Blogs App'

    quote = get_quotes()
    blogs = Blog.query.order_by(Blog.date_posted).all()

    
    return render_template('index.html', title = title,quote=quote,blogs=blogs)


@main.route('/user_blog', methods=['GET', 'POST'])
@login_required
def user_blog():
    blog_form = BlogForm()

    if blog_form.validate_on_submit():
        title = blog_form.title.data
        category=blog_form.category.data
        description=blog_form.description.data
        user_blog = Blog(title=title,category=category,description=description,user=current_user)

        user_blog.save_blog()
        db.session.add(user_blog)
        db.session.commit()
        
        return redirect(url_for('main.index'))
    else:
        blogs = Blog.query.order_by(Blog.date_posted).all()
    
    return render_template('blog.html', blogs=blogs,blog_form = blog_form)



@main.route('/user_blog/<id>', methods=['GET', 'POST'])
@login_required
def blog_comments(id):

    comments = Comment.query.filter_by(blog_id=id).all()
    blogs = Blog.query.get(id)
    if blogs is None:
        abort(404)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment( comment=comment_form.comment.data, blog_id=id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        comment_form.comment.data = ''
        return redirect(url_for('main.read_comments', id=id))

    return render_template('new_comment.html',blogs= blogs, comments=comments, comment_form = comment_form)

@main.route('/user_blog/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_blog(id):
    """
    Delete blog function that deletes the blog
    """
    blog = Blog.get_blog(id)

    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('main.index', username=current_user.username))



@main.route('/read_comments/<id>')
@login_required
def read_comments(id):
    comment = Comment.get_comments(id)
    return render_template('comments.html', comment=comment)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment =Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect (url_for('main.read_comments',id=id))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    profile_form = UpdateProfile()

    if profile_form.validate_on_submit():
        user.bio = profile_form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',profile_form =profile_form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
