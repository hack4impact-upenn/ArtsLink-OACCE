from flask import render_template
from flask_login import (login_required, current_user)
from . import org


@org.route('/')
def index():
    return render_template('org/welcome_page.html')


@org.route('/<int:org_id>')
def view_org(org_id):
    return render_template('org/view_profile.html', org_id=org_id)


# Organization edits its own profile
# Viewing the updated profile redirects to org/<int:org_id> but with the
# org_id of the current_user
@org.route('/edit-profile')
@login_required
def edit_profile():
    return render_template('org/edit_profile.html', current_user=current_user)
