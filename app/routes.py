from . import app, db
from .forms import (
    AutobaseForm,
    EditPasswordForm,
    EditProfileForm,
    EmptyForm,
)
from .models import Autobase
from flask import (
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    logout_user
)
import requests

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profile_form = EditProfileForm(original_username=current_user.username)
    password_form = EditPasswordForm(current_user=current_user)
    empty_form = EmptyForm()
    if profile_form.submit_profile.data:
        if profile_form.validate():
            current_user.username = profile_form.username.data
            db.session.commit()
            # requests.post('twt_autobase_url', json={
            #         'action':'edit-profile',
            #         'username':current_user.username
            #     }
            # )
            flash('Your profile change has been saved')
            return redirect(url_for('edit_profile'))
        else:
            pass  
    elif password_form.submit_password.data and password_form.validate():
        current_user.set_password(password_form.password.data)
        db.session.commit()
        flash('Your password change has been saved')
        return redirect(url_for('edit_profile'))
    else:
        profile_form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile', profile_form=profile_form,
                           password_form=password_form, empty_form=empty_form)

@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard_default():
    apps = current_user.autobase.all()
    form = EmptyForm()
    return render_template('dashboard.html', title='Dashboard', apps=apps, form=form)

@app.route('/dashboard/<app_name>', methods=['GET', 'POST'])
@login_required
def dashboard(app_name):
    app = current_user.autobase.filter_by(name=app_name).first_or_404()
    form = AutobaseForm(current_app=app)
    # form.validate() only called on first if-condition because the same form
    if form.submit_update.data:
        if form.validate():
            app.name = form.name.data
            app.consumer = form.consumer.data
            app.secret = form.secret.data
            app.status = form.status.data
            db.session.commit()
            flash('Your changed has been saved')
            return redirect(url_for('dashboard', app_name=form.name.data))
        else:
            pass
    # elif form.submit_reset.data:
    else:
        form.name.data = app.name
        form.consumer.data = app.consumer
        form.secret.data = app.secret
        form.status.data = app.status
    return render_template('edit_app.html', title=app_name, app=app, form=form)

@app.route('/delete_app/<app_name>', methods=['POST'])
@login_required
def delete_app(app_name):
    form = EmptyForm()
    if form.validate_on_submit():
        app = current_user.autobase.filter_by(name=app_name).first_or_404()
        db.session.delete(app)
        db.session.commit()
        flash(f'{app_name} has been deleted')
        return redirect(url_for('dashboard', app_name=''))
    else:
        return redirect(url_for('index'))

@app.route('/new_app', methods=['GET', 'POST'])
@login_required
def new_app():
    form = AutobaseForm(current_app=None)
    if form.validate_on_submit():
        app = Autobase(name=form.name.data, owner=current_user)
        app.consumer = form.consumer.data
        app.secret = form.secret.data
        db.session.add(app)
        db.session.commit()
        flash('Your app has been created')
        return redirect(url_for('dashboard', app_name=''))
    return render_template('new_app.html', title='New App', form=form)

@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    form = EmptyForm()
    if form.validate_on_submit():
        for a in Autobase.query.filter_by(user_id=current_user.id).all():
            db.session.delete(a)
        flash(f'Your account {current_user.username} has been deleted')
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
    return redirect(url_for('index'))
