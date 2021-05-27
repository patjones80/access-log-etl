#!usr/bin/python3

import sftp_paramiko
import csv
import os
import get_db_creds
import get_creds		
import sys

from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECOND = timedelta(seconds=1)

def get_access_timestamp(access_time):
    _dt = datetime.strptime(access_time, '%d/%b/%Y:%H:%M:%S')
    return (_dt - datetime(1970, 1, 1)) // SECOND

def get_access_log():
	# get_creds is an abstraction layer to the file where credentials are kept
    creds = get_creds.cred('pythonanywhere')

    # download access log from website host	
    client = sftp_paramiko.SftpClient(creds.host, creds.port, creds.user, creds.password)
    client.download('/var/log/www.atweather.org.access.log', r'{}/access_log.txt'.format(BASE_DIR))

    # parse log records
    with open(r'{}/access_log.txt'.format(BASE_DIR), 'r', newline='') as log:
        reader = csv.reader(log, delimiter=' ', quotechar='"')

        with open(r'{}/access_log_reduced.txt'.format(BASE_DIR), 'w', newline='') as reduced:
            writer = csv.writer(reduced, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in reader:
                remote_ip = row[0]
                local_time = row[3].lstrip('[')
                path = row[5].split(' ')[1].lstrip('GET ')
                status = int(row[6])
                user_agent = row[9]
                response_time = float(row[11].split('=')[1])
				
                writer.writerow([remote_ip, local_time, path, status, user_agent, response_time, get_access_timestamp(local_time)])

try:
	get_access_log()
except Exception as e:
	print('Error pulling access log: {}'.format(e))
	sys.exit()

try:
    conn = get_db_creds.db_conn('access_log_main')
    cursor = conn.cursor()
except AssertionError:
    print('Database connection timeout after multiple attempts')
    sys.exit()

cursor.execute('''CREATE TEMP TABLE tmp_table
                  ON COMMIT DROP
                  AS
                  SELECT *
                  FROM access_log
                  WITH NO DATA;''')

with open(r'{}/access_log_reduced.txt'.format(BASE_DIR), 'r') as f:
    cursor.copy_expert('''COPY tmp_table FROM STDIN WITH (DELIMITER '\t')''', f)

cursor.execute('''INSERT INTO access_log
                  SELECT *
                  FROM tmp_table
                  WHERE access_timestamp > (SELECT MAX(access_timestamp)
                                            FROM access_log);''')
conn.commit()
conn.close()
