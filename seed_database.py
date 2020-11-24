"""Script to seed database"""

import os #module from Python's library, code related to working with your computer's operating system
import json
from random import choice, randint
from datetime import datetime



import crud
import model
import server

os.system('dropdb rooms')
os.system('createdb rooms')

model.connect_to_db(server.app)
model.db.create_all()

# Create rooms, store them in list so we can use them
# to create fake posts, likes and comments later
rooms_in_db = []
rooms = ["living room", "bedroom", "kitchen", "patio", "home office"]
for room_name in rooms:
    db_room = crud.create_room(room_name)    
    rooms_in_db.append(db_room)

#Create 10 users
for n in range(10):
    user_name = f'user{n}'
    email = f'user{n}@test.com'  #unique email
    password = f'test{n}'

    user = crud.create_user(user_name, email, password)

    