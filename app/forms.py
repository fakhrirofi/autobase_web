from .models import User, Autobase
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

def check_username(name):
    allowed_chars = ("1234567890"
                     "abcdefghijklmnopqrstuvwxyz"
                     "_")
    for x in name:
        if x.lower() not in allowed_chars:
            raise ValidationError("Please use only alphabets, numbers, and/or underscore.")

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=12)])
    submit_profile = SubmitField('Update')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        check_username(username.data)
        if username.data.lower() == self.original_username.lower():
            return
        if User.query.filter(func.lower(User.username)==username.data.lower()).first() is not None:
            raise ValidationError('Please use a different username.')

class EditPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=20)])
    password2 = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('password')])
    submit_password = SubmitField('Update')

    def __init__(self, current_user, *args, **kwargs):
        super(EditPasswordForm, self).__init__(*args, **kwargs)
        self.current_user = current_user

    def validate_old_password(self, old_password):
        if not self.current_user.check_password(old_password.data):
            raise ValidationError('Wrong Password!')
    
    def validate_password(self, password):
        if password.data == self.old_password.data:
            raise ValidationError('Please use a different password.')

class AutobaseForm(FlaskForm):
    name = StringField("App Name", validators=[DataRequired()])
    consumer = StringField("Consumer", validators=[DataRequired()])
    secret = StringField("Secret", validators=[DataRequired()])
    status = BooleanField("App Status")
    submit_reset = SubmitField("Reset")
    submit_update = SubmitField("Update")

    def __init__(self, current_app, *args, **kwargs):
        super(AutobaseForm, self).__init__(*args, **kwargs)
        self.current_app = current_app

    def validate_name(self, name):
        check_username(name.data)
        if self.current_app is None:
            pass
        elif name.data.lower() == self.current_app.name.lower():
            return
        if Autobase.query.filter(func.lower(Autobase.name)==name.data.lower()).first() is not None:
            raise ValidationError("Please use a different app name.")

    def validate_consumer(self, consumer):
        if self.current_app is None:
            pass
        elif consumer.data == self.current_app.consumer and self.secret.data == self.current_app.secret:
            return
        for app in Autobase.query.all():
            if consumer.data == app.consumer and self.secret.data == app.secret:
                raise ValidationError('Please use a different credentials.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
