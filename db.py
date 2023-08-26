from sqlalchemy import create_engine, Column, Integer,  String, text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
import datetime

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

    def __repr__(self):
        return f"<User(name='{self.name}', age='{self.age}')>"
    
    def __getDetails__(self):
        return [self.id, self.name, self.year, self.discord_id, self.roll_number]
Base.metadata.create_all(engine)
session = Session()

# user1 = User(id='5675', name='fada', year=1212, discord_id=1123068928834899933, roll_number='2115044')
# session.add(user1)
# session.commit()
# users = session.query(User).all()
def addStudent(id, name, batch, roll_number, time_stamp):
    user1 = User(id=id, name=name, batch=batch, roll_number=roll_number)
    session.add(user1)
    session.commit()

d = datetime.datetime.now()

addStudent(212123123,'nameeafda', 2077, 212313 , d)
result = engine.execute(text("SELECT * FROM students"))

for row in result:
    print(row)
    
