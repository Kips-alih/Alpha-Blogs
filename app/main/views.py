from flask import render_template,request,redirect,url_for,abort

from app.main.forms import UpdateProfile
from . import main
from ..models import  User
from flask_login import login_required,current_user
from .. import db,photos




#views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data.
    '''

    title = 'Home - Welcome to Alpha Blogs App'

    
    return render_template('index.html', title = title,)



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
