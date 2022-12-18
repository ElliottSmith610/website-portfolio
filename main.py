from flask import Flask, render_template
from flask_bootstrap import *
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from smtplib import SMTP
import os
from dotenv import load_dotenv

load_dotenv()

MY_EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Required to use the CSRF token
Bootstrap(app)


class MessageForm(FlaskForm):
    email = EmailField(label="Your Email*", validators=[DataRequired(), Email()])
    name = StringField(label="Your Name*", validators=[DataRequired()])
    msg = TextAreaField(label="Message", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


@app.route("/")
def home():
    with app.open_resource('static/text/bio.txt') as text:
        bio = text.readlines()
    return render_template("index.html", bio=bio)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = MessageForm()
    message_success = False
    if form.validate_on_submit():
        with SMTP('smtp.gmail.com') as connect:
            connect.starttls()
            connect.login(user=MY_EMAIL, password=PASSWORD)
            connect.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                             msg=f"Subject: New mail from portfolio!\n\n"
                                 f"Email: {form.email.data}\n"
                                 f"Name: {form.name.data}\n"
                                 f"Message:\n{form.msg.data}")
            message_success = True
            return render_template("contact.html", form=form, message_success=message_success)
    return render_template("contact.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
