import mysql.connector
from datetime import date
import helper

con = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='arumstay')

def is_user(mail,password):
    user = []
    c = con.cursor()
    c.execute("SELECT * FROM client WHERE email='"+mail+"' AND password='"+password+"'")
    for row in c:
        user = {
            'login': 'on',
            'user_id': str(row[0]),
            'user_name':row[1]+" "+row[2],
            'user_email': row[4],
            'user_roles': row[5]
        }
    return user


def create_user(user):
    c = con.cursor()
    record = [user['fname'], user['lname'], user['pass'], user['email'],'user']
    c.execute("insert into client(first_name, last_name, password, email, roles) values(%s,%s,%s,%s,%s)", record)
    con.commit()

def check_user(mail):
    user = []
    c = con.cursor()
    c.execute("SELECT * FROM client WHERE email='"+mail+"'")
    for row in c:
        user = {
            'isset': 'true',
        }
    return user

def get_all_users():
    users = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM client")
    for row in c:
        user = {
            'id': str(row[0]),
            'first_name': row[1],
            'last_name': row[2],
            'email': row[4],
            'role': row[5],
        }
        users.append(user)
    return users

def get_all_rooms():
    rooms = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM room")
    for row in c:
        room = {
            'id': str(row[0]),
            'title': row[1],
            'amenities' : row[2],
            'price' : row[3],
            'kapasitas' : str(row[4])
        }
        data = room.copy()
        data.update(get_room_by_id(str(row[2])))
        rooms.append(data)
    return rooms


def add_room(room):
    c = con.cursor()
    record = [room['title'], room['amenities'], room['price'], room['kapasitas']]
    c.execute("insert into room(title, amenities, price, kapasitas) values(%s,%s,%s,%s)", record)
    con.commit()

def admin_home_static():
    user = totalUser()
    room = totalHotel()
    reservation = totalReservation()
    total = {
        'user': user['total'],
        'hotel': room['total'],
        'reservation': reservation['total'],

    }
    return total




def get_all_reservation():
    reservations = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM reservation r LEFT JOIN room rm ON r.id=rm.id LEFT JOIN client c ON c.id=r.name")
    for row in c:
        reservation = {
            'id': str(row[0]),
            # 'name': row[10],
            'type': row[9],
            'client': row[14]+" "+row[15],
            'price':row[11],
            'checkin' : row[5],
            'checkout' : row[6],
            'status':row[4]

        }
        reservations.append(reservation)
    return reservations

def get_rooms(value, kapasitas="0"):
    title = get_type_room(value)
    rooms = []
    c = con.cursor(buffered=True)
    if (kapasitas == "0"):
        c.execute("SELECT * FROM room WHERE id='"+title+"'")
    else:
        c.execute("SELECT * FROM room WHERE id='"+str(title)+"' AND kapasitas='"+str(kapasitas)+"'")
    for row in c:
        hotel = {
            'id': str(row[0]),
            'title': row[1],
            'amenities' : row[2],
            'price' : row[3],
            'kapasitas' : str(row[4]),
        }
        rooms.append(hotel)
    return rooms

def get_type_room(value):
    room = []
    c = con.cursor()
    c.execute("SELECT * FROM room WHERE title='"+value+"'")
    for row in c:
        room = str(row[0])
    return room

def get_basket(basket):
    room = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM room WHERE id='"+basket['room_id']+"'")
    for row in c:
        room = {
            'basket': 'on',
            'h_id': str(row[0]),
            'h_title': row[1],
            'h_amenities' : row[2],
            'h_price' : row[3]
            # 'h_img': row[6]
        }
    data = room.copy()
    data.update(get_room_by_id(basket['room_id']))
    return data

def get_room_by_id(value):
    room = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM room WHERE id='"+value+"'")
    for row in c:
        room = {
            'r_id':str(row[0]),
            'r_title': row[1],
            'r_amenities': row[2],
            'r_price':row[3],
            'r_kapasitas':str(row[4])
        }
    return room

def get_reservation_by_user(data):
    reservations = []
    c = con.cursor()
    c.execute("SELECT * FROM reservation r LEFT JOIN room rm ON r.id=rm.id WHERE r.name='"+data+"'")
    for row in c:
        reservation = {
            'id': str(row[0]),
            'name': row[9],
            'price': row[11],
            'date': row[7]
        }
        reservations.append(reservation)
    return reservations

def totalUser():
    user = []
    c = con.cursor(buffered=True)
    c.execute("SELECT COUNT(*) FROM client")
    for row in c:
        user = {
            'total': str(row[0]),
        }
    return user

def totalHotel():
    hotel = []
    c = con.cursor(buffered=True)
    c.execute("SELECT COUNT(*) FROM room")
    for row in c:
        hotel = {
            'total': str(row[0]),
        }
    return hotel

def create_reservation(data):
    c = con.cursor(buffered=True)
    record = [data['id'],data['client_id'], data['room_id'], data['price'],data['status'],data['checkin'], data['checkout'], date.today()]
    c.execute("insert into reservation(id, name, title, price, status, check_in_date, check_out_date, created_at) values(%s,%s,%s,%s,%s,%s,%s,%s)", record)
    con.commit()


def totalReservation():
    result = []
    c = con.cursor(buffered=True)
    c.execute("SELECT COUNT(*) FROM reservation")
    for row in c:
        result = {
            'total': str(row[0]),
        }
    return result

# def update_reservation(param):
#     c = con.cursor(buffered=True)
#     record = [data['status']]
#     c.execute("UPDATE reservation SET status=%s WHERE id=%s", record)
#     con.commit()
    

def delete_room(param):
    c = con.cursor()
    c.execute("Delete from room where id ='"+param+"'")
    con.commit()

def delete_user(param):
    c = con.cursor()
    c.execute("Delete from client where id ='"+param+"'")
    con.commit()

def delete_reservation(param):
    c = con.cursor()
    c.execute("Delete from reservation where id ='"+param+"'")
    con.commit()