from flask import render_template
from flask_login import (login_required, current_user)
from . import org
from ..decorators import organization_required
from .forms import OrganizationForm


@org.route('/')
def index():
    print('hi')
    return render_template('org/welcome_page.html')


@org.route('/<int:org_id>')
def view_org(org_id):
    return render_template('org/view_profile.html', org_id=org_id)


# Organization edits its own profile
# Viewing the updated profile redirects to org/<int:org_id> but with the
# org_id of the current_user
@org.route('/edit-profile')
@login_required
@organization_required
def edit_profile():
    form = OrganizationForm()
    return render_template('org/edit_profile.html', form=form)
