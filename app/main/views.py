from flask import render_template
from ..models import EditableHTML

from . import main


@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template('main/about.html',
                           editable_html_obj=editable_html_obj)

@main.route('/list-orgs')
def list_orgs():
    return render_template('main/list-orgs.html')
