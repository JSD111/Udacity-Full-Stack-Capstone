# Udacity Full Stack - Capstone Project

## Casting Agency Project

## Motivation

This project is the capstone project for Udacity Full Stack Web Developer Nanondegree.

This project covers all the learnt concepts which includes: SQL and data modeling for the web, API development and documentation, identity and access management and deployment.

No frontend is developed for this app.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/starter` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

### Setting up

#### Database Setup

```bash
createdb capstone
```

#### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `delete:actors`
    - `delete:movies`
    - `get:actors`
    - `get:movies`
    - `patch:actors`
    - `patch:movies`
    - `post:actors`
    - `post:movies`
6. Create new roles for:
    - Casting Assistant
        - Can view actors and movies
    - Casting Director
        - All permissions a Casting Assistant has and
        - Add or delete an actor from the database
        - Modify actors or movies
    - Executive Producer
        - All permissions a Casting Director has and
        - Add or delete a movie from the database
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users and assign each role to a user.
    - Sign into each account and make note of the JWT.

#### Configuration file

You need to update all variables found in setup.sh

### Running the project

#### Start the project locally

From within the `starter` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source ./setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
#### Running tests (Unittests)

From within the `starter` directory first ensure you are working using your created virtual environment.

To run the tests, execute:

```bash
source ./setup.sh
dropdb capstone_test
createdb capstone_test
python test_app.py
```

If you choose to run all tests, it should give this response if everything went fine:

```
----------------------------------------------------------------------
Ran 21 tests in 9.576s

OK
```

### API Reference
- Localhost on http://127.0.0.1:5000/

### Endpoints

#### GET /movies
* General: Returns a list of movies and success value
* Requiered Role: Casting Assistant, Casting Director, Executive Producer
* Requested Argument : None
* Response:
```
{
    "movies": [
        {
            "id": 2,
            "release_date": "Tue, 03 Nov 2009 00:00:00 GMT",
            "title": "AVATAR"
        },
        {
            "id": 1,
            "release_date": "Mon, 22 Feb 2010 00:00:00 GMT",
            "title": "JAWS"
        }
    ],
    "success": true
}
```

#### GET /actors
* General: Returns a list of actors and success value
* Requiered Role: Casting Assistant, Casting Director, Executive Producer
* Requested Argument : None
* Response:
```
{
    {
    "actors": [
        {
            "age": 66,
            "gender": "Male",
            "id": 1,
            "name": "Tom Hanks"
        },
        {
            "age": 70,
            "gender": "Female",
            "id": 2,
            "name": "Meryl Streep"
        }
    ],
    "success": true
}
  
}
```

#### DELETE /movies/<int:id>
* General: Deletes a movie by id and returns success value and id of deleted movie
* Requiered Role: Executive Producer
* Requested Argument : None
* Response:
```
{
    "deleted_movie_id": 2,
    "success": true
}
```

#### DELETE /actors/<int:id>
* General: Deletes an actor by id and returns success value and id of deleted actor
* Requiered Role: Executive Producer or Casting Director
* Requested Argument : None
* Response:
```
{
    "deleted_actor_id": 2,
    "success": true
}
```

#### POST /movies
* General: Creates a new movie with the given parameters and returns success value and id of created movie
* Requiered Role: Executive Producer
* Requested Argument : title, release_date
* Response:
```
{
    "created_movie_id": 6,
    "success": true
}
```

#### POST /actors
* General: Creates a new actor with the given parameters and returns success value and id of created actor
* Requiered Role: Executive Producer or Casting Director
* Requested Argument : name, age, gender
* Response:
```
{
    "created_actor_id": 2,
    "success": true
}
```

#### PATCH /movies/<int:id>
* General: Updates an existing movie with given parameters and returns success value and the movie after updated
* Requiered Role: Executive Producer or Casting Director
* Requested Argument : title, release_date
* Response: after updating release_date
```
{
    "movie": [
        {
            "id": 1,
            "release_date": "Fri, 20 Jun 1975 00:00:00 GMT",
            "title": "JAWS"
        }
    ],
    "success": true
}
```

#### PATCH /actors/<int:id>
* General: Updates an existing actor with given parameters and returns success value and the actor after updated
* Requiered Role: Executive Producer or Casting Director
* Requested Argument : name, age, gender
* Response: after updating age
```
{
    "actor": [
        {
            "age": 64,
            "gender": "Male",
            "id": 1,
            "name": "Tom Hanks"
        }
    ],
    "success": true
}
```

### Deployment
This app is hosted on heroku: https://jsaldossary.herokuapp.com






