import os
from flask import Flask, flash, request, redirect , render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
import json

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

try:
    with open('key.json') as fp:
        mydict = json.load(fp)
except:
    mydict={}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():

    global titles
    if request.args.get('file'):

        with open(request.args.get('file')) as f_obj:
            content = f_obj.readlines()

        titles = []
        links = []
        for item in mydict.items():
            titles.append(item[0]), links.append(item[1])
        return render_template('upload.html', the_title='Welcome', len=len(titles), titles=titles, links=links, file_content=content, numOfLines=len(content) , fileName = request.args.get('file'),showSubheading="Available Titles: " )

    elif request.method == 'POST':
        title = request.form['title']
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            mydict[title] = filename
            with open('key.json', 'w') as fp:
                json.dump(mydict, fp)

    titles = []
    links = []
    for item in mydict.items():
        titles.append(item[0]), links.append(item[1])

    if mydict == {}:
        return render_template('upload.html', the_title='Welcome',len=len(titles), titles=titles, links=links, numOfLines=0, showSubheading = "")
    else:
        return render_template('upload.html', the_title='Welcome', len=len(titles), titles=titles, links=links,
                               numOfLines=0, showSubheading="Available Titles: ")


@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.secret_key = 'super-secret-key'
    app.run(debug=True)
