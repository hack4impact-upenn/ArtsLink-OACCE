from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields import (StringField, SubmitField,
                            TextAreaField, IntegerField)
from wtforms.fields.html5 import EmailField, URLField

from .. import db
from ..models import Organization, Tag


class MultipleFileUploadField(StringField):
    pass


class OrganizationForm(Form):
    name = StringField('Organization Name')
    email = EmailField('Organization Contact Email')
    phone = IntegerField('Phone number (eg 2108619271)')
    address = StringField('Organization Address')
    website_link = URLField('Organization website address \
            (eg http://hack4impact.org)')
    hours = StringField('Organization Hours of Operation')
    description = TextAreaField('Description of your organization')
    tags = QuerySelectMultipleField(
        'Tags to describe your organization',
        get_label='tag_name',
        query_factory=lambda: db.session.query(Tag).order_by('tag_name'))

    picture_urls = MultipleFileUploadField(
            'Upload Field')
    submit = SubmitField('Create')

    def validate_email(self, field):
        if Organization.query.filter_by(name=field.data).first():
            raise ValidationError('Name already registered.')
