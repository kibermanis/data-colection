from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate
from send_email import send_email


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:<passw>@localhost:5433/height_api"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)
migrate = Migrate(app, db)

class Data(db.Model):
    __tabelname__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120),unique=True)
    height_=db.Column(db.Integer)
    
    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST']) #default for all decorators is GET method
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_value"]
        if db.session.query(Data).filter(Data.email_==email).count()==0:
            data=Data(email, height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data).count()
            send_email(email, height, average_height, count) # sends email using SMTP
            return render_template("success.html")
        return render_template("index.html", text="Email address already used!")

if __name__=='__main__':
    app.debug= False
    app.run()