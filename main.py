from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(import_name=__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy()

db.init_app(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note_content = request.form.get("note")
        if note_content:
            new_note = Note(note=note_content)
            db.session.add(new_note)
            db.session.commit()
            return redirect("/")
    else:
        notes = Note.query.all()
        return render_template("index.html", notes=notes)


app.run(port=8000, debug=True)
