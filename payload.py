import sys
import sqlite3
import os

IP = '127.0.0.1'


def download(id):
    print("Download Reached")
    conn = sqlite3.connect('admin.db')
    c = conn.cursor()
    c.execute('select payload from Tripwires where id='+str(id))
    payloads = c.execute('select payload from Tripwires where id='+str(id))
    #print(c.fetchone()[0])
    payload = ""
    for row in payloads:
        print("roooooo"+row[0])
        payload = row[0]
    print("payy" + payload)
    if payload.strip() == "robots.txt":
        print("robotsss...============================")
        os.system ("echo 'User-agent: *' > payloads/"+id+".txt")
        d = conn.cursor()
        d.execute('select tw_id from Tripwires where id='+id)
        tw_id = d.fetchone()[0]
        os.system ("echo 'Disallow: /"+tw_id+"' >> payloads/"+id+".txt ")
    else:
        print("no match")

    