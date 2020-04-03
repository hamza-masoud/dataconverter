from flask import request
from App import app
import random
import string
import datetime


class securityClass:
    def chick_the_request(self, data):
        result = None
        for one in data:
            if one in request.form:
                if request.form[one] != '':
                    result = True
                else:
                    result = False
                    return result
            else:
                result = False
                return result
        return result

    def random_filename(self):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        ts = datetime.datetime.now().timestamp()
        random_key = ''.join(random.choice(letters) for i in range(app.config.file_name_length))
        return random_key + str(ts)

    def check_file_from_html(self, file_from_html):
        if file_from_html not in request.files:
            self.error_message = "there is some error in the application, please replay your request"
            return True

        json_file = request.files[file_from_html]
        if json_file.filename == '':
            self.error_message = "there is some error in your request, please check that you uploaded a json file"
            return True
