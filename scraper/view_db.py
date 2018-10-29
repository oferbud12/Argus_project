import mysql.connector

with open('host_ip.txt', 'r') as ip_file:
	HOST = ip_file.read()
USER = 'root'
PASSWD = '123'
DATABASE = 'github_scrape'

connection = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE) #connects to github_scrape database
cursor = connection.cursor()

cursor.execute('SELECT * FROM selenium')

for row in cursor:
	row = [x if x == None else x.encode('ascii', 'ignore').decode('ascii') for x in row ]
	print(row)