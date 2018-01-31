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

## Fusion Table:

https://fusiontables.google.com/data?docid=1wHekeIi0hlM6E2PcsaVzBEx5BpY3JyThL554ZKGz#rows:id=1