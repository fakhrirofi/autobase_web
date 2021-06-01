from ..forms import check_username
from ..models import User
from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    EqualTo,
    ValidationError,
    Length
)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=12)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    token = PasswordField('Token', validators=[DataRequired()])
    submit = SubmitField('Register')

    def __init__(self, register_token, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.register_token = register_token

    def validate_username(self, username):
        check_username(username.data)
        user = User.query.filter(func.lower(User.username)==username.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_token(self, token):
        if token.data != self.register_token:
            raise ValidationError('Wrong token')
