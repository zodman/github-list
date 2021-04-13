import pytest
from app import app
import seed


def test_seed(mocker, faker):
    mocker.patch("os.remove")
    spy = mocker.patch("seed.fetch_data")
    spy.return_value = [{'id': faker.random_int()} for i in range(1, 15000)]
    spy_populate_db = mocker.patch('seed.populate_database')
    seed.main(15000)
    assert len(spy_populate_db.call_args[0][0]) == 15000


@pytest.fixture
def client(faker):
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_index(mocker, client):
    r = client.get("/?format=json")
    assert r.status_code == 200
