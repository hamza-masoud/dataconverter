import os
from App import app

basedir = os.path.abspath(os.path.dirname(__file__))

app.secret_key = "data_convert"
app.config['UPLOAD_FOLDER'] = 'uploaded_files'

files_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'])

app.config.app_url = "https://dataconverter.website/"
app.config.download_url = app.config.app_url + "download/"

db_path = os.path.join(basedir, 'projectDB.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this separator use to split node and sub node in json
app.config.field_separator = "."
# length of random filename
app.config.file_name_length = 20
