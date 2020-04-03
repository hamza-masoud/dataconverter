from flask import request, render_template
from App.securityClass import securityClass
from email.mime.text import MIMEText
import smtplib


class contactController:

    def received_message(self):

        if securityClass().chick_the_request(['name', 'email', 'title', 'message']):

            name = request.form['name']
            email = request.form['email']
            title = request.form['title']
            message = request.form['message']

            try:

                from_email = "hmzmsod@gmail.com"
                from_password = "Foxing@2020"
                to_email = "hamzahanimasoud@gmail.com"

                message = "<h1>{}</h1><h3>{},  {}</h3><p>{}</p>".format(title, name, email, message)

                msg = MIMEText(message, 'html')
                msg['Subject'] = title
                msg['To'] = to_email
                msg['From'] = from_email

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(from_email, from_password)
                server.send_message(msg)
                server.quit()

            except ConnectionError:
                return "error"

            return render_template("pages/thanks.html", name=name, error=False, message="")

        else:
            error_message = "there is an error in your request please replay it"
            return render_template("pages/thanks.html", message=error_message)
