# Argus_project
### scripts: ###
* db_init.py
  * This script connects to the Mysql database container and creates 
  database- github_scrape. Inside the db, the script creates table- selenium.
  The script changes the db to 'utf8mb4' in order to deal with Chinese and other languages.
  The script will run after the Scraper and db container will be created.
* scraper.py
  * This script use selenium package in order to get information from github.
  It searches on github search field- the world 'selenium' and check the validation
  of the result's links. After that, it uses get request in order to retrive information
   about each result. in the end, it will connect to github_scrape database and insert every
  result as new line in selenium table. The scripts movve between 5 first pages of the search result.
* view_db.py
  * This script prints the selenium table data from github_scrape database.
* find_ip.bat
  * This bat script check the host's ip addres and write it to a file- host_ip.txt
     in order to deliver it to scraper container
   


### Docker images ###
* db- mysql server
* scraper- ubuntu with pytohn

## Instructions ##
- [ ] download or clone the project's repository in to new directory in your computer
- [ ] open CMD/PowerShell/Terminal from the project directory 'Argus_project'
- [ ] run find_ip.bat- if you are using linux you should change /scraper/host_ip.txt ip to your ip
  - [ ] in the terminl write ifconfig, the ipV4 will be the addres you need to save in the host_ip.txt file
- [ ] Docker containers innit- write in the shell 'docker-compose up -d', it might take some time to download all relevant files.
- [ ] Connect to scraper container- write in the shell 'docker exec -it scraper /bin/bash'
- [ ] write in the new bash shell cd /Scraper
- [ ] Database innit- write in the shell 'python3 db_innit.py'
- [ ] Scraper- write in the shell 'python3 scraper.py' in order to start scraping
- [ ] If you want to see the database content write in the shell python3 view_db.py
