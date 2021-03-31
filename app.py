import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import StringField, SubmitField, SelectField, FileField, IntegerField, BooleanField, FieldList
from wtforms.validators import DataRequired, NoneOf, AnyOf, ValidationError
from wtforms.fields.html5 import URLField, TimeField


app = Flask(__name__)
app.config["SECRET_KEY"] = "fDFJ8321knfIHFE3802Nef"
app.config["UPLOAD_PATH"] = "uploads"
csrf = CsrfProtect(app)
Bootstrap(app)


# def comma_check(form, field):
#     if "," in form.field.data:
#         raise ValidationError("List of numbers can not contain commas, only spaces between numbers")
#
#     len_of_list = len(form.std_conc.data.strip().split(" "))
#     if len_of_list != 6 and len_of_list != 12:
#         raise ValidationError(f"List should contain either 6 of 12 concentrations. List contains {len_of_list}")


class ParserForm(FlaskForm):
    proj_name = StringField(label="Project Name: ", validators=[DataRequired()])
    plate_num = IntegerField(label="Plate Number: ", validators=[DataRequired()])
    first_rep = BooleanField(label="First plate in replicate")
    last_rep = BooleanField(label="Last plate in replicate")
    all_rep = BooleanField(label="All plates in replicate")
    points = SelectField(label="Is this a 4 pt of 8 pt run: ", choices=[4, 8], validators=[DataRequired()])
    std_row = StringField(label="Enter standard row letter(s) e.g. 'H' or 'G H'")
    std_pos = SelectField(label="Half or Full standard row: ", choices=["", "Half", "Full"])
    std_conc = StringField(label="Enter standard concentration eg 200 100 50 25")
    raw_file = FileField(label="Upload Raw File: ",)
    submit = SubmitField(label="Add Project")



# @app.route("/")
# def home():
#     return render_template("index.html")
#
#

@app.route("/", methods=["POST", "GET"])
def home():
    form = ParserForm()
    file_list = os.listdir('uploads')
    if form.validate_on_submit():
        print(form.proj_name.data)
        print(form.std_conc.data)
        # uploaded_raw = form.raw_file.data
        # uploaded_raw.save(os.path.join(app.config["UPLOAD_PATH"], uploaded_raw.filename))
        # form.proj_name.data = ""
        return render_template("index.html", form=form)
    return render_template('index.html', form=form)

# @app.route("/remove")
# def remove_files():
#     file_list = os.listdir('uploads')
#     return render_template('remove.html', files=file_list)

if __name__ == "__main__":
    app.run(debug=True)
