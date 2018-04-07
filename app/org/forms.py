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
    name = StringField('Organization Name',
        validators=[InputRequired(), Length(1, 64)])
    email = EmailField('Organization Contact Email',
        validators=[InputRequired(), Email()])
    # TODO(steven): see if there is a better validator.
    # Also, might want to change to a StringField.
    phone = StringField('Phone number (eg 2108619271)',
        validators=[InputRequired()])
    address = StringField('Organization Address',
        validators=[InputRequired(), Length(1, 500)])
    website_link = URLField('Organization website address \
        (eg http://hack4impact.org)',
        validators=[InputRequired(), Length(1, 120)])
    hours = TextAreaField('Organization Hours of Operation',
        validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField('Description of your organization',
        validators=[InputRequired()])
    # TODO: tag type separation based on a DB query

    picture_urls = MultipleFileUploadField('Upload Photos')
    submit = SubmitField('Create')

    def validate_email(self, field):
        if Organization.query.filter_by(name=field.data).first():
            raise ValidationError('Name already registered.')
