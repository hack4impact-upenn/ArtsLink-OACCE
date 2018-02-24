from .. import db


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
    organiztion_id = db.Column(db.Integer,
                               db.ForeignKey(
                                   'organizations.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    tags = db.relationship("Tag", back_populates="organizations")
    organizations = db.relationship("Organization", back_populates="tags")


class TagType(db.Model):
    __tablename__ = 'tag_type'
    id = db.Column(db.Integer, primary_key=True)
    tag_type_name = db.Column(db.String(120), nullable=False)
    tags = db.relationship("Tag", back_populates="tag_type")
