 
import sys
import sqlite3


#########

conn = sqlite3.connect('admin.db')
c = conn.cursor()

c.execute('select * from Person where tw_id in (select tw_id from logs)')
table1 = c.execute('select * from Person where tw_id in (select tw_id from logs)')

b = conn.cursor()

table2 = b.execute('select * from logs where tw_id in (select tw_id from Person)')

cur = conn.cursor()

check = conn.cursor()
ifexist = check.execute('select tw_id from triggered where tw_id in (select tw_id from Person)')

output = check.fetchall()


# https://stackoverflow.com/questions/10937334/python-sqlite-get-column-values-as-a-list-tuple-from-rows-where-other-columns-h
canary = False
#for x in ifexist: 
#    canary = True
if canary == False:
    for i in table1:
        for j in table2:
            name = i[1]        
            email = i[2]
            tw_id = i[3]
            remote_host = j[1]
            request_time = j[2]
            print(name)
            print(email)
            print(tw_id)
            print(remote_host)
            print(request_time)
            try:
                cur.execute('INSERT INTO triggered (name, email, tw_id, remote_host, request_time) VALUES (?, ?, ?, ?, ?)', (name, email, tw_id, remote_host, request_time))
                conn.commit()
            except:
                pass
            break
        

        #if CheckTriggered() != "":



    