from sqlalchemy import String, Integer,Float
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
# from dotenv import load_dotenv

# load_dotenv()

database_name = 'parking'
database_name = 'd7lodd1m8mjqmv'
username = 'postgres'
username = 'sljvxkxylywizp'
password = 'password'
password = '609a4947240515ad5e61aa0153b378c29e907170ef6dfda59b4a9af11c3824b8'
host = 'localhost:5432'
host = 'ec2-54-164-40-66.compute-1.amazonaws.com:5432'
# DATABASE_URL: postgres://sljvxkxylywizp:609a4947240515ad5e61aa0153b378c29e907170ef6dfda59b4a9af11c3824b8@ec2-54-164-40-66.compute-1.amazonaws.com:5432/d7lodd1m8mjqmv
database_path= "postgres://{}:{}@ec2-3-216-113-109.compute-1.amazonaws.com:5432/{}".format(
    username, password, database_name
)


# database_path = "postgresql://{}:{}@{}/{}".format(
#     username, password, host, database_name
# )


db = SQLAlchemy()
migrate = Migrate(compare_type=True)
"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app,db)
    # db.create_all()



"""
User

"""
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(Integer, primary_key=True)
    full_name = db.Column(String, nullable=False)
    phone_number = db.Column(Integer, nullable=False)
    email = db.Column(String ,nullable=False,unique=True)
    password = db.Column(String ,nullable=False)
    reserve =db.relationship('Reservation',backref='users',lazy='dynamic')

    def __init__(self, full_name, phone_number, email, password):
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'password': self.password
        }


"""
County

"""


class County(db.Model):
    __tablename__ = 'counties'

    id = db.Column(Integer, primary_key=True)
    county_name = db.Column(String,unique=True ,nullable=False)
    place =db.relationship('Place', backref='counties', lazy='dynamic')

    def __init__(self, county_name):
        self.county_name = county_name
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'county_name': self.county_name
        }


'''
Place
'''
class Place(db.Model):
    __tablename__ ='places'
    id = db.Column(Integer, primary_key=True)
    place_name = db.Column(String,unique=True ,nullable=False)
    county_id = db.Column(Integer,db.ForeignKey("counties.id"))
    lot = db.relationship('Lot',backref='places',lazy='dynamic')

    def __init__(self,place_name,county_id):
        self.place_name = place_name
        self.county_id = county_id
        
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id':self.id,
            'place_name':self.place_name,
            'county_id':self.county_id
        }

'''
Lot
'''
class Lot(db.Model):
    __tablename__ = 'lots'

    id = db.Column(Integer, primary_key=True)
    place_id =db.Column(Integer,db.ForeignKey('places.id'))
    lot_number =db.Column(String,nullable=False,unique=True)
    lot_price =db.Column(Float,nullable=False)
    current_use = db.Column(String,default='green')
    reserve = db.relationship('Reservation',backref='lots',lazy='dynamic')

    def __init__(self, place_id,lot_number,lot_price):
        self.place_id = place_id
        self.lot_number = lot_number
        self.lot_price = lot_price
 

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    

    def format(self):
        return {
            "id":self.id,
            "place_id":self.place_id,
            "lot_number":self.lot_number,
            "lot_price":self.lot_price,
            "current_use":self.current_use
        }

    """
    Reserve
    """
class Reservation(db.Model):
    __tablename__ ='reservations'
    id = db.Column(Integer,primary_key=True)
    lot_id = db.Column(Integer,db.ForeignKey('lots.id'))
    vehicle_category = db.Column(String ,nullable=False) 
    vehicle_plate =db.Column(String,nullable=True)
    reserve_date = db.Column(String ,nullable=False)
    start_time = db.Column(String ,nullable=False)
    end_time = db.Column(String,nullable=False)
    user_id = db.Column(Integer,db.ForeignKey('users.id'))
    payment = db.relationship('Payment',backref = 'reservations',lazy='dynamic')

    def insert(self,lot_id,vehicle_category,vehicle_plate,reserve_date,
    start_time,end_time,user_id):
        self.lot_id =lot_id
        self.vehicle_category =vehicle_category
        self.vehicle_plate = vehicle_plate
        self.reserve_date =reserve_date
        self.start_time =start_time
        self.end_time =end_time
        self.user_id =user_id

      
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    def format(self):
        return{
            "id":self.id,
            "lot_id":self.lot_id,
            "vehicle_category":self.vehicle_category,
            "vehicle_plate":self.vehicle_plate,
            "reserve_date":self.reserve_date,
            "start_time":self.start_time,
            "end_time":self.end_time,
            "user_id":self.user_id

        }


"""
Payment
"""
class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(Integer,primary_key=True)
    reserve_id = db.Column(Integer,db.ForeignKey('reservations.id'))
    reservation_fees =db.Column(Float ,nullable=False)

    def __init__(self, reserve_id, reservation_fees):
        self.reserve_id =  reserve_id
        self.reservation_fees = reservation_fees

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            "id":self.id,
            "reserve_id":self.reserve_id,
            "reservation_fees":self.reservation_fees

        }
