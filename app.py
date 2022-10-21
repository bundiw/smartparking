import datetime
import functools
import json
import sys
import requests
from time import gmtime, strftime, strptime
from flask import Flask, request,redirect, url_for, abort, jsonify
from flask_cors import CORS
import bcrypt

from models import setup_db, Lot, Reservation,Payment, Place, County, User,db


app = Flask(__name__)
setup_db(app)

"""
@DONE: Set up CORS. Allow '*' for origins
"""
CORS(app)
"""
@DONE: Use the after_request decorator to set Access-Control-Allow
"""
@app.after_request
def after_request(response):
    
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response

"""
User APIs
"""
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/api/login', methods=['POST'])
def login():
    
    username = request.form.get('email')
    password = request.form.get('password')
    # get the first item from the matching list of objects
    user = User.query.filter(User.email == username).first()
    if user is None:
        abort(404)
    hash = bytes.fromhex(user.password[2:]) 
    
    match = bcrypt.checkpw(password.encode('utf-8'),hash)
    
    
    if user is None or not match:
        
        abort(404)
    return {
        "data":user.format(),
        "success":True,
        "message":"User fetched success"

    }
    
@app.route('/api/users')
def registered_users():

    # get the first item from the matching list of objects
    users = User.query.order_by(User.id).all()
    
    if not users:
        
        abort(404)
    users = [user.format() for user in users]
    return {
        "data":users,
        "success":True,
        "message":"Users fetched success"
    }
    
@app.route('/api/users/<int:user_id>')
def edit_user(user_id):

    # get the first item from the matching list of objects
    user = User.query.filter_by(id=user_id).first()
    
    if  user is None:
        
        abort(404)
    
    return {
        "data":user.format(),
        "success":True,
        "message":"User deleted success"
    }
@app.route('/api/users/<int:user_id>/delete',methods=["DELETE"])
def delete_user(user_id):

    # get the first item from the matching list of objects
    user = User.query.filter_by(id=user_id).first()
    
    if  user is None:
        
        abort(404)
    user.delete()
    
    return {
        "data":user.format(),
        "success":True,
        "message":"User deleted success"
    }

@app.route('/api/users/create',methods=['POST'])
def register():
    
    
    if(not ('full_name' in request.form and 
        'phone_number' in request.form and 
        'email' in request.form and 
        'password' in request.form)
    ): 
        abort(400)

    full_name  = request.form.get('full_name')
    phone_number= request.form.get('phone_number')
    email =  request.form.get('email')   
    password =request.form.get('password')
    # encrypt password with bcrypt
    
    byte_pwd = password.encode('utf-8')
    my_salt= bcrypt.gensalt()
    hash =bcrypt.hashpw(byte_pwd,my_salt)
    
    user =User(full_name, phone_number, email, hash)
    try:
        user.insert()
    except:
        # print(sys.exc_info())
        abort(422)


    return{
        "success":True,
        "data":user.format(),
        "message":"User added success"
    }
    
@app.route('/api/users/<int:user_id>/edit',methods=['PATCH'])
def update_user(user_id):
    user_data = User.query.get(user_id)
    # print(request.form)
    if user_data is None:
        abort(404)
    
    
    if(not ('full_name' in request.form and 
        'phone_number' in request.form and 
        'email' in request.form and 
        'password' in request.form)
    ): 
        abort(400)

    full_name  = request.form.get('full_name')
    phone_number= request.form.get('phone_number')
    email =  request.form.get('email')   
    password =request.form.get('password')
    # encrypt password with bcrypt
    
    byte_pwd = password.encode('utf-8')
    my_salt= bcrypt.gensalt()
    hash =bcrypt.hashpw(byte_pwd,my_salt)
    
    user_data.full_name =  full_name
    user_data.phone_number = phone_number
    user_data.email = email 
    user_data.password = hash
    try:
        user_data.update()
    except:
        # print(sys.exc_info())
        abort(422)

    return{
        "success":True,
        "data":user_data.format(),
        "message":"User updated success"
    }

"""
Counties APIs
"""
# display all counties that are already added by admin (GET)
@app.route('/api/counties')
def show_counties():
    # get all the counties from the database and display them to the screen
    counties =County.query.order_by(County.county_name).all()
    
    #    if the list is empty alert not found success handler
    if not counties:
        abort(404)

    # convert the county list item to json objects
    counties = [county.format() for county in counties]
    return {
        "success":True,
        "data":counties,
        "message":"Counties fetched success"
    }
    
# add new county to the county list (POST) 
@app.route('/api/counties/create',methods=['POST'])
def add_counties():
            
    if not "county_name" in request.form:

        abort(400)
    county_data = request.form.get("county_name")
    # get all the counties from the database and display them to the screen
    county = County(county_data)
    try:
        county.insert()
    except:
        abort(422)
    

    # convert the county list item to json objects
    
    return {
        "success":True,
        "data":county.format(),
        "message":"County added success"
    }

@app.route('/api/counties/<int:county_id>/delete',methods=['DELETE'])
def delete_county(county_id):
    county = County.query.get(county_id)
    if not county:
        abort(404)
    county.delete()

    return {
        "success":True,
        "data":county.format(),
        "message":"County deleted success"
    }

@app.route('/api/counties/<int:county_id>/edit',methods=['PATCH'])
def update_county(county_id):
    county = County.query.get(county_id)
    
    if "county_name" not in request.form:
        abort(400)
    if county is  None:
        abort(400)
    county.county_name=request.form.get('county_name')
    county.update()
    return {
        "success":True,
        "data":county.format(),
        "message":"County updated success"
    }

@app.route('/api/counties/<int:county_id>')
def single_county(county_id):
    county = County.query.get(county_id)
    if not county:
        abort(404)

    return {
        "success":True,
        "data":county.format(),
        "message":"County fetched success"
    }

    

"""
Place apis
"""
@app.route('/api/places')
def show_places():
    # fetch all places from the database
    places = Place.query.all()
    
    
    # if no place listed the abort 
    if not places:
        abort(404)

    places = [place.format() for place in places]

    return{
        "success":True,
        "data":places,
        "message":"Places fetched success"
    }
    
@app.route('/api/counties/<int:county_id>/places')
def show_counties_places(county_id):

    
    # fetch all places from the database
    places = Place.query.filter_by(county_id=county_id).all()
    
    
    # if no place listed the abort 
    if not places:
        abort(404)

    places = [place.format() for place in places]

    return{
        "success":True,
        "data":places,
        "message":"Places fetched success"
    }


@app.route('/api/places/create',methods=['POST'])
def add_places():
    
    # count how many places are in the database from the county and add one to increment place counter
    place_data = request.form
    
    if "place_name" not in place_data or "county_id" not in place_data:
        abort(400)

    place_name = place_data.get('place_name')
    county_id = place_data.get('county_id')
    
    place = Place(place_name,county_id)
    try:
        place.insert()
    except:
        abort(422)
    return{
        "success":True,
        "data":place.format(),
        "message":"Place added success"
        
    }
    

@app.route('/api/places/<int:place_id>')
def single_place(place_id):
    place_data = Place.query.get(place_id)
    if place_data is None:
        abort(404)
    return {
        "success":True,
        "data":place_data.format(),
        "message":"Place fetched success"
    }


@app.route('/api/places/<int:place_id>/delete', methods=['DELETE'])
def delete_place(place_id):
    place_data = Place.query.get(place_id)
    if(place_data is None):
        abort(404)
    place_data.delete()
    return{
        'success':True,
        'data':place_data.format(),
        "message":"Place deleted success"
    }

@app.route('/api/places/<int:place_id>/edit', methods=['PATCH'])
def update_place(place_id):
    place_data = Place.query.get(place_id)
    place_name =request.form.get('place_name')
    if place_data is None or 'place_name' not in request.form:
        abort(404)

    place_data.place_name = place_name
    place_data.update()
    return{
        "success":True,
        "data":place_data.format(),
        "message":"Place updated success"
    }

"""
Lot apis
"""
@app.route('/api/lots')
def show_lots():
    lots = Lot.query.all()

    if not lots:
        abort(404)
    lots = [lot.format() for lot in lots]
    return {
        "success":True,
        "data":lots,
        "message":"Lots fetched success"
    }
    
@app.route('/api/places/<int:place_id>/lots')
def show_place_lots(place_id):
    lots = Lot.query.filter_by(place_id = place_id).all()
    
    currDate = datetime.datetime.now()
    currTime = currDate.strftime("%H:%M") 
    currDate = currDate.strftime("%Y-%m-%d") 

    str_time = ''
    time_diff = 0
    
    lots_in_use_numbers = []
    for lot in lots:
        lot_id = lot.id
        
        reservations = Reservation.query.filter_by(lot_id = lot_id).order_by(Reservation.start_time.desc()).all()
        for reservation in reservations:
            if (reservation.reserve_date  + reservation.end_time) > (currDate + currTime):
                
                if currTime > reservation.start_time:
                    # time_diff_start = datetime.datetime.strptime(currTime,'%H:%M') - datetime.datetime.strptime(reservation.start_time,'%H:%M')
                    lots_in_use_numbers.append(reservation.lot_id)
                time_diff =  datetime.datetime.strptime(reservation.reserve_date+' '+ reservation.end_time,'%Y-%m-%d %H:%M') - datetime.datetime.strptime(currDate+' '+currTime,'%Y-%m-%d %H:%M')
                
                str_time = str(time_diff)
                break
        # print(time_diff," ",time_diff_start)
        if len(str_time) > 0:
                pos_of_colon = str_time.index(':')
        else:
            pos_of_colon = 0 
        
        if  pos_of_colon > 0  and  int(str_time[:pos_of_colon]) > 0 :
            # make it yellow
            
            lot.current_use = 'yellow'
            
            
        else:
            lot.current_use = 'green'
            
        lot.update()
        
        # print(lots_in_use_numbers)
        for lot_number in lots_in_use_numbers:
            lot_in_use = Lot.query.get(lot_number)
            lot_in_use.current_use ='red'
            
            lot_in_use.update()
                
                    
    if not lots:
        abort(404)
    lots = [lot.format() for lot in lots]
    return {
        "success":True,
        "data":lots,
        "message":"Lots fetched success"
    }

@app.route('/api/lots/create', methods=['POST'])
def add_lot():
    # place_id,lot_number,lot_price,current_use
    if "place_id" not in request.form  or  "lot_number" not in request.form or "lot_price" not in request.form:
        abort(400)
    lot = Lot(**request.form)
    try:

        lot.insert()
    except:
    #    print(sys.exc_info())
        abort(422)
    return{
        "success":True,
        "data":lot.format(),
        "message":"Lot added success"
    }

@app.route('/api/lots/<int:lot_id>')
def single_lot(lot_id):
    lot = Lot.query.get(lot_id)
    if lot is None:
        abort(404)
        
    return{
        "success":True,
        "data":lot.format(),
        "message":"Lot fetched Sucess"
    }

@app.route('/api/lots/<int:lot_id>/delete', methods=["DELETE"])
def delete_lot(lot_id):
    lot = Lot.query.get(lot_id)
    if lot is None:
        abort(422)
    lot.delete()
        
    return{
        "success":True,
        "data":lot.format(),
        "message":"Lot deleted success"
    }

@app.route('/api/lots/<int:lot_id>/edit', methods=["PATCH"])
def update_lot(lot_id):
    lot = Lot.query.get(lot_id)
    if lot is None:
        abort(422)
    
    if "current_use" not in request.form or "place_id" not in request.form or  "lot_price" not in request.form :
        abort(400)
    lot.place_id = request.form.get("place_id")
    lot.lot_price = request.form.get("lot_price")
    lot.current_use = request.form.get('current_use')
    try:
        lot.update()
    except:
        abort(422)
                    
    return{
        "success":True,
        "data":lot.format(),
        "message":"Lot updated success"
    }

"""
Reservations api
"""

@app.route('/api/reservations')
def show_reservation():
    reservations = Reservation.query.order_by(Reservation.reserve_date.desc(),Reservation.start_time.desc()).all()
    if not reservations:
        abort(404)
    reservations = [reservation.format() for reservation in reservations]

    return{
        "success":True,
        "data":reservations,
        "message":"Reservations fetched success",
        "match_count":len(reservations)
    }

@app.route('/api/lots/<int:lot_id>/reservations',methods=['POST'])
def show_lot_reservations(lot_id):
    
    reservations = Reservation.query.order_by(Reservation.start_time.desc()).filter(Reservation.lot_id == lot_id).all()

    start_time = request.form.get('start_time')
    reserve_date = request.form.get('reserve_date')
    if not reservations:
        abort(404)
    
    reservations = [reservation.format() for reservation in reservations if reservation.start_time <= start_time and start_time < reservation.end_time and str(reservation.reserve_date) == str(reserve_date)]
    # print(reservations)    
    return{
        "success":True,
        "data":reservations,
        "message":"Reservations fetched success"
    }
    
@app.route('/api/reservations/create', methods=['POST'])
def add_reservation():
    # lot_number,vehicle_category,reserve_date,
    # start_time,end_time,user_id
    # print(request.form)
    if "lot_id" not in request.form or "vehicle_category" not in request.form or"vehicle_plate" not in request.form or "reserve_date" not in request.form or "start_time" not in request.form or "end_time" not in request.form or "user_id" not in request.form:
        abort(400)
    # udate the lot status
    lot = Lot.query.get(request.form.get("lot_id"))
    
    currDate = datetime.datetime.now()
    currTime = currDate.strftime("%H:%M") 
    start_time =request.form.get("start_time")
    temp = None
    if start_time < currTime:
        # swap values
        temp = currTime
        currDate = start_time
        start_time =temp
    
    time_diff =  datetime.datetime.strptime(start_time,'%H:%M') - datetime.datetime.strptime(currTime,'%H:%M')

    str_time_diff = str(time_diff)
    position = str_time_diff.index(':')
    minutes = int(str_time_diff[int(position+1):-3])
    hours = int(str_time_diff[:position])
    minutes_diff = hours*60+minutes
    current_state = 'yellow'
    if minutes_diff < 60:
        current_state ='red'
    lot.current_use = current_state
    # print(request.form.get('user_id'))
    
    reservation = Reservation(**request.form)
    try:
        lot.update()
        
        reservation.insert()
    except:
        # print(sys.exc_info())
        abort(422)
        
    return {
        "success":True,
        "data":reservation.format(),
        "message":"Reservation added success"
    }



@app.route('/api/reservations/<int:reserve_id>')
def single_reservation(reserve_id):
    reservation = Reservation.query.get(reserve_id)
    if reservation is None:
        abort(404)
    return{
        "success":True,
        "data":reservation.format(),
        "message":"Reservation fetched success"
        
    }
        
        
@app.route('/api/reservations/<int:reserve_id>/edit', methods=['PATCH'])
def update_reservation(reserve_id):
    reservation = Reservation.query.get(reserve_id)
    if reservation is None:
        abort(404)
    
    # note the reserved lot id and user(client) cannot be cahnged ut the rest of the data can change
    if  "vehicle_category" not in request.form or "reserve_date" not in request.form or "start_time" not in request.form or "end_time" not in request.form :
        abort(400)
    reservation.vehicle_category =request.form.get("vehicle_category")
    reservation.vehicle_plate =request.form.get("vehicle_plate")
    reservation.reserve_date =request.form.get("reserve_date")
    reservation.start_time =request.form.get("start_time")
    reservation.end_time =request.form.get("end_time")
    # print( request.form.get("lot_id"))
    # udate the lot status
    lot = Lot.query.get(request.form.get("lot_id"))
    
    currDate = datetime.datetime.now()
    currTime = currDate.strftime("%H:%M") 
    start_time =request.form.get("start_time")
    temp = None
    if start_time < currTime:
        # swap values
        temp = currTime
        currDate = start_time
        start_time =temp
    
    time_diff =  datetime.datetime.strptime(start_time,'%H:%M') - datetime.datetime.strptime(currTime,'%H:%M')

    str_time_diff = str(time_diff)
    position = str_time_diff.index(':')
    minutes = int(str_time_diff[int(position+1):-3])
    hours = int(str_time_diff[:position])
    minutes_diff = hours*60+minutes
    current_state = 'yellow'
    if minutes_diff < 60:
        current_state ='red'
    lot.current_use = current_state
    # print(lot)
    
    reservation = Reservation(**request.form)
    try:
        lot.update()
        
        reservation.update()
    except:
        # print(sys.exc_info)
        abort(422)
    return{
        "success":True,
        "data":reservation.format(),
        "message":"Reservation updated Sucess"
    }
    

@app.route('/api/reservations/<int:reserve_id>/delete', methods=['DELETE'])
def delete_reservation(reserve_id):
    reservation =Reservation.query.get(reserve_id)
    
    if reservation is None:
        abort(404)
        
    try:
        reservation.delete()
    except:
        abort(422)
    return{
        "success":True,
        "data":reservation.format(),
        "message":"Reservation deleted success"
    }
    
"""
Payment APIs
The api allow for viewing and adding payment  only
"""
@app.route('/api/payments')
def show_payment():
    payments = Payment.query.all()
    
    if not payments:
        abort(404)
    # delete payment that have no associate reserve
    removed_pays = [payment.delete() for payment in payments if not payment.reserve_id ]
    payments = [payment.format() for payment in payments if payment.reserve_id ]
    
    return{
        "success":True,
        "data":payments,
        "message":"All payment fetched success",
        "match_count":len(payments)
    }
    

@app.route('/api/payments/create', methods=["POST"])
def add_payment():
    if "reserve_id" not in request.form or "reservation_fees" not in request.form:
        abort(400)
        
    payment = Payment(**request.form)
    try:
        payment.insert()
    except:
        abort(422)
    return{
        "success":True,
        "data":payment.format(),
        "message":"Payment added success"
    }
    
@app.route('/api/payments/<int:payment_id>/edit', methods=["PATCH"])
def edit_payment(payment_id):
    payment = Payment.query.filter_by(id=payment_id)
    if payment is None or "reserve_id" not in request.form or "reservation_fees" not in request.form:
        abort(400)
        
    payment.reserve_id = request.form.get("reserve_id")
    payment.reservation_fees = request.form.get("reservation_fees")
    try:
        payment.update()
    except:
        abort(422)
    return{
        "success":True,
        "data":payment.format(),
        "message":"Payment updated success"
    }
            
    
    
@app.route('/api/payments/<int:payment_id>/delete')
def delete_single_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if payment is None:
        abort(404)
    payment.delete()
    return{
        "success":True,
        "data":payment.format(),
        "message":"Payment deleted success"
    }
    
@app.route('/api/payments/<int:payment_id>')
def single_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if payment is None:
        abort(404)
    return{
        "success":True,
        "data":payment.format(),
        "message":"Payment fetched success"
    }
    
# the reservations and states
@app.route('/api/users/<int:user_id>/reservations/<end_date>/<stop_time>')
def show_reservation_states(user_id,end_date,stop_time):
    
    reserve_state =  request.args.get("reserve_state")
    
    place_data={}
    data = []
    reserve_count =0
    reservations =[]
    # print(len(str(reserve_state)) , len("active"))
    if reserve_state == "active":
        
        reservations = Reservation.query.filter(Reservation.user_id == user_id, (Reservation.reserve_date + Reservation.end_time) > (end_date+stop_time)).all()
        # print(reserve_state, reservation.reserve_date ,end_date, reservation.reserve_date >= end_date)
        reserve_count =len(reservations)
    else:
        reservations = Reservation.query.filter(Reservation.user_id == user_id,(Reservation.reserve_date + Reservation.end_time) <= (end_date+stop_time)).all()
        # reservations = Reservation.query.filter(func.concat(),Reservation.user_id == user_id, func.concat() Reservation.reserve_date <= end_date, Reservation.end_time <= stop_time).all()
        # [print(reserve_state, (reservation.reserve_date+reservation.end_time) , (end_date +stop_time)) for reservation in reservations]
        reserve_count =len(reservations)
    
    for reservation in reservations:
        lot = Lot.query.get(reservation.lot_id)
        payment = Payment.query.filter_by(reserve_id = reservation.id).first()
        pay = None
        if payment is None:
            pay ="Payment Due"
            reservation.delete()
            
        else:
                
            # place 
            place = Place.query.get(lot.place_id)
            place_data={'place_name': place.place_name,
            'lot_number': lot.lot_number,
            'reserved_date':reservation.reserve_date,
            'reserved_start_time':reservation.start_time,
            'reserved_stop_time':reservation.end_time,
            'reservation_fees': payment.reservation_fees 
            }
            data.append(place_data)
                
    
    return{
        "success":True,
        "message":"Reservation fetched success",
        "data":data,
        "match_count": reserve_count
    }
    
# the reservations and states
@app.route('/api/places/<int:place_id>/reservations')
def filter_reservation(place_id):
    
    reserve_start_date =  request.args.get("start_date")
    reserve_stop_date =  request.args.get("stop_date")
    print(reserve_start_date,reserve_stop_date)
    if "start_date" in request.args and "stop_date" in request.args :
        # if both filter start an end date are given
        
        reservations = db.session.query(Reservation,Lot).join(Lot).filter(Lot.place_id == place_id,Reservation.reserve_date >= reserve_start_date,Reservation.reserve_date <= reserve_stop_date).order_by(Reservation.reserve_date.desc()).all()
    
    elif "start_date" in request.args and not "stop_date" in request.args:
        reservations = db.session.query(Reservation,Lot).join(Lot).filter(Lot.place_id == place_id,Reservation.reserve_date >= reserve_start_date).order_by(Reservation.reserve_date.desc()).all()
        
        # if no end date is given
    
    elif "stop_date" in request.args and not "start_date" in request.args:
        # if stop date alone is given 
        reservations = db.session.query(Reservation,Lot).join(Lot).filter(Lot.place_id == place_id,Reservation.reserve_date <= reserve_stop_date).order_by(Reservation.reserve_date.desc()).all()
        
    else:
        
        reservations = db.session.query(Reservation,Lot).join(Lot).filter(Lot.place_id == place_id).order_by(Reservation.reserve_date.desc()).all()
        
    reservations = [ reservation.format() for reservation,lot in reservations]
       
    match_count = len(reservations)
        
    return {
        "success":True,
        "message":"Reservation fetched success",
        "data":reservations,
        "match_count": match_count
    }
    

    
@app.route('/api/payments/mpesa', methods=['POST'])
def mpesa_pay():
    # print(request.form)  
    print(request.get_json())
    # print(request.headers)
    # save the transaction
    
    return {
        "success":True,
        "Message":"Payment Success"
    }


@app.errorhandler(404)
def success_404(error):

    return jsonify({
        'success': False,
        'message': error.name,
        'data':None


    }), 404

@app.errorhandler(400)
def success_400(error):

    return jsonify({
        'success': False,
        'message': error.name,
        'data':None


    }), 400


@app.errorhandler(422)
def success_422(error):

    return jsonify({
        'success': False,
        'message': error.name,
        'data':None


    }), 422

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)


    


