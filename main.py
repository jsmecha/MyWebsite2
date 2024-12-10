from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
#from flask_ckeditor import CKEditor, CKEditorField
from wtforms.fields.simple import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap5
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('CSRF_SECRET_KEY')
#app.config['CKEDITOR_PKG_TYPE'] = 'basic'
Bootstrap5(app)
#ckeditor = CKEditor(app)


class EmailForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    phone = StringField(label='Phone')
    message = StringField(label="Leave your message", validators=[DataRequired()])
    submit = SubmitField(label="Send Message")


@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/project')
def project():
    return render_template('project.html')


@app.route('/contact')
def contact():
    form = EmailForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data
        print(f"{name}, {email}, {phone}, {message}")
        result = send_message(name, email, phone, message)
        if result:
            flash('Successfully send message.')
        else:
            flash('Failed to send message')

    return render_template('contact.html', form=form)


def send_message(name, email, phone, message):
    admin_email = os.environ.get('EMAIL')
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(admin_email, os.environ.get('APP_PASSWORD'))
        send_result = connection.sendmail(
            from_addr=email, to_addrs=admin_email,
            msg=f"Subject:{name} wants to contact you\n\n{message}\nFrom {name} ({phone})")
        if len(send_result) == 0:
            return True
        else:
            return False


if __name__ == "__main__":
    app.run(debug=True)