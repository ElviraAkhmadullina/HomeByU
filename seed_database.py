"""Script to seed database"""

import os #module from Python's library, code related to working with your computer's operating system
import json
# from random import choise, randint
from datetime import datetime



import crud
import model
import server

os.system('dropdb rooms')
os.system('createdb rooms')

model.connect_to_db(server.app)
model.db.create_all()

# Load data from data/rooms.json file
with open('data/rooms.json') as f:
    room_data = json.loads(f.read())

# Create rooms, store them in list so we can use them
# to create fake posts, likes and comments later

rooms_in_db = []
for room in room_data:
    room_name = room['room_name']

    db_room = crud.create_room(room_name)    

    rooms_in_db.append(db_room)

#Create 10 users
for n in range(10):
    user_name = 'user'
    email = f'user{n}@test.com'  #unique email
    password = 'test'

    user = crud.create_user(user_name, email, password)

    