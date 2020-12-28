import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

#---------------------------------------------------#
# Endpoints
#---------------------------------------------------#

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                                'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                                'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route("/", methods=["GET"])
    def welcome():
        return jsonify({
            "message": "WELCOME"
        })

    # Endpoint to handle GET requests for all movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):

        all_movies = Movie.query.all()
        formatted_movies = [m.format() for m in all_movies]

        return jsonify({
            'success': True,
            'movies': formatted_movies
        }), 200  

    # Endpoint to handle GET requests for all actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):

        all_actors = Actor.query.all()
        formatted_actors = [a.format() for a in all_actors]

        return jsonify({
            'success': True,
            'actors': formatted_actors
        }), 200 

    # Endpoint to DELETE a movie by id
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):

        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()
        except Exception:
            abort(400)

        return jsonify({
            'success': True, 
            'deleted_movie_id': id
        }), 200

    # Endpoint to DELETE an actor by id
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):

        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()
        except Exception:
            abort(400)

        return jsonify({
            'success': True, 
            'deleted_actor_id': id
        }), 200

    # Endpoint to POST a movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):

        body = request.get_json()

        if "title" and "release_date" not in body:
            abort(422)

        try:
            title = body.get('title', None)
            release_date  = body.get('release_date', None)
            movie = Movie(title=title, release_date=release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'created_movie_id': movie.id
            })
        except Exception:
            abort(400)

    # Endpoint to POST an actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):

        body = request.get_json()

        if "name" and "age" and "gender" not in body:
            abort(422)

        try:
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                'success': True,
                'created_actor_id': actor.id
            })
        except Exception:
            abort(400)

    # Endpoint to PATCH a movie
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):

        body = request.get_json()
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None or body is None:
            abort(404)

        try:
            title = body.get('title', None)
            release_date = body.get('release_date', None)

            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date

            movie.update()
            updated_movie = Movie.query.get(id)
        except Exception:
            abort(400)

        return jsonify({
            'success': True, 
            'movie': [updated_movie.format()]
        }), 200

    # Endpoint to PATCH an actor
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, id):

        body = request.get_json()
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None or body is None:
            abort(404)

        try:
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)

            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender

            actor.update()
            updated_actor = Actor.query.get(id)
        except Exception:
            abort(400)

        return jsonify({
            'success': True, 
            'actor': [updated_actor.format()]
        }), 200
##-----------------------------------------------
## Error Handling
##-----------------------------------------------
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(AuthError)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error["description"]
        }), error.status_code

    return app
#-------------------------------------------------------
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
