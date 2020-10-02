# Sensat Backend Challenge

### Candidate
Maurice Zard: mauricezard@yahoo.com  

### Interviewer
Paddy Lambros: paddy.lambros@sensat.co.uk

### Libraries Used
* pymysql
* flask

### Assumptions
I've made the following assumptions:
* When searching between times, results are greater than the start datetime and less than or equal to the end datetime.
i.e. (from_time, to_time]
* The initial configuration of the database by default is the configuration provided in the brief. Any changes need to 
be made via the HTTP API by uploading a new .yaml file.
* The results returned from a search do not need to be displayed (many results would look messy), but saved statically 
for download by the user. 
* The brief says "return them as a JSON documents" - this is ambiguous as to whether multiple jsons should be returned, 
one for each reading, or multiple results should be returned in a single json. It has been assumed that a single json 
should be returned containing all the results of the latest query, because it seems a lot neater.
* Previous query results are not saved, only the most recent is saved and will be returned on triggering a download.
 

### How to run in Docker

#### Steps to build the image and run the container
1. Make sure your terminal is pointing to `/sensat_backend_challenge`, where the `Dockerfile` is located.

2. Run the following command to build the image:  
`docker build -t sensat_backend_challenge .` 

    (OPTIONAL) Check and see if the images have been built by using the following command:  
    `docker images`

    If all is correct you should see the following two images:
    * **sensat_backend_challenge**
    * **tiangolo/uwsgi-nginx-flask**

3. Run the container execute the following command:  
`docker run -p 5000:5000 -d -t --name sensat_backend_challenge.container sensat_backend_challenge`. 

    This should now run the container.  
    
    (OPTIONAL) To see if it is running execute the following command:  
    `docker container ls`  
    You should now see your container present in the list.
4. Visit [`http://localhost:5000/`](http://localhost:5000/) to see the HTML API homepage with instructions on how to use it.
