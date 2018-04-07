from .. import db
from .user import User
import random 

class Organization(db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    hours = db.Column(db.String(64))
    description = db.Column(db.Text)
    tags = db.relationship("TagAssociation", back_populates="organizations")
    picture_urls = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def generate_fake(count=20):
        from sqlalchemy.exc import IntegrityError
        from random import randint
        from faker import Faker
        users = User.query.filter_by(role_id=1)
        usr_id = 0
        fake = Faker()

        num_tag_types = 5
        num_tags = 3 # num tags per tag type
        tag_types = []
        tags = []
        for i in range(num_tag_types):
            currTagType = TagType(
                tag_type_name=fake.word(),
            )
            for j in range(num_tags):
                tag = Tag(tag_name = fake.word(), 
                    tag_type = currTagType, 
                    tag_type_id = currTagType.id)
                db.session.add(tag)
            db.session.add(currTagType)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()  
        for i in range(1,count):
            # Connect to a User ID
            curr_user_id = users[usr_id].id
            #choose what tag values to append to the org, make TagAssociations for each
            org = Organization(name=fake.name(), 
                email = fake.email(), 
                phone = fake.phone_number(), 
                address = fake.address(), 
                user_id = curr_user_id)
            db.session.add(org)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()  
            tag_list = Tag.query.all()
            tags = random.sample(tag_list, 7) #make an association bt this resource and these tags
            for tag in tags:
                tag_assoc = TagAssociation(organization_id=i, tag_id=tag.id)
                db.session.add(tag_assoc)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
            usr_id +=1 


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), nullable=False)
    tag_type_id = db.Column(db.Integer, db.ForeignKey('tag_type.id'))
    tag_type = db.relationship("TagType", back_populates="tags")
    organizations = db.relationship("TagAssociation", back_populates="tags")


class TagAssociation(db.Model):
    __tablename__ = 'tag_association'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    tags = db.relationship("Tag", back_populates="organizations")
    organizations = db.relationship("Organization", back_populates="tags")


class TagType(db.Model):
    __tablename__ = 'tag_type'
    id = db.Column(db.Integer, primary_key=True)
    tag_type_name = db.Column(db.String(120), nullable=False)
    tags = db.relationship("Tag", back_populates="tag_type")
    @staticmethod
    def generate_fake(count=20):
        from sqlalchemy.exc import IntegrityError
        from random import randint
        from faker import Faker

        fake = Faker()

        num_tag_types = 5
        num_tags = 3 # num tags per tag type
        tag_types = []
        tags = []
        for i in range(num_tag_types):
            currTagType = TagType(
                tag_type_name=fake.word(),
            )
            for j in range(num_tags):
                tag = Tag(tag_name = fake.word(), tag_type = currTagType, tag_type_id = currTagType.id)
                db.session.add(tag)
            db.session.add(currTagType)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()  
