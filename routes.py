from flask import render_template, request, redirect, url_for, flash
from passlib.hash import sha256_crypt
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/running")
def running():
    # Retrieve the 'csv' argument from the query string. Default to None if not provided.
    csv_file = request.args.get('csv', None)
    
    # Pass the 'csv' argument to the template.
    return render_template("running.html", csv=csv_file)


@app.route("/about")
def about():
    return render_template("index.html")


UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # Redirect to the 'running' route with the CSV filename as a query parameter
            return redirect(url_for('running', csv=filename))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)