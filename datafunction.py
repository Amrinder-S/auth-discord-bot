from sqlalchemy import create_engine, Column, Integer,  String, text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from datetime import datetime

engine = create_engine("sqlite:///file.db", poolclass=QueuePool)
Session = sessionmaker(bind=engine)
Base = declarative_base()
class User(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    batch = Column(Integer)
    roll_number = Column(Integer)
    time_stamp = Column(DateTime)
    
Base.metadata.create_all(engine)
session = Session()

# user1 = User(id='5675', name='fada', year=1212, discord_id=1123068928834899933, roll_number='2115044')
# session.add(user1)
# session.commit()
# users = session.query(User).all()
def addStudent(id, name, batch, roll_number):
    time_stamp = datetime.now()
    user1 = User(id=id, name=name, batch=batch, roll_number=roll_number, time_stamp=time_stamp)
    session.add(user1)
    session.commit()

def removeStudent(id):
    result = engine.execute(f"DELETE FROM students WHERE id={id}")

def getStudent(id):
    result = engine.execute(f"SELECT * FROM students where id={id}")
    for row in result:
        return row

def getAll():
    all_items = session.query(User).all()
    return all_items

class Otp(Base):
    __tablename__ = 'otp'
    id = Column(Integer, primary_key = True)
    email = Column(String)
    otp = Column(String)

def addOtp(id, email, otp):
    otp = Otp(id = id, email = email, otp = otp)
    session.add(Otp)
    session.commit()

def removeOtp(id):
    result = engine.execute(f"DELETE FROM otp WHERE id={id}")

def checkOtp(email):
    result = engine.execute(f"SELECT * FROM otp WHERE email={email}")
    for row in result:
        return row

def getEmail(id):
    result = engine.execute(f"SELECT * FROM otp WHERE id={id}")
    for row in result:
        return row
