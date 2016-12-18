from flask import *
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Purgna11012@localhost/chetan'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db= SQLAlchemy(app)
DATABASE = 'chetan'

#to map the table in the databse to the python objects we need to define a class

class Expenses(db.Model):
    __tablename__= 'Expenses'
    id=db.Column('id',db.Integer, primary_key=True)
    name=db.Column('Name',db.String(400))
    email=db.Column('email',db.String(100))
    category=db.Column('category',db.String(100))
    description=db.Column('description',db.String(200))
    link=db.Column('link',db.String(100))
    estimated_costs=db.Column('estimated_costs',db.String(100))
    status=db.Column('status',db.String(500))
    submit_date=db.Column('submit_date',db.String(500))
    decision_date=db.Column('decision_date',db.String(500))


# to be able to insert i need to create a constructor that allows you to create new expence objects
#when u want to add something new.

    def __init__(self,name='',email='',category='',description='',link='',estimated_costs='',status='',submit_date='',decision_date=''):
        self.name=name
        self.email=email
        self.category=category
        self.description=description
        self.link=link
        self.estimated_costs=estimated_costs
        self.status=status
        self.submit_date=submit_date
        self.decision_date=decision_date
#sqlalchemy will take care of mapping the data back to the database once we insert the

#db.create_all()
class CreateDB():
    engine = sqlalchemy.create_engine('mysql://root:Purgna11012@localhost/chetan')
    engine.execute("CREATE DATABASE IF NOT EXISTS %s;" %(DATABASE))
    engine.execute("USE chetan")
    db.create_all()
    db.session.commit()



