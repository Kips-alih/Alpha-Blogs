from wtforms import StringField,TextAreaField, SubmitField, SelectField
from wtforms.validators import Required,Email
from flask_wtf import FlaskForm


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    title = StringField('Blog title', validators=[Required()])
    category = SelectField('Blog category',choices=[('Choose category','Choose category'),('Lifestyle', 'Lifestyle'),('News','News'),('Sports','Sports'),('Politics','Politics'),('Fashion','Fashion'),('Travel', 'Travel')], validators=[Required()])
    description = StringField('What is your blog?')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment = StringField('Comment here', validators=[Required()])
    submit = SubmitField('Submit')


class SubscriptionForm(FlaskForm):
    email=SelectField('Enter your email adress',validators=[Required(),Email()])
    submit=SubmitField('Subscribe')