import unittest
from flask import current_app
from app import create_app
from app.main.routes import my_app
from datetime import datetime, timedelta
import json

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.appctx = self.app.app_context()
        self.appctx.push()

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_my_app(self):
        data = [9.999, 10.545]
        latitude = data[0]
        longitude = data[1]
        current_time = datetime.utcnow()
        # test without data in db
        data = my_app(latitude, longitude, current_time)
        data = json.loads(data.get_data().decode("utf-8"))
        assert data['report_type'] == 'new'
        # test with data in db
        data = my_app(latitude, longitude, current_time)
        data = json.loads(data.get_data().decode("utf-8"))
        assert data['report_type'] == 'db'
        # test data of current_time + 23 hours
        data = my_app(latitude, longitude, current_time + timedelta(hours=23))
        data = json.loads(data.get_data().decode("utf-8"))
        assert data['report_type'] == 'db'
        # test data of current_time + 25 hours
        data = my_app(latitude, longitude, current_time + timedelta(hours=25))
        data = json.loads(data.get_data().decode("utf-8"))
        assert data['report_type'] == 'new'
        # test data of current_time + 26 hours
        data = my_app(latitude, longitude, current_time + timedelta(hours=26))
        data = json.loads(data.get_data().decode("utf-8"))
        assert data['report_type'] == 'db'

if __name__ == '__main__':
    unittest.main(verbosity=2)