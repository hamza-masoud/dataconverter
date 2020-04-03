from App import app
from App.pagesController import pagesController
from flask import request, redirect


@app.route('/')
def start(): return pagesController().show()


@app.route('/result/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        return pagesController().result()
    else:
        return redirect(app.config.app_url + 'error/')


@app.route('/send-message/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        return pagesController().received_message()
    else:
        return redirect(app.config.app_url + 'error/')


@app.route('/download/<filename>')
def download(filename): return pagesController().download_file(filename)


@app.errorhandler(404)
def error(e): return pagesController().error_page(e)


@app.route('/about-data-convert-online/')
def about(): return pagesController().show("about-data-convert-online")


@app.route('/data-converting-format/')
def data_converting_format(): return pagesController().show("data-converting-format")


@app.route('/contact/')
def contact(): return pagesController().show("contact")


@app.route('/what-is-json/')
def json(): return pagesController().show("what-is-json")


@app.route('/what-is-xml/')
def xml(): return pagesController().show("what-is-xml")


@app.route('/what-is-csv/')
def csv(): return pagesController().show("what-is-csv")


@app.route('/static-files/')
def examples(): return pagesController().show("global-data-in-examples")


@app.route('/static-files/<string:filename>')
def showstaticfiles(filename): return pagesController().showstaticfiles(filename)
