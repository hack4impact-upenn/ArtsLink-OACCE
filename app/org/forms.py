from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields import (StringField, SubmitField, TextAreaField,
                            IntegerField)
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import Email, InputRequired, Length

from .. import db
from ..models import Organization, Tag


class MultipleFileUploadField(StringField):
    pass


class OrganizationForm(Form):
    name = StringField(
        'Organization Name (Required)', validators=[InputRequired(),
                                         Length(1, 64)])
    email = EmailField(
        'Organization Contact Email (Required)', validators=[InputRequired(),
                                                  Email()])
    phone = StringField(
        'Phone number (eg. 215-686-8446) (Required)',
        validators=[InputRequired(), Length(1, 40)])
    address = TextAreaField(
        'Organization Address')
    website_link = URLField(
        'Organization website address \
        (ex: http://hack4impact.org)')
    hours = TextAreaField(
        'Organization Hours of Operation')
    description = TextAreaField(
        'Description of your Organization (Required, max 500 characters)',
        validators=[InputRequired(), Length(1, 500)])
    services = TextAreaField(
        'Description of the services offered by your organization (max 500 characters)',
        validators=[Length(0, 500)])
    # TODO: tag type separation based on a DB query

    picture_urls = MultipleFileUploadField('Upload Photos')
    submit = SubmitField('Create')

    def validate_email(self, field):
        if Organization.query.filter_by(name=field.data).first():
            raise ValidationError('Name already registered.')
