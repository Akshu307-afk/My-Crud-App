# Import
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My App
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Data class ~ row of Data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Task {self.id}>"

    with app.app_context():
        db.create_all()

# Routes to webpages
# home page
@app.route("/", methods=["GET", "POST"])
def index():
    # Add a task
    if request.method == "POST":  # <-- FIXED
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print (f'ERROR: {e}')
            return f"There was an issue adding your task: {e}"

    # See all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        print(tasks)
    return render_template('index.html', tasks=tasks)


# delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"There was a problem deleting that task: {e}"

# Edit an item
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"There was a problem updating that task: {e}"
    else:
        return render_template("edit.html", task=task)











#  Run and Debbuger
if __name__ == "__main__":
    app.run(debug=True)
