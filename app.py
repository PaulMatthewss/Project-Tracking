from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired

#Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to see"
#Create a Form Class
class WorkerForm(FlaskForm):
    fio = StringField("ФИО", validators=[DataRequired()])
    edu = StringField("Образование", validators=[DataRequired()])
    phone = StringField("Телефон", validators=[DataRequired()])
    email = StringField("Эл.адрес", validators=[DataRequired()])
    socmid = StringField("Соц.сеть", validators=[DataRequired()])
    submit = SubmitField("Подтвердить")

class ProjectForm(FlaskForm):
    project_name = StringField("Название проекта", validators=[DataRequired()])
    project_manager = SelectField("Руководитель проекта", choices=[('Анна'), ('Павел'), ('Пётр')], validate_choice=False)
    project_description = TextAreaField("Описание проекта", validators=[DataRequired()])
    submit = SubmitField("Подтвердить")

#Main page that logs you into system
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

#Page with all workers
@app.route('/workers')
def workers():
    return render_template('workers.html')

#Page with all projects
@app.route('/projects')
def projects():
    return render_template('projects.html')

#Create a new worker
@app.route('/newworker', methods=['GET', 'POST'])
def newworker():
    fio = None
    edu = None
    phone = None
    email = None
    socmid = None
    form = WorkerForm()
    #Validate Form
    if form.validate_on_submit():
        fio = form.fio.data
        form.fio.data = ''
        edu = form.edu.data
        form.edu.data = ''
        phone = form.phone.data
        form.phone.data = ''
        email = form.email.data
        form.email.data = ''
        socmid = form.socmid.data
        form.socmid.data = ''

    return render_template('newworker.html',
        fio = fio,
        edu = edu,
        phone = phone,
        email = email,
        socmid = socmid,
        form = form)

#Create a new project
@app.route('/newproject', methods=['GET', 'POST'])
def newproject():
    project_name = None
    project_manager = None
    project_description = None
    form = ProjectForm()
    #Validate Form
    if form.validate_on_submit():
        project_name = form.project_name.data
        form.project_name.data = ''
        project_manager = form.project_manager.data
        form.project_manager.data = ''
        project_description = form.project_description.data
        form.project_description.data = ''

    return render_template('newproject.html',
        project_name = project_name,
        project_manager = project_manager,
        project_description = project_description,
        form = form)

if __name__ == "__main__":
    app.run(debug=True)