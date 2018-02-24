from flask import render_template, flash, redirect, url_for
from flask_login import (login_required, current_user)
from . import org
from ..decorators import organization_required
from .forms import OrganizationForm
from ..models import Organization
from .. import db


@org.route('/')
def index():
    return render_template('org/welcome_page.html')


@org.route('/<int:org_id>')
def view_org(org_id):
    organization = Organization.query.filter_by(id=org_id).first()
    pics = []
    if len(organization.picture_urls) > 0:
        pics = organization.picture_urls.split(",")
    return render_template(
        'org/view_profile.html', org=organization, pics=pics)


# Organization edits its own profile
# Viewing the updated profile redirects to org/<int:org_id> but with the
# org_id of the current_user
@org.route('/edit-profile', methods=["GET", "POST"])
@login_required
@organization_required
def edit_profile():
    form = OrganizationForm()
    organization = Organization.query.filter_by(user_id=current_user.id)\
                               .first()
    if form.validate_on_submit():
        if organization is None:
            organization = Organization()
            organization.user_id = current_user.id
        organization.name = form.name.data
        organization.email = form.email.data
        organization.phone = form.phone.data
        organization.address = form.address.data
        organization.website_link = form.website_link.data
        organization.hours = form.hours.data
        organization.description = form.description.data
        organization.tags = form.tags.data
        organization.picture_urls = form.picture_urls.data
        db.session.add(organization)
        db.session.commit()
        flash('Organization {} successfully updated. Redirecting you to ' +
              'profile page'.format(organization.name),
              'form-success')
        return redirect(url_for('org.view_org', org_id=organization.id))
    if organization is not None:
        form.name.data = organization.name
        form.email.data = organization.email
        form.phone.data = organization.phone
        form.address.data = organization.address
        form.website_link.data = organization.website_link
        form.hours.data = organization.hours
        form.description.data = organization.description
        form.tags.data = organization.tags
        form.picture_urls.data = organization.picture_urls
    return render_template('org/edit_profile.html', form=form)
