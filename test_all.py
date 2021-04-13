import pytest
import seed

def test_seed(mocker, faker):
    mocker.patch("seed.init")
    spy = mocker.patch("seed.fetch_data")
    spy.return_value = [
        {
            'id': faker.random_int()
        }
        for i in range(1,15000)
    ]
    spy_populate_db = mocker.patch('seed.populate_database')
    seed.main(15000)
    assert len(spy_populate_db.call_args[0][0]) == 15000

