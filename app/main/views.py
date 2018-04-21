from flask import render_template, request

from . import main
from ..models import EditableHTML
import boto3
import json
import time
import os
from ..models import Organization, Tag, TagType, User

@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)


@main.route('/list-orgs')
def list_orgs():
    return render_template('main/list-orgs.html')

@main.route('/search')
def search():
    # Search function
    orgs = [x for x in Organization.query.all() if User.query.get(x.user_id).approved == True]
    tags = Tag.query.all()
    classes = ""
    tag_types = TagType.query.all()
    return render_template(
        'main/search_orgs.html', orgs=orgs, tags=tags, classes=classes, tag_types=tag_types)


@main.route('/search/<string:tags>')
def search_tag(tags):
    all_tags = tags.split("_")
    send_orgs = []
    for t in all_tags:
        send_orgs.extend(Organization.query.join(Organization.tags).filter_by(tag_name=t).all())
    return render_template(
        'main/search_orgs.html', orgs=send_orgs, tags=tags, checked=all_tags)


# generates all signed URL for AWS upload
@main.route('/sign-s3/')
def sign_s3():
    # Load necessary information into the application
    S3_BUCKET = os.environ.get('S3_BUCKET')
    S3_REGION = os.environ.get('S3_REGION')
    TARGET_FOLDER = 'json/'
    # Load required data from the request
    pre_file_name = request.args.get('file-name')
    file_name = ''.join(pre_file_name.split('.')[:-1]) +\
                str(time.time()).replace('.',  '-') + '.' +  \
                ''.join(pre_file_name.split('.')[-1:])
    file_type = request.args.get('file-type')

    # Initialise the S3 client
    s3 = boto3.client('s3', 'us-west-2')

    # Generate and return the presigned URL
    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=TARGET_FOLDER + file_name,
        Fields={
            "acl": "public-read",
            "Content-Type": file_type
        },
        Conditions=[{
            "acl": "public-read"
        }, {
            "Content-Type": file_type
        }],
        ExpiresIn=60000)

    # Return the data to the client
    return json.dumps({
        'data':
        presigned_post,
        'url_upload':
        'https://%s.%s.amazonaws.com' % (S3_BUCKET, S3_REGION),
        'url':
        'https://%s.amazonaws.com/%s/json/%s' % (S3_REGION, S3_BUCKET,
                                                 file_name)
    })
