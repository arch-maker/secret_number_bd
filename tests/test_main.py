import os
from unittest.mock import Mock

import pytest
from main import app, db
from model import User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    client = app.test_client()

    cleanup()

    db.create_all()

    yield client


def cleanup():
    db.drop_all()


def test_index_not_logged_in(client):
    response = client.get('/')
    assert b'Introduce tu nombre' in response.data


def test_index_logged_in(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get('/')
    assert b'adivina el numero' in response.data


def test_user_profile(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get("/profile")
    assert b'Test User' in response.data


def test_user_profile_edit(client):
    client.post('/login', data={"user-name": "rubX", "user-email": "test@mail.com",
                                "user-password": "password124"}, follow_redirects=True)

    response = client.post('/profile/edit', data={"profile-name": "RubX2",
                                                  "profile-email": "test999@mail.com"}, follow_redirects=True)

    assert b'RubX2' in response.data
    assert b'test999@mail.com' in response.data


def test_secret_number_correct(client):
    client.post('/login', data={"user-name": "ruben", "user-email": "ruben34@user.com",
                                "user-password": "password124"}, follow_redirects=True)

    user = db.query(User).first()

    user.secret_number = 30
    db.add(user)
    db.commit()

    response = client.post('/result', data={"num_user": 30})
    assert b'Enhorabuena!! El numero correcto es: 30' in response.data


def test_user_profile_delete(client):
    client.post('/login', data={"user-name": "rubX2", "user-email": "test22@mail.com",
                                "user-password": "password124"}, follow_redirects=True)

    response = client.post('/profile/delete', follow_redirects=True)
    assert b'adivina el numero' in response.data


def test_user_mock_db():

    user = Mock()

    user.name = "rubenXR"
    user.email = "test22@mail.com"
    user.password = "password1245"
    user.secret_number = "15"
    user.delete = False

    user = db.query(User).first()

    db.add(user)
    db.commit()
