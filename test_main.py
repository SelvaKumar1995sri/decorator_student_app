import pytest
import unittest

from unittest.mock import patch
from main import Student, view_all, view_student, add_student, delete_student, update_student

class Testmongodb():

    @pytest.fixture(autouse=True)
    def mongo_get(self, mongodb):
        resp = mongodb.list_collection_names()
        self.mongodb = mongodb

    def test_view_all(self):
        with patch('main.get_collection') as mock_mongo:
            mock_mongo.return_value = self.mongodb.mycollection
            resp = view_all()
            assert resp

    def test_view(self):
        with patch('main.get_collection') as mock_mongo:
            mock_mongo.return_value = self.mongodb.mycollection
            resp = view_student(1)
            assert resp

    def test_add(self):
        with patch('main.get_collection') as mock_mongo:
            mock_mongo.return_value = self.mongodb.mycollection
            d = Student(roll_no= 5,
                name = "ramu",
                age = 25,
                location = "vizhupuram")
                            
            resp = add_student(d)
            assert resp

    def test_update(self):
        with patch('main.get_collection') as mock_mongo:
            mock_mongo.return_value = self.mongodb.mycollection
            d = Student(roll_no= 5,
                name = "ramu",
                age = 25,
                location = "vizhupuram")
                            
            resp = update_student(1,d)
            assert resp


    def test_delete(self):
        with patch('main.get_collection') as mock_mongo:
            mock_mongo.return_value = self.mongodb.mycollection                         
            resp = delete_student(1)
            assert resp