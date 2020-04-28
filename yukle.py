from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)

class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)



@app.route('/')
def upload_file():
   return render_template('index.html')
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    file = request.files['file']
    newfile = FileContents(name=file.filename, data=file.read())
    db.session.add(newfile)
    db.session.commit()
    return 'Kaydedildi.' + file.filename

@app.route('/download/<int:data>')
def download(data):
    file_data = FileContents.query.filter_by(id=data).first()
    return send_file(BytesIO(file_data.data), attachment_filename=file_data.name, as_attachment=True)

@app.route('/show/<int:data>')
def show(data):
    file_data = FileContents.query.filter_by(id=data).first()
    return show(BytesIO(file_data.data), attachment_filename=file_data.name, as_attachment=True)


if __name__ == '__main__':
   app.run(debug = True, port=8888)