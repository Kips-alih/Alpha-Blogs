from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime


#Added this code to solve the Exception: Missing user_loader or request_loader.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))

    blog = db.relationship('Blog',backref = 'user',lazy = "dynamic")
    comment = db.relationship('Comment',backref = 'user',lazy = "dynamic")

    # upvote = db.relationship('Like',backref='user',lazy='dynamic')
    # downvote = db.relationship('Dislike',backref='user',lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model): 
    _tablename_ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    category = db.Column(db.String)
    description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comment = db.relationship('Comment', backref='blog', lazy='dynamic')
    

    # save blog

    def save_blog(self):
        db.session.add(self)
        db.session.commit()
     
    #Delete blog 
    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()


    # get blog by id
    @classmethod
    def get_blog(cls, id):
        blog = Blog.query.filter_by(id=id).first()
        return blog

    @classmethod
    def get_blogs(cls,id):
            blogs =Blog.query.filter_by(blog_id=id).all()
            return blogs

    def _repr_(self):
        return f'Blog {self.title}'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer,db.ForeignKey("blog.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()
    

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id=id).all()
        return comments 
    
    def _repr_(self):

        return f'Comment {self.comment}'
class Quote:
    """
    Qoute blueprint
    """
    def __init__(self,quote, author):
        self.quote = quote
        self.author = author
