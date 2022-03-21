from flask import Flask, request, render_template, url_for, redirect

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
#tạo đối tượng lớp Flask
app=Flask(__name__)
#tạo cors


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy()
db.init_app(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        #lấy người dùng nhập và thêm vào database
        task_content=request.form.get('content')
        new_task=Todo(content=task_content)
        #thêm sp vào database nếu được
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was no issue adding your task'
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    #truy vấn lấy cái id
    #xóa id
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

#Xây dựng hàm update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    #lấy id hàng cần update
    task=Todo.query.get_or_404(id)
    #nếu là post
    if request.method=='POST':
        #lấy thông tin người dùng update
        task.content=request.form.get('content')
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updatting your task'
    else:
        return render_template('update.html', task=task)
if __name__=='__main__':
    app.run(debug=True)