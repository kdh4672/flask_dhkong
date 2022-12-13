from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect
import flask

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('main._content_list'))

@bp.route('/content_list/')
def _content_list():
    content_list = ['Face analysis using AI', 'OCR for blackbox video']
    return render_template('main/content_list.html', content_list=content_list)

@bp.route('/content_list/<int:content_id>/')
def _content(content_id):
    return render_template(f'main/content_{content_id}.html')


# @bp.route('/')
# def index():
#     return redirect(url_for('question._list'))
