#!/usr/bin/env python3
 
import sys
import sqlite3
from apachelogs import LogParser
import re
from pygtail import Pygtail


conn = sqlite3.connect('admin.db')
cur = conn.cursor()
 
cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    remote_host TEXT,
                    request_time TEXT,
                    request_line TEXT,
                    final_status TEXT,
                    bytes_sent INTEGER,
                    tw_id TEXT
                )
            """)
 
# Pattern below is from the LogFormat setting in apache2.conf/httpd.conf file
# You will likely need to change this value to the pattern your system uses
parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
 
log_file = '/var/log/apache2/access.log'
 
with open(log_file) as f:
    for line in Pygtail(log_file):
    #for line in f:
 
        entry = parser.parse(line)
       
        # Line below adds minimalistic date stamp column 
        # in format that sqlite3 date functions can work with
        #d['date'] = d['time_received_datetimeobj'].date().isoformat()
        
        match = re.search("GET /(.*) HTTP/1.1", entry.request_line)
        tw_id_temp = match.group(1)
        print(tw_id_temp)
        cur.execute("""
                        INSERT INTO logs ( remote_host, request_time, request_line, final_status, bytes_sent, tw_id)
                                  VALUES (?, ?, ?, ?, ?, ?)
                        """, (entry.remote_host, entry.request_time, entry.request_line, entry.final_status, entry.bytes_sent, tw_id_temp))
        
 
cur.close()
 
conn.commit();
conn.close();