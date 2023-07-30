from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Events.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Events(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    council = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.String(500), nullable=False)
    time=db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        council=request.form['council']
        date_created= request.form['date_created']
        time=request.form['time']
        to = Events(title=title, desc=desc,council=council,date_created=date_created,time=time)
        db.session.add(to)
        db.session.commit()
        
    allevents = Events.query.all() 
    return render_template('index.html', allevents=allevents)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        council = request.form['council']
        date_created = request.form['date_created']
        time = request.form['time']
        to = Events.query.filter_by(sno=sno).first()
        to.title = title
        to.desc = desc
        to.council=council
        to.date_created=date_created
        to.time=time
        db.session.add(to)
        db.session.commit()
        return redirect("/")
        
    to = Events.query.filter_by(sno=sno).first()
    return render_template('update.html', to=to)

@app.route('/delete/<int:sno>')
def delete(sno):
    to = Events.query.filter_by(sno=sno).first()
    db.session.delete(to)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)