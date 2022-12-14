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
    fio = StringField("??????", validators=[DataRequired()])
    edu = StringField("??????????????????????", validators=[DataRequired()])
    phone = StringField("??????????????", validators=[DataRequired()])
    email = StringField("????.??????????", validators=[DataRequired()])
    socmid = StringField("??????.????????", validators=[DataRequired()])
    submit = SubmitField("??????????????????????")

class ProjectForm(FlaskForm):
    project_name = StringField("???????????????? ??????????????", validators=[DataRequired()])
    project_manager = SelectField("???????????????????????? ??????????????", choices=[], validate_choice=False)
    project_description = TextAreaField("???????????????? ??????????????", validators=[DataRequired()])
    submit = SubmitField("??????????????????????")

#Main page that logs you into system
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

#Page with all workers
@app.route('/workers')
def workers():
    our_workers = Person.query.order_by(Person.fio)
    return render_template('workers.html', our_workers = our_workers)

#Page with all projects
@app.route('/projects')
def projects():
    our_projects = Project.query.order_by(Project.p_name)
    return render_template('projects.html', our_projects = our_projects)

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
        worker = Person.query.filter_by(email=form.email.data).first()
        if worker is None:
            worker = Person(fio=form.fio.data, education=form.edu.data, phone=form.phone.data, email=form.email.data, s_media=form.socmid.data)
            db.session.add(worker)
            db.session.commit()

        form.fio.data = ''
        form.edu.data = ''
        form.phone.data = ''
        form.email.data = ''
        form.socmid.data = ''
        flash("?????????? ?????????????????? ?????? ?????????????? ????????????????")

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
    form.project_manager.choices = [(project_manager.id, project_manager.person_id) for project_manager in Manager.query.all()]
    #Validate Form
    if form.validate_on_submit():
        proj = Project.query.filter_by(p_name=form.project_name.data).first()
        if proj is None:
            proj = Project(p_name=form.project_name.data, manager_id=form.project_manager.data, description=form.project_description.data)
            db.session.add(proj)
            db.session.commit()
        form.project_name.data = ''
        form.project_manager.data = ''
        form.project_description.data = ''
        flash("?????????? ???????????? ?????? ?????????????? ????????????????")

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