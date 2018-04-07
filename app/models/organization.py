from .. import db

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
    address = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    hours = db.Column(db.Text)
    description = db.Column(db.Text)
    tags = db.relationship(
        "Tag", secondary=tag_association, back_populates="organizations")
    picture_urls = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), nullable=False)
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
        from sqlalchemy.exc import IntegrityError
        from random import randint
        from faker import Faker

        fake = Faker()

        num_tag_types = 5
        num_tags = 3  # num tags per tag type
        tag_types = []
        tags = []
        for i in range(num_tag_types):
            currTagType = TagType(tag_type_name=fake.word(), )
            for j in range(num_tags):
                tag = Tag(
                    tag_name=fake.word(),
                    tag_type=currTagType,
                    tag_type_id=currTagType.id)
                db.session.add(tag)
            db.session.add(currTagType)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
