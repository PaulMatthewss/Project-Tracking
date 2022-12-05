from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/workers')
def workers():
    return render_template('workers.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/newworker')
def newworker():
    return render_template('newworker.html')

@app.route('/newproject')
def newproject():
    return render_template('newproject.html')

if __name__ == "__main__":
    app.run(debug=True)