from flask import render_template, redirect, request, send_from_directory, send_file
from App.settings import basedir
from App import app
import os
from App.converterController import converterController
from App.contactController import contactController


class pagesController:
    error_message = ""

    def show(self, filename="main"):
        dir_pages = os.listdir(os.path.join(basedir, "templates", "pages"))
        if filename + ".html" in dir_pages:
            return render_template("pages/" + filename + ".html")
        else:
            return redirect(app.config.app_url + "error/")

    def download_file(self, filename):
        return send_from_directory("downloads", filename)

    def error_page(self, e):
        return render_template("pages/error-page.html", error_text=e)

    def received_message(self):
        if request.method == 'POST':
            return contactController().received_message()
        else:
            return redirect(app.config.app_url + 'error/')

    def result(self):
        if request.method == 'POST':
            if 'input_type' in request.form:

                type_of_action = request.form['input_type']
                if type_of_action == "txt":
                    return converterController().start_txt_converter()
                elif type_of_action == "file":
                    return converterController().start_file_converter()
                else:
                    self.error_message = "there is an error in your request please replay it"
                    return render_template("pages/result.html", message=self.error_message)
            else:
                self.error_message = "there is an error in your request please replay it"
                return render_template("pages/result.html", message=self.error_message)

        elif request.method == 'GET':
            return redirect(app.config.app_url + 'error/')

    def showstaticfiles(self, filename):
        return send_from_directory(os.path.join("downloads", "staticFiles"), filename)
