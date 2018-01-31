# NextBigThing
Python Django Restful Api.

## Concept

Sqlite DB is used for storing data with the help of Django ORM. Django Rest Framework is used for CRUD operations.
No major Frontend Framework used due to shortage of time just basic jquery. address_collector.js is reponsible for doing all ajax requests to Rest API.

Functional tests are added for testing all the endpoints.

## Development Environment

At the bare minimum you'll need the following for your development environment:

1. [Python3](http://www.python.org/)
2. [Sqlite](https://sqlite.org)

### Local Setup

The following assumes you have all of the recommended tools listed above installed.

#### 1. Clone the project:

    $ git clone git@github.com:syedwaseemjan/NextBigThing.git
    $ cd NextBigThing

#### 2. Create and initialize virtualenv for the project:

    $ mkdir nbt_virtualenv
    $ virtualenv nbt_virtualenv --python=python3
    $ source nbt_virtualenv/bin/activate
    $ pip install -r requirements.txt

#### 3. Setup the Sqlite DB (Add default admin user):

    $ python manage.py makemigrations
    $ python manage.py migrate

#### 4. Run tests:
    
    $ python manage.py test

#### 5. Run the server:

    $ python manage runserver

#### 6. Load the system in browser:

    Visit http://127.0.0.1:8000

## Fusion Table

    https://fusiontables.google.com/data?docid=1wHekeIi0hlM6E2PcsaVzBEx5BpY3JyThL554ZKGz#rows:id=1

## API Endpoints
----

### Add Address
  Adds address information to DB and fusion table.

* **URL**

  /api/v1/addresses/

* **Method:**

  `POST`

* **Data Params**

    {
        "address": "220KV Grid Station NTDCL Nishatabad Faisalabad, Nishatabad Bridge, Faisalabad, Pakistan",
        "latitude": "31.449899868379656",
        "longitude": "73.1195068359375"
    }

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** `{
        "address": "220KV Grid Station NTDCL Nishatabad Faisalabad, Nishatabad Bridge, Faisalabad, Pakistan",
        "latitude": "31.449899868379656",
        "longitude": "73.1195068359375"
    }`
 
* **Error Response:**

  * **Code:** 400 BAD Request <br />

  OR

  * **Code:** 403 Forbidden <br />
    **Content:** `NBT does not have write permissions to the provided table. Please add your service email address to fusion table access list.`

### Get All Addresses
  Returns json data for all addresses.

* **URL**

  /api/v1/addresses/

* **Method:**

  `GET`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{
        "address": "220KV Grid Station NTDCL Nishatabad Faisalabad, Nishatabad Bridge, Faisalabad, Pakistan",
        "latitude": "31.449899868379656",
        "longitude": "73.1195068359375"
    }]`

### Delete All Addresses
  Deletes all addresses inside DB and Fusion Table.

* **URL**

  /api/v1/addresses/

* **Method:**

  `DELETE`

* **Success Response:**

  * **Code:** 205 <br />
    **Content:** `[]`