# Build REST APIs with Python

## Introduction
Providing REST API service 

## Prerequisites

mysql.connector

falcon

falcon_cors

gunicorn


## Installation

* Install MySQL Connector
```
  $ cd ~/tools
  $ wget https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-8.0.20.tar.gz
  $ tar xzf mysql-connector-python-8.0.20.tar.gz
  $ cd ~/tools/mysql-connector-python-8.0.20
  $ sudo python3 setup.py install
```

* Install Falcon,

  Refer to 
  
  https://falconframework.org/

  https://github.com/lwcolton/falcon-cors

```
  $ mkdir ~/tools/falcon && cd ~/tools/falcon
  $ pip3 download cython falcon falcon-cors 
  $ export LC_ALL="en_US.UTF-8"
  $ export LC_CTYPE="en_US.UTF-8"
  $ sudo dpkg-reconfigure locales
  $ sudo pip3 install --upgrade --no-index --find-links ~/tools/falcon cython falcon falcon-cors
```

* Install gunicorn, refer to http://gunicorn.org
```
  $ mkdir ~/tools/gunicorn && cd ~/tools/gunicorn
  $ pip3 download gunicorn
  $ sudo pip3 install --no-index --find-links ~/tools/gunicorn gunicorn
```

## Run for debugging and testing
```
$ sudo gunicorn -b 127.0.0.1:8000 app:api
```

## API List

View in Postman: import the file *.postman_collection.json with Postman


[Meter](#Meter) 


### Meter
* GET Meter by ID

```bash
$ curl -i -X GET http://BASE_URL/meters/{id}
```
Result

| Name          | Data Type | Description                               |
|---------------|-----------|-------------------------------------------|
| id            | integer   | Meter ID                                  |
| name          | string    | Meter name                                |
| uuid          | string    | Meter UUID                                |
| description   | string    | Meter description                         |

* GET All Meters
```bash
$ curl -i -X GET http://BASE_URL/meters
```
* DELETE a Meter by ID
```bash
$ curl -i -X DELETE http://BASE_URL/meters/{id}
```
* POST Create a Meter
```bash
$ curl -i -H "Content-Type: application/json" -X POST -d '{"data":{"name":"PM20", "description":"空调用电"}}' http://BASE_URL/meters
```
* PUT Update a Meter
```bash
$ curl -i -H "Content-Type: application/json" -X PUT -d '{"data":{"name":"PM20", "description":"空调用电"}}' http://BASE_URL/meters/{id}
```
