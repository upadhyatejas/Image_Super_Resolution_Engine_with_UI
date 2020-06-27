import os
import shutil

from flask import Flask, request, render_template, send_from_directory

__author__ = 'ibininja'

app = Flask(__name__)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    target1 = 'LR'
    if os.path.isdir(target1):
        shutil.rmtree('LR')
    if os.path.isdir('results'):
        shutil.rmtree('results')
        os.mkdir('results')
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'LR/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file[]"))
    for upload in request.files.getlist("file[]"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
    exec(open('test.py').read())
    # return send_from_directory("images", filename, as_attachment=True)
    # return render_template("complete.html", image_name=filename)
    return get_gallery()


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("results", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./results')
    print(image_names)
    return render_template("result.html", image_names=image_names)


if __name__ == "__main__":
    app.run(port=4555, debug=True)
