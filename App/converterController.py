import codecs
import csv

import json
import os

os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

from xlsxwriter.workbook import Workbook
import pandas as pandas
from flask import render_template, request

from App import app
from App.settings import basedir, files_path
from App.securityClass import securityClass


class converterController:
    error_message = ''

    def start_file_converter(self):
        if self.check_file_from_html('json_file'):
            return render_template("pages/result.html", message=self.error_message)

        json_file = self.save_file_from_html('json_file')

        if not self.validate_json_format(json_file[0], "file"):
            return render_template("pages/result.html", message=self.error_message)

        list_file = self.convert_json(json_file[0])

        matrix = self.matrix_to_html(list_file[0])

        list_file[0] = json_file[1] + ".csv"
        list_file[1] = json_file[1] + ".xlsx"

        return render_template("pages/result.html", message="", file=list_file, keys=matrix[0], data_to_show=matrix[1])

    # function to handle text entered json
    def start_txt_converter(self):
        if 'json_text' in request.form:
            json_txt = request.form['json_text']
        else:
            self.error_message = "there is an error in your request please replay it"
            return render_template("pages/result.html", message=self.error_message)

        # call function to validate json format
        if json_txt != '':
            if self.validate_json_format(json_txt, "text"):
                pass
            elif not self.validate_json_format(json_txt, "text"):
                return render_template("pages/result.html", message=self.error_message)
        elif json_txt == '':
            self.error_message = "the text that you send it is empty please full the input with json type"
            return render_template("pages/result.html", message=self.error_message)

            # call a function to convert to csv

        filename = os.path.join(files_path, securityClass().random_filename() + ".json")
        with open(filename, "w+", encoding='utf-8', errors='ignore') as file_to_convert:
            txt = json.loads(json_txt)
            json.dump(txt, file_to_convert, ensure_ascii=False)

        list_file = self.convert_json(filename)
        matrix = self.matrix_to_html(list_file[0])

        return render_template("pages/result.html", message='', file=list_file, keys=matrix[0], data_to_show=matrix[1])

    def check_file_from_html(self, file_from_html):
        if file_from_html not in request.files:
            self.error_message = "there is some error in the application, please replay your request"
            return True

        json_file = request.files[file_from_html]
        if json_file.filename == '':
            self.error_message = "there is some error in your request, please check that you uploaded a json file"
            return True

    def save_file_from_html(self, file_from_html):
        json_file = request.files[file_from_html]

        filename = securityClass().random_filename()

        json_file.save(os.path.join(files_path, filename + ".json"))
        return [os.path.join(files_path, filename + ".json"), filename]

    def validate_json_format(self, json_file, type_of_action):
        try:
            if type_of_action == "file":
                with open(json_file, errors='ignore') as f:
                    json.load(f)
            elif type_of_action == "text":
                json.loads(json_file)
            return True
        except ValueError as e:
            self.error_message = 'invalid json: %s' % e
            if type_of_action == "file":
                os.remove(json_file)
            return False

    # function to convert json to csv and create the files
    def convert_json(self, json_path):
        # convert json
        list = json_path.split(".")
        csv_file_path = ".".join(list[0:-1])

        with open(json_path, errors='ignore') as f:
            data = json.load(f)
            if isinstance(data, dict):
                n = [data]
                data = n
            z = 0
            x = []
            for row in data:
                x.append(self.flattenjson(data[z]))
                z += 1
        os.remove(json_path)

        with open(csv_file_path + "filetoconver.txt", "w") as file_to_convert:
            json.dump(x, file_to_convert)

        lines = []
        file = pandas.read_json(csv_file_path + "filetoconver.txt")
        file_t = file.T
        keys = file.keys()
        keys_t = file_t.keys()
        for ky in keys_t:
            lines.append(file_t[ky])
        os.remove(csv_file_path + "filetoconver.txt")

        csv_file_path = csv_file_path.split(os.sep)
        csv_file_path.remove(csv_file_path[len(csv_file_path) - 2])
        csv_file_path.insert(len(csv_file_path) - 1, "downloads")
        csv_file_path = os.sep.join(csv_file_path)

        with open(csv_file_path + "toedit.csv", 'w', encoding="utf-8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(keys)
            for line in lines:
                filewriter.writerow(line)

        with open(csv_file_path + "toedit.csv", encoding="utf-8") as input, open(csv_file_path + ".csv", 'w',
                                                                                 newline='',
                                                                                 encoding="utf-8") as output:
            non_blank = (line for line in input if line.strip())
            output.writelines(non_blank)

        os.remove(csv_file_path + "toedit.csv")

        csv_file = csv_file_path + ".csv"
        workbook = Workbook(csv_file_path + '.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csv_file, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()

        return [csv_file_path + ".csv", csv_file_path + ".xlsx"]

    def flattenjson(self, b, separator=app.config.field_separator, data_type='json'):

        if data_type == 'json':
            val = {}
            for i in b.keys():
                if isinstance(b[i], dict):
                    get = self.flattenjson(b[i], separator)
                    for j in get.keys():
                        val[str(i) + separator + str(j)] = (get[j])
                elif isinstance(b[i], list):
                    get = self.flattenjson(b[i], separator, 'list')
                    for j in get.keys():
                        val[str(i) + separator + str(j)] = (get[j])
                else:
                    val[i] = b[i]
            return val
        elif data_type == 'list':
            val = {}
            for i in b:
                i = b.index(i)
                if isinstance(b[i], dict):
                    get = self.flattenjson(b[i], separator)
                    for j in get.keys():
                        val[str(i) + separator + str(j)] = get[j]
                elif isinstance(b[i], list):
                    get = self.flattenjson(b[i], separator, 'list')
                    for j in get:
                        id = get.index(j)
                        val[str(i) + separator + str(id)] = j
                else:
                    val[i] = b[i]
            return val

    def matrix_to_html(self, file):

        data_in_matrix = []
        with open(file, "r", errors='ignore') as data_in_file:
            lines = data_in_file.readlines()
            for line in lines:
                line = ['{}'.format(x) for x in list(csv.reader([line], delimiter=',', quotechar='"'))[0]]

                data_in_matrix.append(line)

        keys = data_in_matrix[0]
        data_in_matrix.remove(data_in_matrix[0])

        return [keys, data_in_matrix]
