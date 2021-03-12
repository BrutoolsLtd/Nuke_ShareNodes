import random
import pymongo

CLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
DB = CLIENT['ShareNodesDB']
USER_COLLECTION = DB['users']

USER_COLLECTION.drop()

import string
list_of_users = []

with open('users.txt') as userFile:
    for line in userFile:
        line_stripped = line.rstrip()
        new_name = ''.join(char for char in line_stripped if char in string.printable)
        # new_name.rstrip()
        list_of_users.append(new_name.rstrip())

for name in list_of_users:
    doc = dict()
    doc['name'] = name
    doc['login'] = name[0].lower() + name.split(' ')[-1].lower()
    doc['email'] = '{}@brutools.com'.format(name.lower().replace(' ', '.'))
    doc['age'] = random.randint(18, 60)
    USER_COLLECTION.save(doc)

