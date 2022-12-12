from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

#Flask instance
app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdata.db'
# Secret Key
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to see"

# Initialize the database
db = SQLAlchemy(app)
db.init_app(app)

# Database model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(100), nullable=False)
    education = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    s_media = db.Column(db.String(100))
    managers = db.relationship('Manager', backref='person')
    stats = db.relationship('Stat', backref='person')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    stats = db.relationship('Stat', backref='project')

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    projects = db.relationship('Project', backref='manager')

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    m_name  = db.Column(db.String(25), nullable=False, unique=True)
    picture = db.Column(db.BLOB)
    stats = db.relationship('Stat', backref='mark')

class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_number = db.Column(db.Integer, nullable=False, unique=True)
    s_name = db.Column(db.String(100), nullable=False, unique=True)
    stats = db.relationship('Stat', backref='stage')

class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'))
    mark_id = db.Column(db.Integer, db.ForeignKey('mark.id'))

with app.app_context():
    db.create_all()

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
        flash("Новый сотрудник был успешно добавлен")

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
        flash("Новый проект был успешно добавлен")

    return render_template('newproject.html',
        project_name = project_name,
        project_manager = project_manager,
        project_description = project_description,
        form = form)

#Invalid pages
@app.errorhandler(404)
def error404(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def error500(e):
    return render_template(500), 500

if __name__ == "__main__":
    app.run(debug=True)