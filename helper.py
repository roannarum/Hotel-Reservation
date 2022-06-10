from flask import *
import connection as db
import hashlib, enum

def is_user(mail,password):
    user = db.is_user(mail, md5hasher(password))
    session_set(user)

def create_user(request):
    message = []
    user = {
        'fname':request.form['f_name'],
        'lname':request.form['l_name'],
        'email':request.form['e_mail'],
        'pass':md5hasher(request.form['f_pass'])
   }
    user_isset = db.check_user(user['email'])
    if('isset' in user_isset):
        message = {'type':'error','message':'A user has already been defined with this e-mail address.'}
    else:
        db.create_user(user)
        message = {'type':'success','message':'User successfully created.'}
    return message

def find_reservation(request):
    date = {
        'checkin':request.form['checkin'],
        'checkout':request.form['checkout']

    }
    session_set(date)
    return db.get_rooms(request.form['room'])

def session_set(array):
    for key in array:
        session[key] = array[key]

def session_get(key):
    if key in session:
        return session[key]
    else:
        return False

def session_unset(array):
    for key in array:
        if key in session:
            session.pop(key)

def session_clear():
    session.clear()


def add_to_basket(request):
    basket = {
        'room_id' : request.args.get("room"),
        'client_id': session_get('user_id'),
        'checkin': session_get('checkin'),
        'checkout' :session_get('checkout')
    }
    data = db.get_basket(basket)
    session_set(data)


def add_room(request):
    room = {
        'title':request.form['name'],
        'amenities':request.form['amenities'],
        'price':request.form['price'],
        'kapasitas':request.form['kapasitas']
    }
    db.add_room(room)


def create_reservation():
    reservartion = {
        'id' : session_get('h_id'),
        'client_id' : session_get('user_id'),
        'room_id' : session_get('r_id'),
        'price' : session_get('price'),
        'status' : request.args.get("room"),
        'checkin' : session_get('checkin'),
        'checkout' : session_get('checkout')
    }
    db.create_reservation(reservartion)

def delete_room(request):
    room_id = request.args.get('id')
    db.delete_room(room_id)


def delete_user(request):
    hotel_id = request.args.get('id')
    db.delete_user(hotel_id)


# def get_update_reservation(request):
#     reservation = {
#         'status': request.form['status']
#     }
#     session_set(reservation)


# def update_reservation(request):
#     reservation = {
#         'status' : session_get('status')
#     }
#     db.update_reservation(reservation)

def delete_reservation(request):
    hotel_id = request.args.get('id')
    db.delete_reservation(hotel_id)


def md5hasher(data):
    md5hash = hashlib.md5()
    md5hash.update(data.encode('utf-8'))
    return str(md5hash.hexdigest())