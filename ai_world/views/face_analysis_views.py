import os
import json
import re

from PIL import Image
import flask
from flask import Blueprint, url_for, render_template, request
from flask import Blueprint, render_template
from werkzeug.utils import redirect
from torchvision import models
import torchvision.transforms as transforms
import hgtk


bp = Blueprint('face_analysis', __name__, url_prefix='/')
UPLOAD_PATH = 'ai_world/static/face_analysis/images/'
RELATIVE_PATH = 'face_analysis/images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
imagenet_class_index = json.load(open('ai_world/static/imagenet_class_index.json'))
model = models.densenet121(pretrained=True)
model.eval()

def transform_image(image_path):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(image_path)
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_path):
    tensor = transform_image(image_path=image_path)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def isHangul(text):
    text = hgtk.text.decompose(text)
    hangul = re.compile('[ㄱ-ㅣ가-힣]+')
    hanCount = len(hangul.findall(text))
    return hanCount > 0


@bp.route('/')
def index():
    return redirect(url_for('face_analysis._result'))


@bp.route('/face_analysis/result', methods = ['GET','POST'])
def _result():
    if request.method == 'POST':
        f = request.files['file']        
        file_format = f.filename.split('.')[-1]
        upload_path = os.path.join(UPLOAD_PATH, f'image.{file_format}')
        relative_path = os.path.join(RELATIVE_PATH, f'image.{file_format}')
        f.save(upload_path)
        class_id, class_name = get_prediction(image_path = upload_path)
        output = {}
        output['image_path'] = relative_path
        output['class_name'] = class_name
        
    return render_template('face_analysis/result.html', output=output)