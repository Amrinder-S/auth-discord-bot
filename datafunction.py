from sqlalchemy import create_engine, Column, Integer,  String, text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from datetime import datetime

engine = create_engine("sqlite:///file.db", poolclass=QueuePool)
connection = engine.connect()
Session = sessionmaker(bind=engine)
Base = declarative_base()
class User(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    batch = Column(Integer)
    roll_number = Column(Integer)
    time_stamp = Column(DateTime)

class Otp(Base):
    __tablename__ = 'otp'
    id = Column(Integer, primary_key = True)
    email = Column(String)
    otp = Column(String)
Base.metadata.create_all(engine)
session = Session()

def addStudent(id, name, batch, roll_number):
    time_stamp = datetime.now()
    s = User(id=id, name=name, batch=batch, roll_number=roll_number, time_stamp=time_stamp)
    if s:
        session.add(s)
        session.commit()

def removeStudent(id):
    s = session.query(User).filter_by(id=id).first()
    if s:
        session.delete(s)
        session.commit()


def getStudent(id):
    s = session.query(User).filter_by(id=id).first()
    if s:
        return s


def getAll():
    all_items = session.query(User).all()
    if all_items:
        return all_items
    return False


def addOtp(id, email, otp):
    s = Otp(id=id, email=email, otp=otp)  # Create an instance of the Otp class
    if s:
        session.add(s)  # Add the instance to the session
        session.commit()

def removeOtp(id):
    s = session.query(Otp).filter_by(id=id).first()
    if s:
        session.delete(s)
        session.commit()

def checkOtp(id, msg):
    s = session.query(Otp).filter_by(id=id).first()
    if s:
        if s.otp == msg:
            return True
    return False

def checkOtpByEmail(mail):
    s = session.query(Otp).filter_by(email=mail).first()
    if s:
        return True
    return False

def checkOtpByUser(id):
    s = session.query(Otp).filter_by(id=id).first()
    if s:
        return True
    return False

def getEmailForOtp(id):
    s = session.query(Otp).filter_by(id=id).first()
    if s:
        return s.email
    return False

def getAllOtp():
    all_items = session.query(Otp).all()
    if all_items:
        return all_items
    return False
