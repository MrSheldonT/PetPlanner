import pytest
from app import create_app
from app.config import TestingConfig
from app.models.petplanner import db

@pytest.fixture
def client():
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def registered_user(client):
    response = client.post('/users/register', json={
        "email": "kukuo798@gmail.com",
        "password": "Losquesaben2",
        "name": "Test User"
    })
    return response

@pytest.fixture
def auth_token(client, registered_user):
    response = client.post('/users/login', json={
        "email": "kukuo798@gmail.com",
        "password": "Losquesaben2"
    })
    return response.get_json()['token']

def test_register_user(registered_user):
    assert registered_user.status_code == 201
    assert registered_user.get_json()['message'] == 'Successfully created user'

def test_login_user(client, registered_user):
    response = client.post('/users/login', json={
        "email": "kukuo798@gmail.com",
        "password": "Losquesaben2"
    })
    assert response.status_code == 200
    assert 'token' in response.get_json()

def test_forgot_password(client, registered_user):
    response = client.post('/users/forgot-password', json={
        "email": "kukuo798@gmail.com"
    })

    assert response.status_code in (200, 500)  
    assert response.get_json()['message'] == 'Email sent'

def test_get_me(client, auth_token):
    response = client.get('/users/me', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    assert response.get_json()['email'] == "kukuo798@gmail.com"
    assert response.get_json()['name'] == "Test User"


def test_edit_user(client, auth_token):
    response = client.put('/users/me', json={
        "name": "New test user",
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    assert response.get_json()['data']['name'] == "New test user"
    assert response.get_json()['message'] == 'user successfully updated'

def test_change_password(client, auth_token):
    response = client.post('/users/reset-password', data={
        "password": "Losquenosaben2"
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == "Password changed"

def test_assign_role_to_user(client, auth_token):
    from app.models.petplanner import User
    from app.models.role import Role
    with client.application.app_context():
        user = User.query.filter_by(email="kukuo798@gmail.com").first()
        user.role = Role.ADMIN.value
        db.session.commit()

    response = client.put('/users/1/role', json={
        "new_role": "USER"
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    print(response.get_json())
    assert response.status_code == 200
    assert response.get_json()['message'] == "Role updated to USER"
