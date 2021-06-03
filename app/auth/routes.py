from .. import app, db
from ..models import User
from . import auth
from .forms import (
    LoginForm,
    RegistrationForm
)
from flask import (
    flash,
    render_template,
    redirect,
    request,
    url_for
)
from flask_login import (
    current_user,
    login_user,
    login_required,
    logout_user
)
from sqlalchemy import func
from werkzeug.urls import url_parse

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', app_name=''))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.username)==form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard', app_name='')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', app_name=''))
    
    form = RegistrationForm(register_token=app.config['REGISTER_TOKEN'])
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)
