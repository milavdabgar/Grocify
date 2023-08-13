import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_app(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data

if __name__ == '__main__':
    pytest.main()
