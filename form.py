from flask import Flask, request, render_template,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,AnyOf
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'alesek'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class LoginForm(FlaskForm):
   username = StringField('username',validators=[InputRequired('Username is required'), Length(min=5, max=15, message="again")])
   password = PasswordField('password',validators=[InputRequired('password is required'),AnyOf(values=['ales','katka'],message="try again")])
   submit = SubmitField('Log In')

class Comments(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    comment = db.Column(db.String(200),nullable=False)
    posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)


@app.route('/',methods=['GET','POST'])
def ales():
    form = LoginForm()
    if form.is_submitted():
        result = Comments.query.all()
        return render_template('index.html',result=result)
    return render_template('pass.html',form=form)


@app.route('/process',methods=['POST'])
def process():
    name = request.form['name']
    comment = request.form['comment']
    posted = datetime.utcnow()

    signature = Comments(name=name,comment=comment,posted=posted)
    db.session.add(signature)
    db.session.commit()

    result = Comments.query.all()
    return render_template('index.html',result=result)

if __name__ == "__main__":
    app.run()
