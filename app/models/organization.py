from .. import db
from .user import User
import random
from sqlalchemy.exc import IntegrityError
from faker import Faker

tag_association = db.Table('tag_association', db.Model.metadata,
                           db.Column('tag_id', db.Integer,
                                     db.ForeignKey('tags.id')),
                           db.Column('organization_id', db.Integer,
                                     db.ForeignKey('organizations.id')))


class Organization(db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(64), nullable=False)
    address = db.Column(db.Text)
    website_link = db.Column(db.String(120))
    hours = db.Column(db.Text)
    description = db.Column(db.Text)
    services = db.Column(db.Text)
    tags = db.relationship(
        "Tag", secondary=tag_association, back_populates="organizations")
    picture_urls = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def generate_fake(count=20):
        users = User.query.filter_by(role_id=1)
        usr_id = 0
        fake = Faker()

        tag_types = ['Discipline', 'Program Activity', 'Program Time',
                     'Age Group', 'Additional Consideration']
        num_tag_types = 5
        num_tags = 3  # num tags per tag type
        for i in range(num_tag_types):
            currTagType = TagType(tag_type_name=tag_types[i], )
            for j in range(num_tags):
                name = fake.word()+'_' + fake.word();
                print_name = name.replace('_',' ')
                tag = Tag(
                    tag_name=print_name,
                    tag_class_name=name,
                    tag_type=currTagType,
                    tag_type_id=currTagType.id)
                db.session.add(tag)
            db.session.add(currTagType)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
        for i in range(1, count):
            # Connect to a User ID
            curr_user_id = users[usr_id].id
            # choose what tag values to append to the org,
            # make TagAssociations for each
            tag_list = Tag.query.all()
            tags = random.sample(
                tag_list,
                7)
            org = Organization(
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                address=fake.address(),
                user_id=curr_user_id,
                tags =tags)
            db.session.add(org)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            usr_id += 1


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), nullable=False)
    tag_class_name = db.Column(db.String(64), nullable=False) # tag name no spaces for classname in HTML
    tag_type_id = db.Column(db.Integer, db.ForeignKey('tag_type.id'))
    tag_type = db.relationship("TagType", back_populates="tags")
    organizations = db.relationship(
        "Organization", secondary=tag_association, back_populates="tags")


class TagType(db.Model):
    __tablename__ = 'tag_type'
    id = db.Column(db.Integer, primary_key=True)
    tag_type_name = db.Column(db.String(120), nullable=False)
    tags = db.relationship("Tag", back_populates="tag_type")

    @staticmethod
    def generate_fake(count=20):
        fake = Faker()

        tag_types = ['Art Type', 'Art Activity', 'Program Time',
                     'Age Group', 'Other Needs']
        num_tag_types = 5
        num_tags = 3  # num tags per tag type
        for i in range(num_tag_types):
            currTagType = TagType(tag_type_name=tag_types[i], )
            for j in range(num_tags):
                name = fake.word()+'_' + fake.word();
                print_name = name.split('_')
                tag = Tag(
                    tag_name=print_name,
                    tag_class_name=name,
                    tag_type=currTagType,
                    tag_type_id=currTagType.id)
                db.session.add(tag)
            db.session.add(currTagType)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
