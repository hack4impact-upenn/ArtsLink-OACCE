from flask import render_template, flash, redirect, url_for
from flask_login import (login_required, current_user)
from . import org
from ..decorators import organization_required
from .forms import OrganizationForm
from wtforms.fields import SelectMultipleField
from ..models import Organization, TagType, Tag, User
from .. import db


@org.route('/')
def index():
    return render_template('org/welcome_page.html')


@org.route('/<int:org_id>')
def view_org(org_id):
    organization = Organization.query.filter_by(id=org_id).first()
    pics = []
    user = User.query.filter_by(id=organization.user_id).first()
    if user.approved is False:
        flash('The admin has not approved your organization', 'error') 
    if (organization.picture_urls is not None) and (len(
            organization.picture_urls) > 0):
        pics = organization.picture_urls.split(",")
    tag_types = TagType.query.all()
    return render_template(
        'org/view_profile.html',
        tag_types=tag_types,
        org=organization,
        pics=pics)


# Organization edits its own profile
# Viewing the updated profile redirects to org/<int:org_id> but with the
# org_id of the current_user
@org.route('/edit-profile', methods=["GET", "POST"])
@login_required
@organization_required
def edit_profile():
    class moddedOrgForm(OrganizationForm):
        pass

    for tt in TagType.query.all():
        tags = [(str(x.id), x.tag_name)
                for x in Tag.query.filter_by(tag_type_id=tt.id).all()]
        setattr(
            moddedOrgForm, 'tag_{}'.format(tt.tag_type_name),
            SelectMultipleField(
                'Select Tags from the category {} to describe your organization: '.
                format(tt.tag_type_name),
                choices=tags))
    form = moddedOrgForm()
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
        organization.picture_urls = form.picture_urls.data
        ts = []
        for f in form:
            if f.name.find('tag_') > -1:
                for t in f.data:
                    ts.append(Tag.query.get(t))
        print(ts)
        organization.tags = ts
        db.session.add(organization)
        db.session.commit()
        flash('Organization {} successfully updated. Redirecting you to ' +
              'profile page'.format(organization.name), 'form-success')
        return redirect(url_for('org.view_org', org_id=organization.id))
    if organization is not None:
        form.name.data = organization.name
        form.email.data = organization.email
        form.phone.data = organization.phone
        form.address.data = organization.address
        form.website_link.data = organization.website_link
        form.hours.data = organization.hours
        form.description.data = organization.description
        for tt in TagType.query.all():
            matches = [
                str(x.id) for x in Tag.query.filter(
                    Tag.id.in_([x.id for x in organization.tags]))
                .filter(Tag.tag_type_id == tt.id).all()
            ]
            form['tag_{}'.format(tt.tag_type_name)].data = matches
        form.picture_urls.data = organization.picture_urls
    return render_template('org/edit_profile.html', form=form)
