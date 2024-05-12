from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.Date)
    progress = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Todo {self.id}>"

@app.route('/', methods=['GET'])
def index():
    todos = Todo.query.order_by(Todo.id).all()
    return render_template('index.html', todos=todos)

@app.route('/new', methods=['GET', 'POST']) 
def new():
    if request.method == 'GET':
        return render_template('new.html')

    content = request.form['content']
    deadline = datetime.fromisoformat(request.form['deadline']).date()
    new_todo = Todo(content=content, deadline=deadline)

    try:
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    except:
        print('ERROR: Could not add todo to database')
        return "Todo could not be saved"

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')
    except:
        return "ERROR: Todo not deleted"

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('edit.html', todo=todo)

    todo.content = request.form['content']
    todo.deadline = datetime.fromisoformat(request.form['deadline']).date()
    todo.progress = request.form['progress']

    try:
        db.session.commit()
        return redirect('/')
    except:
        print('ERROR: Could not add todo to database')
        return "The changes could not be saved"

@app.route('/impressum', methods=['GET'])
def impressum():
    return render_template('impressum.html')


if __name__ == "__main__":
    # execute once to initialise the database
    # with app.app_context():
    #     db.create_all()
        
    app.run(debug=True, port=1234)
