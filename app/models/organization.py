from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db, login_manager


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


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), nullable=False)
    tag_type_id = Column(Integer, ForeignKey('tag_type.id'))
    tag_type = relationship("TagType", back_populates="tag")
    organizations = db.relationship("TagAssociation", back_populates="tag")


class TagAssociation(db.Model):
    __tablename__ = 'tag_association'
    id = db.Column(db.Integer, primary_key=True)
    organiztion_id = db.Column(db.Integer,
                               db.ForeignKey(
                                   'organizations.id', ondelete='CASCADE'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'))
    tag = db.relationship("Tag", back_populates="organizations")
    organization = db.relationship("Organization", back_populates="tags")


class TagType(db.Model):
    __tablename__ = 'tag_type'
    id = db.Column(db.Integer, primary_key=True)
    tag_type_name = db.Column(db.String(120), nullable=False)
    tags = db.relationship("Tag", back_populates="tag_type")
