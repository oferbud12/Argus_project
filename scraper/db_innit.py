#db_init.py

"""
This script connects to the Mysql database container and creates 
database- github_scrape. Inside the db, the script creates table- selenium/
The script changes the db to 'utf8mb4' in order to deal with Chinese and other languages 
The script will run after the Scraper and db container will be created.
*host_ip.txt is a fail that contains the hos ip address in order to deliver it to Scrapper script.
"""

import mysql.connector

with open('host_ip.txt', 'r') as ip_file:
	HOST = ip_file.read()
USER = 'root'
PASSWD = '123'
DATABASE = 'github_scrape'

print('-> Connecting to db'.format(HOST))
connection = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD)
cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS {} ".format(DATABASE)) #creates data base, name- github_scrape

cursor.execute("""ALTER DATABASE github_scrape CHARACTER 
	SET = utf8mb4 COLLATE = utf8mb4_unicode_ci""") #handle Chinese chars

connection = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE) #connects to github_scrape database
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS selenium (title VARCHAR(255),
		description TEXT, tags VARCHAR(255), time VARCHAR(255), language VARCHAR(255),
		rate VARCHAR(255))""") # creates table, name- selenium

connection.close() #closes script's connection to the database
print('-> github_scrape database is ready ')	
	