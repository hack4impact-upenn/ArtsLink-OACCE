from flask import render_template
from ..models import EditableHTML
from flask.ext.login import (
    login_required,
    login_user,
    logout_user,
    current_user
)
from . import main



@org.route('/')
def index():
    return render_template('org/welcome_page.html')

@org.rout('/login')
def org_login():
	return render_template('org/login.html')

@org.route('view-profile/')
@login_required
def view_profile():
    return render_template('org/view_profile.html',
                           current_user=current_user)

@org.route('edit-profile/<int:org_id>')
@login_required
def edit_profile(org_id):
    return render_template('org/edit_profile.html',
                           current_user=current_user)