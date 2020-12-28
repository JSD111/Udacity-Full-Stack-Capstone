import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie

casting_assistant_auth_header = {
    "Authorization": "Bearer " + os.environ['CASTING_ASSISTANT_TOKEN']
}

casting_director_auth_header = {
    "Authorization": "Bearer " + os.environ['CASTING_DIRECTOR_TOKEN'] 
}

executive_producer_auth_header = {
    "Authorization": "Bearer " + os.environ['EXECUTIVE_PRODUCER_TOKEN']
}

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_movie = {
            "title": "New Movie",
            "release_date": "2020-11-22"
        }

        self.error_movie = {
            "title": "New Movie",
        }

        self.new_actor = {
            "name": "New Actor",
            "age": 33,
            "gender": "Male"
        }

        self.error_actor = {
            "name": "New Actor",
            "age": 22,
        }

        movie = Movie(title="FROZEN", release_date="2020-02-22")
        movie.insert()
        actor = Actor(name="Ali", age=22, gender="Male")
        actor.insert()

    def tearDown(self):
        """Executed after reach test"""
        pass

#---------------------------------------------------#
# Endpoints Tests
#---------------------------------------------------#
    def test_get_movies(self):
        res = self.client().get('/movies', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_401_get_movies_no_header(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')
#---------------------------------------------------#
    def test_get_actors(self):
        res = self.client().get('/actors', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_401_get_actors_no_header(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')
#---------------------------------------------------#
    def test_delete_movie(self):
        res = self.client().delete("/movies/1", headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_404_delete_movie_if_movie_not_found(self):
        res = self.client().delete("/movies/5000", headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
#---------------------------------------------------#
    def test_delete_actor(self):
        res = self.client().delete("/actors/1", headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_404_delete_actor_if_actor_not_found(self):
        res = self.client().delete("/actors/5000", headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
#---------------------------------------------------#
    def test_post_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_422_post_movie_unprocessable(self):
        res = self.client().post('/movies', json=self.error_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
#---------------------------------------------------#
    def test_post_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_422_post_actor_unprocessable(self):
        res = self.client().post('/actors', json=self.error_actor, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
#---------------------------------------------------#
    def test_patch_movie(self):
        res = self.client().patch('/movies/2', json=self.new_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_movie_if_movie_not_found(self):
        res = self.client().patch('/movies/111', json=self.new_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
#---------------------------------------------------#
    def test_patch_actor(self):
        res = self.client().patch('/actors/2', json=self.new_actor, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_actor_if_actor_not_found(self):
        res = self.client().patch('/actors/111', json=self.new_actor, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

#---------------------------------------------------#
# RBAC Tests
#---------------------------------------------------#
    def test_casting_assistant_role(self):
        res = self.client().get('/actors', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_401_casting_assistant_role_unauthorized(self):
        res = self.client().post('/actors', json=self.new_actor, headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
#---------------------------------------------------#
    def test_casting_director_role(self):
        res = self.client().post('/actors', json=self.new_actor, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    # casting director does not have post:movies permission
    def test_401_casting_director_role_unauthorized(self):
        res = self.client().post('/movies', json=self.new_movie, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
#---------------------------------------------------#
    # executive producer has all permissions
    def test_executive_producer_role(self):
        res = self.client().post('/actors', json=self.new_actor, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
#---------------------------------------------------#
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()