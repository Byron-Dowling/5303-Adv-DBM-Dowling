import json
import mysql.connector
import time
import random
import redis
import pymongo

jsonfile = open('data.json', 'r')
jsondata = json.load(jsonfile)

config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'database': 'testing',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

cursor = cnx.cursor(dictionary=True)

print('Mysql Insertion Testing')
for N in (50000,100000,500000,10000000):
    cursor.execute('DELETE FROM mytable')
    cnx.commit()
    start = time.time()
    for i, rows in enumerate(jsondata):
        cursor.execute('INSERT INTO mytable VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s,%s)', [rows['id'], rows['first_name'], rows['last_name'], rows['email'], rows['city'],rows['state'],rows['address'],rows['latitude'],rows['longitude'],rows['car'],rows['car_model'],rows['car_color'],rows['searchval']])
        cnx.commit()
        if i == N - 1:
            break
    end = time.time()
    print('MYSql took ', end-start, 'seconds to insert ', N)

print('Mysql Single Selection Testing')
cursor = cnx.cursor(buffered=True)
for N in (5,10,500,1000):
    start = time.time()
    for i in range(1,N + 1):
        cursor.execute('SELECT * FROM mytable WHERE id = %s', [random.randint(1, 1000)])
    end = time.time()
    print('MySql took ', end-start, ' seconds to search ', N, '--> Single select on id basis')    

print('Mysql Multi Selection Testing')
cursor = cnx.cursor(buffered=True)
for N in (5,10,500,1000):
    start = time.time()
    for i in range(1,N + 1):
        cursor.execute('SELECT * FROM mytable ')
    end = time.time()
    print('MySql took ', end-start, ' seconds to search ', N, '--> Full Select')   

print('Mysql Updation Testing')
for N in (5,10,500,1000):
    start = time.time()
    for i in range(1,N + 1):
        cursor.execute('UPDATE mytable SET city = %s WHERE id = %s', [random.randint(1, 1000), random.randint(1, 1000)])
        cnx.commit()
    end = time.time()
    print('MySql took ', end-start, ' seconds to update ', N, '--> Single Update')   

print('Mysql Deletion Testing')
for N in (5,10,500,1000):
    start = time.time()
    for i in range(1,N + 1):
        cursor.execute('DELETE FROM mytable WHERE id = %s;', [random.randint(1, 1000)])
        cnx.commit()
    end = time.time()
    print('MySql took ', end-start, ' seconds to delete ', N, '--> Single delete')   


redisdb = redis.Redis(host='localhost', port=6379, db=0)
print('redis insertion Testing')
for N in (50000,100000,500000,10000000):
    redisdb.flushall()
    start = time.time()
    for i, rows in enumerate(jsondata):
        redisdb.hset(rows['id'],  mapping={'first_name': rows['first_name'], 'last_name': rows['last_name'], 'email': rows['email'], 'city': rows['city'],'city': rows['state'],'address': rows['address'],'latitude': rows['latitude'],'longitude': rows['longitude'],'car': rows['car'],'car_model': rows['car_model'],'car_color': rows['car_color'],'searchval': rows['searchval']    })
        if i == N - 1:
            break
    end = time.time()
    print('Redis took ', end-start, ' seconds to insert ', N)

print('redis searching single Testing')
for N in (50000,100000,500000,10000000):
    start = time.time()
    for i in range(1,N + 1):
        redisdb.hgetall(random.randint(1, 1000))
    end = time.time()
    print('Redis took ', end-start, ' seconds to search ', N, ' single on id')


print('redis searching multiple Testing')
for N in (50000,100000,500000,10000000):
    start = time.time()
    keys = redisdb.keys('*')
    for i in range(1,N + 1):
        for key in keys:
            redisdb.hgetall(int(str(key)[2:-1]))
    end = time.time()
    print('Redis took ', end-start, ' seconds to search ', N, ' multisearch')

print('redis updation Testing')
for N in (50000,100000,500000,10000000):
    start = time.time()
    for i in range(1,N + 1):
        key = random.randint(1, 1000)
        row = redisdb.hgetall(key)
        row[str.encode('city')] = str.encode(str(random.randint(1, 1000)))
        redisdb.hset(key,  mapping= row)      
    end = time.time()

    print('Redis took ', end-start, ' seconds to update ', N, ' --> updation')

print('redis deleition Testing')
for N in (50000,100000,500000,10000000):
    start = time.time()
    for i in range(1,N + 1):
        redisdb.delete(i)
    end = time.time()
    print('Redis took ', end-start, ' seconds to delete ', N, ' --> delete')

mongocon = pymongo.MongoClient('mongodb://localhost:27017')
mogodb = mongocon['testing']
tablemongo = mogodb['mytable']

print('mongo insertion Testing')
for N in (50000,100000,500000,10000000):
    tablemongo.drop()
    start = time.time()
    tablemongo.insert_many(jsondata[0:N])
    end = time.time()
    print('Mongo took ', end-start, ' seconds to insert ', N,'--> inserting')


print('mongo insertion Testing')
for N in (50000,100000,500000,10000000):
    tablemongo.drop()
    start = time.time()
    tablemongo.insert_many(jsondata[0:N])
    end = time.time()
    print('Mongo took ', end-start, ' seconds to insert ', N,'--> inserting')


print('mongo search single Testing')
for N in (50000,100000,500000,10000000):
    start = time.time()
    for i in range(1,N + 1):
        tablemongo.find({'id': random.randint(1, 1000)},{'_id': 0})
    end = time.time()

    print('MongoDB took ', end-start, ' seconds to search ', N, ' --> single search on id')


print('mongo search multi Testing')
for N in (50000,100000,500000,10000000):
    start = time.time()
    for i in range(1,N + 1):
        tablemongo.find({},{'_id': 0})
    end = time.time()
    print('MongoDB took ', end-start, ' seconds to search ', N, ' --> multisearch full ')


print('mongo updation Testing')
for N in (50000,100000,500000,10000000):
    start = time.time()
    for i in range(1,N + 1):
        tablemongo.update_one({'id': random.randint(1, 1000)}, {'$set':{'city':random.randint(1, 1000)}})
    end = time.time()
    print('MongoDB took ', end-start, ' seconds to update ', N, ' --> updation')

print('mongo deletion Testing')
for N in (50000,100000,500000,10000000):
    start = time.time()
    for i in range(1,N + 1):
        tablemongo.delete_one({'id': i})
    end = time.time()
    print('MongoDB took ', end-start, ' seconds to delete ', N, ' --> delete')
